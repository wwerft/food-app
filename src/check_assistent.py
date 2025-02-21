import openai
from dotenv import load_dotenv
import os

# API-Key laden
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

ASSISTANT_ID = "asst_oMJDDxhebLO3cMwv9wN4Ij3Y"

try:
    # Assistant-Daten abrufen
    client = openai.OpenAI(api_key=openai.api_key)
    assistant = client.beta.assistants.retrieve(assistant_id=ASSISTANT_ID)

    # Direkt auf Attribute zugreifen
    if hasattr(assistant, "tool_resources") and hasattr(
        assistant.tool_resources, "file_search"
    ):
        vector_store_ids = assistant.tool_resources.file_search.vector_store_ids
        if vector_store_ids:
            print(f"✅ Vector Store ist verknüpft: {vector_store_ids}")
        else:
            print("❌ Kein Vector Store mit dem Assistant verknüpft!")
    else:
        print("❌ Der Assistant hat keine 'file_search' Ressourcen!")

except Exception as e:
    print(f"❌ Fehler beim Abrufen des Assistants: {e}")
