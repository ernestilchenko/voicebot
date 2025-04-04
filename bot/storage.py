# Utwórz plik bot/storage.py
import logging
import os
from datetime import datetime
from google.cloud import storage
from google.oauth2 import service_account
import tempfile

from bot.config import GCS_BUCKET_NAME, GCS_CREDENTIALS_PATH

logger = logging.getLogger(__name__)


class GCSManager:
    """
    Klasa zarządzająca przechowywaniem dokumentów w Google Cloud Storage.
    """

    def __init__(self, credentials_path=GCS_CREDENTIALS_PATH, bucket_name=GCS_BUCKET_NAME):
        """
        Inicjalizacja menedżera Google Cloud Storage.

        Args:
            credentials_path: Ścieżka do pliku z danymi uwierzytelniającymi Google Cloud
            bucket_name: Nazwa bucketa Google Cloud Storage
        """
        try:
            # Uwierzytelnienie za pomocą pliku JSON z kluczem serwisowym
            self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
            self.client = storage.Client(credentials=self.credentials)
            self.bucket = self.client.bucket(bucket_name)
            logger.info(f"Zainicjalizowano połączenie z Google Cloud Storage, bucket: {bucket_name}")
        except Exception as e:
            logger.error(f"Błąd inicjalizacji Google Cloud Storage: {e}")
            raise

    async def upload_document(self, telegram_bot, file_id, user_id, document_name):
        """
        Pobieranie dokumentu z Telegrama i przesyłanie go do Google Cloud Storage.

        Args:
            telegram_bot: Instancja bota Telegram
            file_id: ID pliku w systemie Telegram
            user_id: ID użytkownika
            document_name: Nazwa dokumentu

        Returns:
            str: Ścieżka do pliku w Google Cloud Storage
        """
        try:
            # Pobieranie informacji o pliku z Telegrama
            file_info = await telegram_bot.get_file(file_id)
            file_path = file_info.file_path

            # Tworzenie unikalnej ścieżki dla pliku w GCS
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            gcs_path = f"documents/{user_id}/{timestamp}_{document_name}"

            # Pobieranie pliku z Telegrama do pamięci tymczasowej
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                downloaded_file = await telegram_bot.download_file(file_path, destination=temp_file.name)
                temp_file_path = temp_file.name

            try:
                # Przesyłanie pliku do Google Cloud Storage
                blob = self.bucket.blob(gcs_path)
                blob.upload_from_filename(temp_file_path)

                # Ustawienie typów MIME
                blob.content_type = "application/octet-stream"  # Domyślnie, można dostosować

                # Ustawianie metadanych
                metadata = {
                    'original_filename': document_name,
                    'telegram_file_id': file_id,
                    'user_id': str(user_id),
                    'upload_date': datetime.now().isoformat()
                }
                blob.metadata = metadata
                blob.patch()

                logger.info(f"Pomyślnie przesłano dokument do GCS: {gcs_path}")
                return gcs_path
            finally:
                # Usuwanie pliku tymczasowego
                os.unlink(temp_file_path)

        except Exception as e:
            logger.error(f"Błąd podczas przesyłania dokumentu do GCS: {e}")
            raise

    def get_document_url(self, gcs_path, expire_time=3600):
        """
        Generowanie tymczasowego URL do pobrania dokumentu.

        Args:
            gcs_path: Ścieżka do pliku w Google Cloud Storage
            expire_time: Czas ważności URL w sekundach (domyślnie 1 godzina)

        Returns:
            str: Tymczasowy URL do pobrania pliku
        """
        try:
            blob = self.bucket.blob(gcs_path)
            url = blob.generate_signed_url(
                version="v4",
                expiration=expire_time,
                method="GET"
            )
            return url
        except Exception as e:
            logger.error(f"Błąd podczas generowania URL do dokumentu: {e}")
            raise

    def delete_document(self, gcs_path):
        """
        Usuwanie dokumentu z Google Cloud Storage.

        Args:
            gcs_path: Ścieżka do pliku w Google Cloud Storage

        Returns:
            bool: True jeśli usunięto pomyślnie, False w przeciwnym razie
        """
        try:
            blob = self.bucket.blob(gcs_path)
            blob.delete()
            logger.info(f"Usunięto dokument z GCS: {gcs_path}")
            return True
        except Exception as e:
            logger.error(f"Błąd podczas usuwania dokumentu z GCS: {e}")
            return False