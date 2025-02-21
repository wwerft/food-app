import openai
from dotenv import load_dotenv
import os


class OpenAIStorageCleaner:
    """
    Klasse zum Löschen aller hochgeladenen Dateien aus dem OpenAI Entwickler-Storage.
    """

    def __init__(self):
        """
        Initialisiert den Cleaner mit API-Zugang.
        """
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI(api_key=self.api_key)

    def list_files(self):
        """
        Gibt eine Liste aller hochgeladenen Dateien zurück.
        """
        try:
            response = self.client.files.list()
            file_list = response.data  # Enthält alle Dateien als Liste von Objekten
            return file_list
        except Exception as e:
            print(f"Fehler beim Abrufen der Dateien: {e}")
            return []

    def delete_file(self, file_id):
        """
        Löscht eine Datei anhand ihrer File-ID.
        """
        try:
            self.client.files.delete(file_id=file_id)
            print(f"Datei {file_id} erfolgreich gelöscht.")
        except Exception as e:
            print(f"Fehler beim Löschen der Datei {file_id}: {e}")

    def delete_all_files(self):
        """
        Löscht alle Dateien aus dem OpenAI Storage.
        """
        file_list = self.list_files()

        if not file_list:
            print("Keine Dateien zum Löschen gefunden.")
            return

        for file in file_list:
            file_id = file.id
            print(f"Lösche Datei: {file_id} ...")
            self.delete_file(file_id)

        print("Alle Dateien wurden gelöscht!")


# Beispiel-Nutzung
if __name__ == "__main__":
    cleaner = OpenAIStorageCleaner()
    cleaner.delete_all_files()
