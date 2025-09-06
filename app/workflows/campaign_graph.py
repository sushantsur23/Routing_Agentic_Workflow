# Orchestrator, workers, synthesizer, graph builder

from typing_extensions import TypedDict, Annotated
import operator
from langgraph.constants import START, END
from langgraph.types import Send
from langgraph.graph import StateGraph
from langchain_core.messages import SystemMessage
from app.llms.groq_client import llm

class CampaignState(TypedDict):
    topic: str
    deliverables: list
    completed_assets: Annotated[list, operator.add]
    final_campaign: str

class WorkerState(TypedDict):
    deliverable: dict
    completed_assets: Annotated[list, operator.add]

def orchestrator(state: CampaignState):
    return {"deliverables": [
        {"name": "Email Copy", "description": "Engaging email announcement for customers.", "topic": state["topic"]},
        {"name": "Social Media Ads", "description": "Catchy social media ads.", "topic": state["topic"]},
        {"name": "Blog Post", "description": "Detailed blog introducing the product.", "topic": state["topic"]},
        {"name": "Landing Page Content", "description": "Landing page hero, subheading, benefits, proof, CTA.", "topic": state["topic"]}
    ]}

def worker(state: WorkerState):
    deliverable_name = state['deliverable']['name']
    deliverable_desc = state['deliverable']['description']
    topic = state['deliverable'].get('topic', state.get('topic', ''))

    prompt = f"""
    Campaign Topic: {topic}
    Deliverable: {deliverable_name}
    Description: {deliverable_desc}
    Instructions: Persuasive, conversion-focused copy.
    """
    asset = llm.invoke([SystemMessage(content=prompt)])
    return {"completed_assets": [f"## {deliverable_name}\n\n{asset.content}"]}

def synthesizer(state: CampaignState):
    return {"final_campaign": "\n\n---\n\n".join(state["completed_assets"])}

def assign_workers(state: CampaignState):
    return [Send("worker", {"deliverable": d}) for d in state["deliverables"]]

def build_campaign_workflow():
    campaign_builder = StateGraph(CampaignState)
    campaign_builder.add_node("orchestrator", orchestrator)
    campaign_builder.add_node("worker", worker)
    campaign_builder.add_node("synthesizer", synthesizer)

    campaign_builder.add_edge(START, "orchestrator")
    campaign_builder.add_conditional_edges("orchestrator", assign_workers, ["worker"])
    campaign_builder.add_edge("worker", "synthesizer")
    campaign_builder.add_edge("synthesizer", END)
    return campaign_builder.compile()
