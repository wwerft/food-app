import openai
from dotenv import load_dotenv
import os

# API-Key laden
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Vector Store ID prüfen
VECTOR_STORE_ID = "DEIN_VECTOR_STORE_ID"

client = openai.OpenAI(api_key=openai.api_key)

# Liste der Dateien im Vector Store abrufen
response = client.beta.vector_stores.files.list(vector_store_id=VECTOR_STORE_ID)

print("Verknüpfte Dateien:", response)
