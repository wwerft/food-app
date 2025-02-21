import os
from dotenv import load_dotenv
from pinecone import Pinecone

# .env-Datei laden
load_dotenv()

# Pinecone-Instanz erstellen
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Index-Namen setzen
index_name = "ernaehrungsberater-doc-index"

# Prüfen, ob der Index existiert
if index_name not in pc.list_indexes().names():
    raise ValueError(f"Pinecone-Index '{index_name}' existiert nicht. Bitte prüfen.")

index = pc.Index(index_name)

# Index-Statistiken abrufen
stats = index.describe_index_stats()
print(f"Pinecone Index-Statistiken für '{index_name}':")
print(stats)
