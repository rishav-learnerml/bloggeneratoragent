from typing import Optional
from langchain_groq import ChatGroq
from pydantic import SecretStr
import os
from dotenv import load_dotenv


class GroqLLM:
    def __init__(self) -> None:
        load_dotenv()
        self.groq_api_key: Optional[str] = os.getenv("GROQ_API_KEY")

    def get_llm(self) -> ChatGroq:
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        
        llm: ChatGroq = ChatGroq(api_key=SecretStr(self.groq_api_key), model="llama-3.1-8b-instant")
        return llm
