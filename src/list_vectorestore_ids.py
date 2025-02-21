import openai
from dotenv import load_dotenv
import os

# API-Key laden
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=openai.api_key)

# Alle Vector Stores abrufen
vector_stores = client.beta.vector_stores.list()

print("Vector Stores gefunden:")
for vs in vector_stores.data:
    print(f"ID: {vs.id}, Name: {vs.name}")
