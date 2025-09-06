from __future__ import print_function
import os
import base64
import pickle
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from typing_extensions import TypedDict, Annotated
import operator
from email.mime.text import MIMEText

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.constants import START, END
from langgraph.types import Send
from langgraph.graph import StateGraph

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# ------------------------
# Gmail API Setup
# ------------------------
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

def create_message(sender, to, subject, message_text):
    """Create a Gmail API draft message body"""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'message': {'raw': raw}}

def save_draft(sender, to, subject, message_text):
    """Authenticate and save draft in Gmail"""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    draft_body = create_message(sender, to, subject, message_text)
    draft = service.users().drafts().create(userId="me", body=draft_body).execute()
    return draft['id']

# ------------------------
# LLM Setup
# ------------------------
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="gemma2-9b-it")
planner = ChatOpenAI(model="gpt-4o-mini")  # optional

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
    deliverables = [
        {"name": "Email Copy", "description": "Engaging email announcement for customers.", "topic": state["topic"]},
        {"name": "Social Media Ads", "description": "Catchy social media ads for Twitter/LinkedIn.", "topic": state["topic"]},
        {"name": "Blog Post", "description": "Detailed blog introducing the product.", "topic": state["topic"]},
        {"name": "Landing Page Content", "description": "Hero section, subheading, benefits, proof, and CTA.", "topic": state["topic"]},
    ]
    return {"deliverables": deliverables}

def worker(state: WorkerState):
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
    completed_assets = state["completed_assets"]
    final_doc = "\n\n---\n\n".join(completed_assets)
    return {"final_campaign": final_doc}

def assign_workers(state: CampaignState):
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
# Streamlit App
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

    # Extract email copy for draft
    # email_copy = next((a for a in state["completed_assets"] if a.startswith("## Email Copy")), "")
    # email_subject = "Your AI-Powered Campaign Email Draft"
    # email_body = email_copy.replace("## Email Copy", "").strip()

    import re

    email_copy = next((a for a in state["completed_assets"] if a.startswith("## Email Copy")), "")

    email_subject, email_body = "AI Campaign Draft", ""
    if email_copy:
        try:
            cleaned = email_copy.replace("## Email Copy", "").strip()

            # Try to extract subject from the copy
            match = re.search(r"Subject:\s*(.*)", cleaned, re.IGNORECASE)
            if match:
                email_subject = match.group(1).strip()
                email_body = cleaned.replace(match.group(0), "").strip()
                sender = os.getenv("EMAIL_SENDER")
                receiver = os.getenv("EMAIL_RECEIVER", sender)  # default: send to self
                draft_id = save_draft(sender, receiver, email_subject, email_body)
                st.success(f"✅ Draft saved to Gmail with ID: {draft_id}")
            else:
                email_body = cleaned
        except Exception as e:
            st.error(f"❌ Failed to save Gmail draft: {e}")



    if email_body:
        try:
            sender = os.getenv("EMAIL_SENDER")
            receiver = os.getenv("EMAIL_RECEIVER", sender)  # default: send to self
            draft_id = save_draft(sender, receiver, email_subject, email_body)
            st.success(f"✅ Draft saved to Gmail with ID: {draft_id}")
        except Exception as e:
            st.error(f"❌ Failed to save Gmail draft: {e}")
