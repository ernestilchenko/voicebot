import logging
from datetime import datetime, timedelta
import pytz
import random

from webapp.database import SessionLocal
from webapp.models import User, Document

logger = logging.getLogger(__name__)


class CrewManager:
    """
    Prosta implementacja menedżera Crew AI do analizy dokumentów.
    Ta wersja nie wymaga zewnętrznych API i służy jako przykład.
    """

    def __init__(self, api_key=None):
        """
        Inicjalizacja menedżera.

        Args:
            api_key: Opcjonalny klucz API (nie używany w tej wersji)
        """
        logger.info("Zainicjalizowano uproszczoną wersję Crew AI Manager")

    def create_document_analysis_crew(self, document_id):
        """
        Uproszczona "analiza" dokumentu zwracająca predefiniowane rekomendacje.

        Args:
            document_id: ID dokumentu do analizy

        Returns:
            str: Wyniki analizy dokumentu
        """
        db = SessionLocal()
        try:
            document = db.query(Document).filter(Document.id == document_id).first()
            user = db.query(User).filter(User.id == document.user_id).first()

            if not document or not user:
                logger.error(f"Nie znaleziono dokumentu lub użytkownika: document_id={document_id}")
                return "Błąd: Nie znaleziono dokumentu lub użytkownika"

            # Symulacja czasu przetwarzania
            import time
            time.sleep(1)

            # Obliczenia na podstawie daty wygaśnięcia
            current_date = datetime.now(pytz.UTC)
            days_left = (document.expiration_date - current_date).days if document.expiration_date else 30

            # Określenie priorytetu
            if days_left <= 14:
                priority = "KRYTYCZNY"
            elif days_left <= 30:
                priority = "WYSOKI"
            elif days_left <= 60:
                priority = "ŚREDNI"
            else:
                priority = "NISKI"

            # Losowe rekomendacje w zależności od priorytetu
            recommendations = []
            if priority in ["KRYTYCZNY", "WYSOKI"]:
                recommendations = [
                    "Natychmiast rozpocznij proces odnowienia dokumentu",
                    "Przygotuj wszystkie potrzebne dokumenty w ciągu 2 dni",
                    "Skontaktuj się z urzędem telefonicznie dla przyspieszenia procesu",
                    "Rozważ opcję przyspieszenia za dodatkową opłatą"
                ]
            else:
                recommendations = [
                    f"Zaplanuj odnowienie dokumentu na co najmniej {max(14, days_left - 30)} dni przed wygaśnięciem",
                    "Przygotuj wymagane dokumenty i zrób ich kopie",
                    "Sprawdź godziny otwarcia urzędu i wymagania online",
                    "Zarezerwuj termin wizyty z wyprzedzeniem"
                ]

            # Formatowanie wyniku
            result = (
                f"*Analiza dokumentu: {document.name}*\n\n"
                f"📊 *Priorytet*: {priority}\n"
                f"⏱️ *Pozostały czas*: {days_left} dni\n"
                f"📅 *Data wygaśnięcia*: {document.expiration_date.strftime('%d.%m.%Y') if document.expiration_date else 'Brak'}\n\n"
                f"*Rekomendowane działania:*\n"
            )

            for i, rec in enumerate(recommendations, 1):
                result += f"{i}. {rec}\n"

            result += "\n*Uwaga*: To jest symulacja analizy dokumentu. W pełnej wersji Crew AI, analiza byłaby znacznie bardziej dokładna i spersonalizowana."

            logger.info(f"Wygenerowano analizę dla dokumentu {document_id}")
            return result

        except Exception as e:
            logger.error(f"Błąd podczas analizy dokumentu: {e}")
            return f"Wystąpił błąd podczas analizy: {str(e)}"
        finally:
            db.close()

    async def generate_custom_reminder(self, user_id, document_id, reminder_type):
        """
        Generuje proste przypomnienie dla użytkownika.

        Args:
            user_id: ID użytkownika
            document_id: ID dokumentu
            reminder_type: Typ przypomnienia ('telegram', 'sms', 'voice')

        Returns:
            str: Treść przypomnienia
        """
        db = SessionLocal()
        try:
            document = db.query(Document).filter(Document.id == document_id).first()
            user = db.query(User).filter(User.id == user_id).first()

            if not document or not user:
                return None

            # Przykładowe szablony przypomnień
            if reminder_type == 'telegram':
                templates = [
                    f"📢 Ważne przypomnienie: Twój dokument '{document.name}' wygaśnie dnia {document.expiration_date.strftime('%d.%m.%Y')}. Zaplanuj odnowienie już teraz.",
                    f"⚠️ {user.first_name}, zostało tylko {(document.expiration_date - datetime.now(pytz.UTC)).days} dni do wygaśnięcia dokumentu '{document.name}'. Nie zwlekaj z odnowieniem.",
                    f"🔔 Przypomnienie: '{document.name}' traci ważność {document.expiration_date.strftime('%d.%m.%Y')}. Zadbaj o jego odnowienie w odpowiednim czasie."
                ]
            elif reminder_type == 'sms':
                templates = [
                    f"PRZYPOMNIENIE: Dokument '{document.name}' wygasa {document.expiration_date.strftime('%d.%m.%Y')}. Zaplanuj odnowienie.",
                    f"{user.first_name}, Twoj dokument wygasa wkrotce. Odnow go do {document.expiration_date.strftime('%d.%m.%Y')}.",
                    f"Wazne: '{document.name}' traci waznosc za {(document.expiration_date - datetime.now(pytz.UTC)).days} dni. Skontaktuj sie z urzedem."
                ]
            elif reminder_type == 'voice':
                templates = [
                    f"Dzień dobry, przypominamy że dokument {document.name} wygasa dnia {document.expiration_date.strftime('%d %B %Y')}. Proszę zaplanować wizytę w urzędzie w celu jego odnowienia.",
                    f"Witaj {user.first_name}, dzwonimy przypomnieć o zbliżającym się terminie ważności dokumentu {document.name}. Prosimy o kontakt z urzędem w celu jego przedłużenia.",
                    f"Automatyczne przypomnienie: dokument {document.name} wygaśnie za {(document.expiration_date - datetime.now(pytz.UTC)).days} dni. Prosimy o podjęcie działań w celu jego odnowienia."
                ]
            else:
                templates = [
                    f"Przypomnienie: Dokument '{document.name}' wygasa {document.expiration_date.strftime('%d.%m.%Y')}."
                ]

            # Wybierz losowy szablon
            return random.choice(templates)

        except Exception as e:
            logger.error(f"Błąd podczas generowania przypomnienia: {e}")
            return None
        finally:
            db.close()