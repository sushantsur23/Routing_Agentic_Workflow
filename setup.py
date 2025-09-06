from setuptools import setup, find_packages

setup(
    name="Routing_Agentic_AI_Workflow",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "langchain",
        "langchain-groq",
        "langgraph",
        "python-dotenv",
        "langchain",
        "langchain_huggingface",
        "langchain-tavily",
        "reportlab",
        "google-api-python-client",
        "google_auth_oauthlib",
        "langchain-openai",
        "langchain-groq",
        "pytest"
            ],

    author="Sushant Sur",
    description="ROuting Agentic AI Workflow",
    python_requires=">=3.12",
)
