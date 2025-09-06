# Streamlit entry point
import os, re
import streamlit as st
from dotenv import load_dotenv
from app.workflows.campaign_graph import *
from app.services.gmail_service import save_draft
from app.utils.helpers import *
from app.graphs.save_graphs import *


load_dotenv()

logger = get_logger(__name__)


campaign_workflow = build_campaign_workflow()

# Save graph in multiple formats
save_workflow_graph(campaign_workflow, "campaign_workflow.png", outdir="./graphs")
# save_workflow_graph(campaign_workflow, "campaign_workflow.svg", outdir="../graphs")
save_workflow_graph(campaign_workflow, "campaign_workflow.jpg", outdir="./graphs")
print("✅ Graph saved as successfully")

st.set_page_config(page_title="Marketing Campaign Generator", layout="wide")
st.title("🚀 AI Marketing Campaign Generator")
logging.info("Starting to create Agents ans schedule the task accordingly")

with st.form("campaign_form"):
    topic = st.text_area("✍️ Enter Campaign Details", height=200)
    submitted = st.form_submit_button("Generate Campaign")

if submitted and topic.strip():
    with st.spinner("🔮 Generating campaign assets..."):
        state = campaign_workflow.invoke({"topic": topic})

    st.subheader("📦 Final Campaign Package")
    st.markdown(state["final_campaign"])

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
            logging.info("Create the marketing content and saved email copy to Gmail.")
        except Exception as e:
            st.error(f"❌ Failed to save Gmail draft: {e}")
            logging.error("Failed to save the email content to draft on Gmail")
