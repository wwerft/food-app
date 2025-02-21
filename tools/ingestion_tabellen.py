from dotenv import load_dotenv
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Umgebungsvariablen laden
load_dotenv()

# OpenAI Embeddings für Text
text_embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# PDF-Verzeichnis definieren
PDF_DIRECTORY = "../docs1"  # <-- Pfad anpassen

def ingest_docs():
    """Lädt PDFs, verarbeitet Inhalte und speichert sie in Pinecone."""

    # Alle PDF-Dateien im Verzeichnis sammeln
    pdf_files = [
        os.path.join(PDF_DIRECTORY, f)
        for f in os.listdir(PDF_DIRECTORY)
        if f.endswith(".pdf")
    ]

    if not pdf_files:
        print("Keine PDFs im angegebenen Verzeichnis gefunden.")
        return

    raw_documents = []

    for pdf in pdf_files:
        print(f"Lade Datei: {pdf}")
        try:
            loader_text = PyMuPDFLoader(pdf)
            text_docs = loader_text.load()
            raw_documents.extend(text_docs)
        except Exception as e:
            print(f"Fehler beim Laden von Text aus {pdf}: {e}")

    if not raw_documents:
        print("Keine verwertbaren Textdokumente gefunden. Beende Vorgang.")
        return

    print(f"Geladen: {len(raw_documents)} Text-Dokumente")

    # Text in kleine Chunks zerlegen
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)

    print(f"Bereite {len(documents)} Text-Dokumente für Pinecone vor")

    # Text in Pinecone speichern
    try:
        PineconeVectorStore.from_documents(
            documents, text_embeddings, index_name="ernaehrungsberater-doc-index"
        )
        print("Text in Pinecone gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern von Text in Pinecone: {e}")

if __name__ == "__main__":
    print(__file__)
    ingest_docs()
