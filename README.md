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

### 💡 My Solution: Marketing Campaign Generator

This project introduces an **Agentic AI Workflow** for automated marketing campaign creation:

- **Orchestrator** 🧑‍💼 → Defines deliverables (Email Copy, Social Media Ads, Blog Post, Landing Page).  
- **Workers** ✍️ → Generate each asset individually using LLMs.  
- **Synthesizer** 📦 → Bundles all assets into a cohesive campaign package.  

✅ The result is a **faster, more consistent, and cost-efficient** way to generate complete marketing campaigns.

# 🚀 Routing Agentic AI Workflow

Welcome to the **Routing Agentic AI Workflow**!  
This ACS container aligned with AWS Fargate demonstrates how to build and deploy an **AI-powered campaign workflow generator** using **LangChain, LangGraph, and Groq LLMs**.  

## ✨ Features
- 🔗 **Agentic workflow routing** – dynamically routes requests through different agents.  
- 📧 **Campaign generator** – creates AI-powered marketing campaign drafts.  
- 🌐 **Web search integration** – leverages external data (via Tavily API or similar).  
- ⚡ **Groq-powered LLMs** – optimized for high-speed inference.  
- 🎨 Built with **Streamlit** for an interactive UI.
- ☁️ Deployed on AWS ECS with Fargate – scalable, serverless container orchestration.

## 🏗️ Architecture Flow

![Architecture Flow](https://github.com/sushantsur23/Routing_Agentic_workflow_Rev/blob/3cc1736ef2b79843da7e3491eb3d1a528991a9da/graphs/campaign_workflow.jpg)

## 📂 Project Structure
![Project structure explained in brief](https://github.com/sushantsur23/Routing_Agentic_workflow_Rev/blob/3cc1736ef2b79843da7e3491eb3d1a528991a9da/graphs/project_structure.png)

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
- Deployed via **AWS ECS and Fargate (Docker)**  

## 🔐 Additional Setup Notes

### 1. Google Cloud Credentials
To enable saving generated email copies as **Gmail drafts**, you must:
- Download the `credentials.json` file from your **Google Cloud Console** (OAuth Client ID).
- Place the file in your project root directory.
- This allows the app to authenticate with **Google APIs** securely.

⚠️ Never commit `credentials.json` to GitHub. Add it to `.gitignore`.

---

### 2. VPN Requirements for AWS + Gmail Integration
When running this project on AWS, you may need to configure **VPN settings**.  
- This is required because Gmail APIs open a browser window for OAuth authentication.  
- Without VPN configuration, AWS may block the browser-based login flow.  
- Ensure your VPN is correctly set up so that the Gmail authentication screen can load and let you save drafts.

---

### 3. AWS ECS Task Definition
When deploying to **Amazon ECS**, you must provide a `task-definition.json` file.  

Steps:
1. Create or update your ECS Task Definition in the AWS Console or via CLI.  
2. Export it to your local project using:  
   ```bash
   aws ecs describe-task-definition \
     --task-definition Agentic-routing \
     --query taskDefinition > task-definition.json

### 4. Application Load Balancer (ALB) for Fixed Endpoint

By default, every time the ECS service or task is redeployed, the **public IP address** of the running container may change.  
This can cause issues when you need a stable endpoint for accessing the app.

✅ To solve this, you should attach an **Application Load Balancer (ALB)** in front of your ECS Fargate service:
- The ALB provides a **fixed DNS name** that does not change across deployments.  
- Incoming traffic is routed from the ALB to the ECS tasks automatically.  
- This ensures that your application is always accessible at the same endpoint, even if containers restart or move between nodes.

**Recommended Setup:**
1. Create an **ALB** in your AWS account (ECS → Load Balancers → Application Load Balancer).  
2. Configure a **Target Group** for your ECS Fargate service.  
3. Attach the ECS service to the ALB target group.  
4. Update your DNS (if applicable) to point to the ALB endpoint.  

With this setup:
- The ALB URL (e.g., `http://my-app-alb-123456789.us-east-1.elb.amazonaws.com`) will remain constant.  
- You won’t need to worry about changing IP addresses after each deployment.

## 🙌 Acknowledgements
Special thanks to the **LangChain** and **AWS** teams for making deployment accessible.  

---


🔥 Try it live right here on!  

