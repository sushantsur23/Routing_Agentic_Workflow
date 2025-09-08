# Routing_Agentic_workflow_Rev

## 📝 Problem Statement

Marketing teams often struggle to **orchestrate, generate, and unify campaign assets** across multiple platforms.  
Traditionally, this involves:
- Drafting **email copy** separately.
- Designing **social media ads** in isolation.
- Creating **blog posts** without alignment.
- Building **landing pages** with minimal integration.

This fragmented process leads to:
- 🔄 Duplicated effort.  
- ⚡ Slow turnaround time.  
- 🎯 Inconsistent brand messaging.  

---

### 💡 Our Solution: Marketing Campaign Generator

This project introduces an **Agentic AI Workflow** for automated marketing campaign creation:

- **Orchestrator** 🧑‍💼 → Defines deliverables (Email Copy, Social Media Ads, Blog Post, Landing Page).  
- **Workers** ✍️ → Generate each asset individually using LLMs.  
- **Synthesizer** 📦 → Bundles all assets into a cohesive campaign package.  

✅ The result is a **faster, more consistent, and cost-efficient** way to generate complete marketing campaigns.

# 🚀 Routing Agentic AI Workflow

Welcome to the **Routing Agentic AI Workflow**!  
This Hugging Face Space demonstrates how to build and deploy an **AI-powered campaign workflow generator** using **LangChain, LangGraph, and Groq LLMs**.  

## ✨ Features
- 🔗 **Agentic workflow routing** – dynamically routes requests through different agents.  
- 📧 **Campaign generator** – creates AI-powered marketing campaign drafts.  
- 🌐 **Web search integration** – leverages external data (via Tavily API or similar).  
- ⚡ **Groq-powered LLMs** – optimized for high-speed inference.  
- 🎨 Built with **Streamlit** for an interactive UI.

## 📂 Project Structure
[Project structure explained in brief](graphs/project_structure.png)

## 🔑 Environment Variables

This project uses a `.env` file to manage API keys securely.  
You need to create this file in the **project root directory**.

### 🔹 1. Create `.env` file
In your project root, create a file named `.env`:

```bash
touch .env

🔹 2. Add the following variables
GROQ_API_KEY → Required for using Groq-hosted LLMs (high-speed inference).
OPENAI_API_KEY → Required if you use OpenAI models.
TAVILY_API_KEY → Required for internet search integration with Tavily.
EMAIL_SENDER → Email sender for gmail.
EMAIL_RECEIVER → Target email for gmail.


## ⚙️ Project Setup (Developer Notes)

This project includes an `init.sh` script to set up the required structure and dependencies.

### 🔹 1. Run Initialization Script
In your Git Bash or terminal, run:
```bash
./init.sh

###🔹 2. Install project as package
```bash 
pip install .

🔹 3. Run the Streamlit App
```bash
streamlit run app/mainapp.py --server.port=8000 --server.address=0.0.0.0

## 🚀 How to Use
1. Enter your campaign details in the text box.  
2. Send the instruction to the agent. Here tavily API Search will help to get the bees information from the web search. 
3. The AI agents will collaborate and generate outputs in terms of mail to be sent, markeing to be done across channels, landing page example.  
4. Automatically the copy of the email is saved as draft based on from and to sender as updaed.  

## 🛠️ Tech Stack
- [Streamlit](https://streamlit.io/)  
- [LangChain](https://www.langchain.com/) + [LangGraph](https://www.langchain.com/langgraph)  
- [Groq LLMs](https://groq.com/)  
- [Tavily API](https://tavily.com/) (for search integration)  
- Deployed via **Hugging Face Spaces (Docker)**  

## 🙌 Acknowledgements
Special thanks to the **LangChain** and **Hugging Face** teams for making open-source AI development accessible.  

---

🔥 Try it live right here on!  


## 📂 Project Structure

