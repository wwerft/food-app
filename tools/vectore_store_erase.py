from dotenv import load_dotenv
import os
from pinecone import Pinecone

# Umgebungsvariablen laden
load_dotenv()

# Pinecone-Instanz erstellen
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Index-Namen definieren (Anpassen, falls nötig)
INDEX_NAME = "ernaehrungsberater-doc-index"


def clear_pinecone_index():
    """Löscht alle Vektoren aus dem angegebenen Pinecone-Index."""

    if INDEX_NAME not in pc.list_indexes().names():
        print(f"Index '{INDEX_NAME}' existiert nicht. Vorgang abgebrochen.")
        return

    # Index referenzieren
    index = pc.Index(INDEX_NAME)

    # Anzahl der gespeicherten Vektoren abrufen
    stats = index.describe_index_stats()
    vector_count = stats.get("total_vector_count", 0)

    if vector_count == 0:
        print("Der Index ist bereits leer.")
        return

    print(f"Lösche {vector_count} Vektoren aus '{INDEX_NAME}'...")

    # Alle Vektoren entfernen
    index.delete(delete_all=True)

    print("Alle Vektoren wurden erfolgreich gelöscht.")


if __name__ == "__main__":
    clear_pinecone_index()
