import openai
from dotenv import load_dotenv
import os

# API-Key laden
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

ASSISTANT_ID = "asst_oMJDDxhebLO3cMwv9wN4Ij3Y"
VECTOR_STORE_ID = "vs_67ab7b6c55f4819182bfb78c6f4f6b9e"


def list_vector_store_files():
    """Holt alle Datei-IDs aus dem Vector Store und ruft die Namen separat ab"""
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.beta.vector_stores.files.list(vector_store_id=VECTOR_STORE_ID)

        # Datei-IDs abrufen
        file_ids = [file.id for file in response.data]

        if not file_ids:
            print("❌ Keine Dateien im Vector Store gefunden!")
            return []

        file_names = []
        for file_id in file_ids:
            file_info = client.files.retrieve(file_id)  # Hier holen wir den Dateinamen
            file_name = getattr(file_info, "filename", f"Unbekannte Datei ({file_id})")
            file_names.append(file_name)

        return file_names

    except Exception as e:
        print(f"❌ Fehler beim Abrufen der Dateien: {e}")
        return []


# Teste das Skript
files = list_vector_store_files()
print("📂 Hochgeladene Dokumente:", files)
