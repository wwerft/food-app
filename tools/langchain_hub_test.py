import os
from dotenv import load_dotenv
from langchain import hub

# Lade die Umgebungsvariablen aus der .env Datei
load_dotenv()

# Überprüfe, ob der LangChain API-Key gesetzt ist
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

if not LANGSMITH_API_KEY:
    print(
        "WARNUNG: Kein LangChain API-Key gefunden! Bitte setze ihn in der .env Datei."
    )
else:
    print("LangChain API-Key gefunden!")

# Teste das Abrufen des Prompts
try:
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    print("Prompt erfolgreich geladen!")
except Exception as e:
    print(f"Fehler beim Laden des Prompts: {e}")
