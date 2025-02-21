import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

print("check_langsmith.py")
print("LANGSMITH_API_KEY:", os.getenv("LANGSMITH_API_KEY"))  # Sollte nicht None sein


llm = ChatOpenAI()
llm.invoke("Hello, world!")
