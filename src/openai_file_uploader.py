import openai
from dotenv import load_dotenv
import os
import time


class OpenAIFileUploader:
    """
    Klasse zur Verwaltung des Datei-Uploads und Verknüpfung mit einem OpenAI Assistant über einen Vector Store.
    """

    def __init__(self, directory: str, assistant_id: str):
        """
        Initialisiert den Uploader mit einem Verzeichnis und dem Assistant-ID.
        """
        load_dotenv()  # Lade Umgebungsvariablen
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=self.api_key)
        self.directory = directory
        self.assistant_id = assistant_id

    def get_files(self):
        """
        Liest alle Dateien im angegebenen Verzeichnis aus.
        """
        try:
            files = [
                os.path.join(self.directory, f)
                for f in os.listdir(self.directory)
                if os.path.isfile(os.path.join(self.directory, f))
            ]
            if not files:
                raise FileNotFoundError(
                    "Keine Dateien im angegebenen Verzeichnis gefunden."
                )
            return files
        except Exception as e:
            print(f"❌ Fehler beim Einlesen der Dateien: {e}")
            return []

    def upload_file(self, file_path: str):
        """
        Lädt eine Datei zu OpenAI hoch und gibt die File-ID zurück.
        """
        try:
            with open(file_path, "rb") as file:
                response = self.client.files.create(file=file, purpose="assistants")
            print(f"✅ Datei hochgeladen: {file_path} → File-ID: {response.id}")
            return response.id  # Die File-ID
        except Exception as e:
            print(f"❌ Fehler beim Hochladen der Datei {file_path}: {e}")
            return None

    def upload_all_files(self):
        """
        Lädt alle Dateien aus dem Verzeichnis hoch und gibt eine Liste der File-IDs zurück.
        """
        files = self.get_files()
        if not files:
            return []

        file_ids = []
        for file in files:
            print(f"📤 Lade hoch: {file} ...")
            file_id = self.upload_file(file)
            if file_id:
                file_ids.append(file_id)

        return file_ids

    def create_vector_store(self, file_ids):
        """
        Erstellt einen Vector Store und fügt die hochgeladenen Dateien hinzu.
        """
        if not file_ids:
            print("⚠️ Keine Datei-IDs vorhanden, daher kein Vector Store möglich.")
            return None

        try:
            response = self.client.beta.vector_stores.create(
                name="Ernährungsberatung", file_ids=file_ids
            )
            vector_store_id = response.id
            print(f"✅ Vector Store erstellt: {vector_store_id}")

            # Warten, bis die Dateien verarbeitet wurden
            print("⏳ Warte auf die Verarbeitung der Dateien...")
            time.sleep(10)  # Wartezeit für OpenAI Verarbeitung

            return vector_store_id
        except Exception as e:
            print(f"❌ Fehler beim Erstellen des Vector Stores: {e}")
            return None

    def attach_vector_store_to_assistant(self, vector_store_id):
        """
        Verknüpft den erstellten Vector Store mit dem OpenAI Assistant.
        """
        if not vector_store_id:
            print(
                "⚠️ Keine Vector Store ID vorhanden, daher keine Verknüpfung mit dem Assistant."
            )
            return None

        try:
            response = self.client.beta.assistants.update(
                assistant_id=self.assistant_id,
                tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
            )
            print(
                f"🎯 Assistant {self.assistant_id} erfolgreich mit Vector Store {vector_store_id} verknüpft!"
            )
            return response
        except Exception as e:
            print(f"❌ Fehler beim Verknüpfen des Vector Stores mit dem Assistant: {e}")
            return None


# Beispiel-Nutzung:
if __name__ == "__main__":
    directory_path = (
        r"C:\Bauland\InternalProjects\Kunze\Dokumente"  # Windows-kompatibler Pfad
    )
    assistant_id = "asst_oMJDDxhebLO3cMwv9wN4Ij3Y"  # Deine gespeicherte Assistant-ID

    uploader = OpenAIFileUploader(directory_path, assistant_id)

    uploaded_files = uploader.upload_all_files()

    if uploaded_files:
        print("✅ Hochgeladene Datei-IDs:", uploaded_files)

        # Erstelle einen Vector Store mit den hochgeladenen Dateien
        vector_store_id = uploader.create_vector_store(uploaded_files)

        # Verknüpfe den Vector Store mit dem Assistant
        uploader.attach_vector_store_to_assistant(vector_store_id)
    else:
        print("⚠️ Es wurden keine Dateien hochgeladen.")
