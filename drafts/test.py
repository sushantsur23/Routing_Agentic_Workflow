import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.constants import START, END
from langgraph.types import Send
from langgraph.graph import StateGraph
from typing_extensions import TypedDict, Annotated
import operator

# ------------------------
# LLM Setup
# ------------------------
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="gemma2-9b-it")

planner = ChatOpenAI(model="gpt-4o-mini")  # optional if used later

# ------------------------
# Graph States
# ------------------------
class CampaignState(TypedDict):
    topic: str
    deliverables: list
    completed_assets: Annotated[list, operator.add]
    final_campaign: str

class WorkerState(TypedDict):
    deliverable: dict
    completed_assets: Annotated[list, operator.add]

# ------------------------
# Workflow Nodes
# ------------------------
def orchestrator(state: CampaignState):
    """Generate a marketing campaign plan with deliverables"""
    deliverables = [
        {"name": "Email Copy", "description": "Engaging email announcement for customers.", "topic": state["topic"]},
        {"name": "Social Media Ads", "description": "Catchy social media ads for Twitter/LinkedIn.", "topic": state["topic"]},
        {"name": "Blog Post", "description": "Detailed blog introducing the product.", "topic": state["topic"]},
        {"name": "Landing Page Content", "description": "Hero Section (Big Promise / Attention Grabber), Subheading (Expand the value proposition), Key Benefits (short, scannable bullets), Social Proof / Authority Cues (trust elements, even if placeholders for now), Call to Action (clear, urgent, repeated) for a landing page.", "topic": state["topic"]},
    ]
    return {"deliverables": deliverables}

def worker(state: WorkerState):
    """Worker generates content for one deliverable"""
    deliverable_name = state['deliverable']['name']
    deliverable_desc = state['deliverable']['description']
    topic = state['deliverable'].get('topic', state.get('topic', ''))

    prompt = f"""
    You are a senior marketing copywriter specializing in SaaS product launches.
    Campaign Topic: {topic}
    Deliverable: {deliverable_name}
    Description: {deliverable_desc}

    Instructions:
    - Directly produce the final {deliverable_name}.
    - Use persuasive, benefit-driven language.
    - Focus on conversion (clear CTA for early access signup).
    - Adapt tone and format depending on the deliverable.
    """
    asset = llm.invoke([SystemMessage(content=prompt)])
    return {"completed_assets": [f"## {deliverable_name}\n\n{asset.content}"]}

def synthesizer(state: CampaignState):
    """Merge campaign assets into final package"""
    completed_assets = state["completed_assets"]
    final_doc = "\n\n---\n\n".join(completed_assets)
    return {"final_campaign": final_doc}

def assign_workers(state: CampaignState):
    """Assign a worker to each deliverable in the plan"""
    return [Send("worker", {"deliverable": d}) for d in state["deliverables"]]

# ------------------------
# Build Workflow
# ------------------------
campaign_builder = StateGraph(CampaignState)
campaign_builder.add_node("orchestrator", orchestrator)
campaign_builder.add_node("worker", worker)
campaign_builder.add_node("synthesizer", synthesizer)

campaign_builder.add_edge(START, "orchestrator")
campaign_builder.add_conditional_edges("orchestrator", assign_workers, ["worker"])
campaign_builder.add_edge("worker", "synthesizer")
campaign_builder.add_edge("synthesizer", END)

campaign_workflow = campaign_builder.compile()

# ------------------------
# Streamlit App UI
# ------------------------
st.set_page_config(page_title="Marketing Campaign Generator", layout="wide")
st.title("🚀 AI Marketing Campaign Generator")

st.write("Provide details about your product or campaign, and the AI will generate Email Copy, Social Ads, Blog, and Landing Page content.")

with st.form("campaign_form"):
    topic = st.text_area(
        "✍️ Enter Campaign Details",
        placeholder="Example: ProWrite AI — an AI-powered writing assistant that helps marketers, consultants, and writers create content 3x faster. Goal: early access signups. Tone: professional but approachable.",
        height=200
    )
    submitted = st.form_submit_button("Generate Campaign")

if submitted and topic.strip():
    with st.spinner("🔮 Generating campaign assets..."):
        state = campaign_workflow.invoke({"topic": topic})

    st.subheader("📦 Final Campaign Package")
    st.markdown(state["final_campaign"])
