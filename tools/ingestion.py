from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.schema import Document  # Importiere Document-Klasse

# Umgebungsvariablen laden
load_dotenv()

# OpenAI Embeddings für Text
text_embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# PDF-Verzeichnis definieren
PDF_DIRECTORY = "../docs"  # <-- Pfad anpassen


def ingest_docs():
    """Lädt PDFs, verarbeitet Inhalte und speichert sie in Pinecone."""
    print("Starte den Ingest-Prozess...")

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
            loader = PyPDFLoader(pdf)
            pages = loader.lazy_load()
            for page in pages:
                doc = Document(page_content=page.page_content, metadata=page.metadata)
                raw_documents.append(doc)  # Füge das Dokument-Objekt hinzu
                print(page.metadata)

        except Exception as e:
            print(f"Fehler beim Laden von {pdf}: {e}")

    if not raw_documents:
        print("Keine verwertbaren Textdokumente gefunden. Beende Vorgang.")
        return

    print(f"Gesamtzahl der geladenen Seiten: {len(raw_documents)}")

    # Text in kleine Chunks zerlegen
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)  # raw_documents ist jetzt eine Liste von Document-Objekten

    print(f"Bereite {len(documents)} Text-Dokumente für Pinecone vor...")

    # Text in Pinecone speichern
    try:
        PineconeVectorStore.from_documents(
            documents, text_embeddings, index_name="ernaehrungsberater-doc-index"
        )
        print("Text erfolgreich in Pinecone gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern von Text in Pinecone: {e}")


if __name__ == "__main__":
    print("Ingestion")
    ingest_docs()
