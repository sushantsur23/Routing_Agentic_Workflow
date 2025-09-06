# ChatGroq setup

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="gemma2-9b-it")
