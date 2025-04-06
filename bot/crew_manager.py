import logging
from datetime import datetime

import pytz

from webapp.database import SessionLocal
from webapp.models import User, Document

logger = logging.getLogger(__name__)


class CrewManager:
    """
    Implementacja menedżera Crew AI do analizy dokumentów i ich zawartości.
    """

    def __init__(self, api_key=None):
        """
        Inicjalizacja menedżera.

        Args:
            api_key: Opcjonalny klucz API (nie używany w tej wersji)
        """
        logger.info("Zainicjalizowano CrewManager z funkcją analizy zawartości dokumentów")

    def _extract_document_content(self, document):
        """
        Symuluje ekstrakcję zawartości dokumentu na podstawie jego metadanych.
        W rzeczywistej implementacji, pobieralibyśmy plik z GCS i analizowalibyśmy jego zawartość.

        Args:
            document: Obiekt dokumentu z bazy danych

        Returns:
            dict: Zasymulowana zawartość dokumentu
        """
        # Symulowanie zawartości na podstawie nazwy dokumentu
        doc_name = document.name.lower() if document.name else "dokument"

        # Słownik możliwych typów dokumentów i ich zawartości
        document_types = {
            "dowod": {
                "type": "Dowód osobisty",
                "fields": ["Nazwisko", "Imię", "PESEL", "Data urodzenia", "Płeć", "Adres zameldowania", "Data wydania",
                           "Data ważności"],
                "content": "Dokument tożsamości wydany przez organ państwowy, potwierdzający tożsamość obywatela.",
                "issuer": "Urząd miasta/gminy",
                "renewal_process": "Wymaga osobistej wizyty w urzędzie i zdjęcia biometrycznego. Czas odnowienia: 2-4 tygodnie."
            },
            "paszport": {
                "type": "Paszport",
                "fields": ["Nazwisko", "Imię", "PESEL", "Data urodzenia", "Płeć", "Miejsce urodzenia", "Data wydania",
                           "Data ważności"],
                "content": "Dokument podróży uprawniający do przekraczania granic państwowych.",
                "issuer": "Urząd wojewódzki",
                "renewal_process": "Wymaga złożenia wniosku w urzędzie wojewódzkim lub konsularnym. Czas odnowienia: 3-4 tygodnie."
            },
            "prawo": {
                "type": "Prawo jazdy",
                "fields": ["Nazwisko", "Imię", "Data urodzenia", "Miejsce urodzenia", "Data wydania", "Data ważności",
                           "Kategorie uprawnień"],
                "content": "Dokument uprawniający do prowadzenia pojazdów mechanicznych.",
                "issuer": "Starostwo powiatowe",
                "renewal_process": "Wymaga złożenia wniosku i aktualnego orzeczenia lekarskiego. Czas odnowienia: 1-2 tygodnie."
            },
            "ubezpieczenie": {
                "type": "Polisa ubezpieczeniowa",
                "fields": ["Ubezpieczający", "Ubezpieczony", "Przedmiot ubezpieczenia", "Suma ubezpieczenia", "Składka",
                           "Data rozpoczęcia", "Data zakończenia"],
                "content": "Umowa ubezpieczenia zawarta pomiędzy ubezpieczającym a ubezpieczycielem.",
                "issuer": "Towarzystwo ubezpieczeniowe",
                "renewal_process": "Wymaga kontaktu z agentem ubezpieczeniowym. Czas odnowienia: 1-3 dni."
            },
            "certyfikat": {
                "type": "Certyfikat",
                "fields": ["Nazwa certyfikatu", "Posiadacz", "Zakres uprawnień", "Data wydania", "Data ważności"],
                "content": "Dokument potwierdzający określone kwalifikacje lub uprawnienia.",
                "issuer": "Instytucja certyfikująca",
                "renewal_process": "Może wymagać ponownego szkolenia i egzaminu. Czas odnowienia: zależny od rodzaju certyfikatu."
            },
            "umowa": {
                "type": "Umowa",
                "fields": ["Strony umowy", "Przedmiot umowy", "Wartość umowy", "Data zawarcia", "Data zakończenia"],
                "content": "Dokument zawierający porozumienie stron dotyczące określonych praw i obowiązków.",
                "issuer": "Strony umowy",
                "renewal_process": "Wymaga renegocjacji warunków i podpisania aneksu lub nowej umowy. Czas odnowienia: zależny od stron."
            }
        }

        # Ustalenie typu dokumentu na podstawie nazwy
        doc_type = None
        for key in document_types.keys():
            if key in doc_name:
                doc_type = document_types[key]
                break

        # Jeśli nie znaleziono pasującego typu, użyj domyślnego
        if not doc_type:
            doc_type = {
                "type": "Dokument urzędowy",
                "fields": ["Wydawca", "Posiadacz", "Data wydania", "Data ważności"],
                "content": "Dokument o charakterze urzędowym.",
                "issuer": "Urząd administracji publicznej",
                "renewal_process": "Wymaga złożenia wniosku w odpowiednim urzędzie. Czas odnowienia: 2-3 tygodnie."
            }

        # Dodaj informacje o rozmiarze pliku
        file_size_str = ""
        if hasattr(document, 'size') and document.size:
            if document.size < 1024:
                file_size_str = f"{document.size} B"
            elif document.size < 1024 * 1024:
                file_size_str = f"{document.size / 1024:.1f} KB"
            else:
                file_size_str = f"{document.size / (1024 * 1024):.1f} MB"

        # Dodaj informacje o formacie pliku
        file_format = "PDF"
        if document.mime_type:
            if "image" in document.mime_type:
                file_format = "Obraz (JPEG/PNG)"
            elif "word" in document.mime_type or "docx" in document.mime_type:
                file_format = "Microsoft Word"
            elif "excel" in document.mime_type or "xlsx" in document.mime_type:
                file_format = "Microsoft Excel"
            elif "pdf" in document.mime_type:
                file_format = "PDF"

        # Zwróć skompletowane informacje
        return {
            "document_name": document.name,
            "document_type": doc_type["type"],
            "file_format": file_format,
            "file_size": file_size_str,
            "fields": doc_type["fields"],
            "content_description": doc_type["content"],
            "issuer": doc_type["issuer"],
            "expiration_date": document.expiration_date.strftime(
                "%d.%m.%Y") if document.expiration_date else "Nieznana",
            "renewal_process": doc_type["renewal_process"]
        }

    def create_document_analysis_crew(self, document_id):
        """
        Analizuje dokument i jego zawartość.

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
            time.sleep(1.5)

            # Ekstrakcja "zawartości" dokumentu
            doc_content = self._extract_document_content(document)

            # Obliczenia na podstawie daty wygaśnięcia
            current_date = datetime.now(pytz.UTC)
            days_left = (document.expiration_date - current_date).days if document.expiration_date else 30

            # Określenie priorytetu odnowienia
            if days_left <= 14:
                priority = "KRYTYCZNY"
                priority_desc = "Dokument wymaga natychmiastowego odnowienia! Istnieje wysokie ryzyko przekroczenia terminu ważności."
            elif days_left <= 30:
                priority = "WYSOKI"
                priority_desc = "Dokument wymaga szybkiego odnowienia. Zalecamy rozpoczęcie procedury w najbliższych dniach."
            elif days_left <= 60:
                priority = "ŚREDNI"
                priority_desc = "Zalecamy zaplanowanie odnowienia dokumentu w najbliższych tygodniach."
            else:
                priority = "NISKI"
                priority_desc = "Dokument zachowuje ważność przez dłuższy czas. Możesz zaplanować jego odnowienie z wyprzedzeniem."

            # Generowanie rekomendacji na podstawie typu dokumentu
            recommendations = [
                f"Przygotuj wymagane dokumenty do odnowienia {doc_content['document_type']} z wyprzedzeniem",
                f"Sprawdź aktualne procedury odnowienia w {doc_content['issuer']}"
            ]

            if days_left <= 30:
                recommendations.append("Zarezerwuj termin wizyty w urzędzie jak najszybciej")
                recommendations.append("Przygotuj alternatywne dokumenty tożsamości na czas procesu odnowienia")

            if "Dowód osobisty" in doc_content['document_type'] or "Paszport" in doc_content['document_type']:
                recommendations.append("Zrób aktualne zdjęcie zgodne z wymogami biometrycznymi")

            if "Prawo jazdy" in doc_content['document_type']:
                recommendations.append(
                    "Uzyskaj aktualne orzeczenie lekarskie o braku przeciwwskazań do prowadzenia pojazdów")

            if "Polisa" in doc_content['document_type'] or "Ubezpieczenie" in doc_content['document_type']:
                recommendations.append("Porównaj oferty różnych ubezpieczycieli przed odnowieniem")

            # Formatowanie wyniku analizy
            fields_list = '\n'.join([f"  - {field}" for field in doc_content['fields']])

            result = (
                f"*Analiza dokumentu: {document.name}*\n\n"
                f"📄 *Typ dokumentu:* {doc_content['document_type']}\n"
                f"📊 *Priorytet odnowienia:* {priority}\n"
                f"⏱️ *Pozostały czas:* {days_left} dni\n"
                f"📅 *Data wygaśnięcia:* {doc_content['expiration_date']}\n"
                f"🔍 *Format pliku:* {doc_content['file_format']}\n"
                f"📦 *Rozmiar pliku:* {doc_content['file_size']}\n\n"

                f"*Zawartość dokumentu:*\n{doc_content['content_description']}\n\n"

                f"*Pola dokumentu:*\n{fields_list}\n\n"

                f"*Ocena priorytetu:*\n{priority_desc}\n\n"

                f"*Proces odnowienia:*\n{doc_content['renewal_process']}\n\n"

                f"*Rekomendowane działania:*\n"
            )

            for i, rec in enumerate(recommendations, 1):
                result += f"{i}. {rec}\n"

            logger.info(f"Wygenerowano analizę zawartości dla dokumentu {document_id}")
            return result

        except Exception as e:
            logger.error(f"Błąd podczas analizy dokumentu: {e}")
            return f"Wystąpił błąd podczas analizy: {str(e)}"
        finally:
            db.close()

    async def generate_custom_reminder(self, user_id, document_id, reminder_type):
        """
        Generuje spersonalizowane przypomnienie dla użytkownika na podstawie analizy dokumentu.

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

            # Pobieramy "zawartość" dokumentu
            doc_content = self._extract_document_content(document)

            # Obliczenia na podstawie daty wygaśnięcia
            current_date = datetime.now(pytz.UTC)
            days_left = (document.expiration_date - current_date).days if document.expiration_date else 30

            # Tworzenie spersonalizowanego przypomnienia w zależności od typu dokumentu i kanału
            if reminder_type == 'telegram':
                if days_left <= 14:
                    return (
                        f"⚠️ *PILNE PRZYPOMNIENIE* ⚠️\n\n"
                        f"Witaj {user.first_name},\n\n"
                        f"Twój dokument *{document.name}* ({doc_content['document_type']}) wygaśnie za {days_left} dni!\n\n"
                        f"*Zalecane natychmiastowe działania:*\n"
                        f"1. Zarezerwuj termin w {doc_content['issuer']}\n"
                        f"2. Przygotuj wymagane dokumenty\n"
                        f"3. {doc_content['renewal_process'].split('.')[0]}\n\n"
                        f"Nie odkładaj tego na później!"
                    )
                else:
                    return (
                        f"📢 *Przypomnienie o odnowieniu dokumentu* 📢\n\n"
                        f"Witaj {user.first_name},\n\n"
                        f"Informujemy, że Twój dokument *{document.name}* ({doc_content['document_type']}) "
                        f"wygaśnie dnia {document.expiration_date.strftime('%d.%m.%Y')} (za {days_left} dni).\n\n"
                        f"Zalecamy zaplanowanie jego odnowienia z wyprzedzeniem.\n\n"
                        f"*Proces odnowienia:*\n{doc_content['renewal_process']}\n\n"
                        f"Dziękujemy za korzystanie z naszego systemu przypominania!"
                    )
            elif reminder_type == 'sms':
                if days_left <= 14:
                    return (
                        f"PILNE: Twoj dokument {document.name} wygasa za {days_left} dni! "
                        f"Natychmiast rozpocznij proces odnowienia w {doc_content['issuer']}."
                    )
                else:
                    return (
                        f"Przypomnienie: {doc_content['document_type']} '{document.name}' wygasa "
                        f"{document.expiration_date.strftime('%d.%m.%Y')}. Zaplanuj odnowienie."
                    )
            elif reminder_type == 'voice':
                if days_left <= 14:
                    return (
                        f"Dzień dobry, {user.first_name}. To pilne automatyczne przypomnienie. "
                        f"Twój dokument {document.name} wygaśnie za {days_left} dni. "
                        f"Zalecamy natychmiastowe rozpoczęcie procesu odnowienia w {doc_content['issuer']}. "
                        f"Dziękuję za uwagę."
                    )
                else:
                    return (
                        f"Dzień dobry, {user.first_name}. Dzwonimy przypomnieć, że Twój dokument {document.name} "
                        f"typu {doc_content['document_type']} wygaśnie dnia {document.expiration_date.strftime('%d %B %Y')}. "
                        f"Zalecamy zaplanowanie odnowienia. Proces odnowienia wymaga {doc_content['renewal_process'].split('.')[0].lower()}. "
                        f"Dziękujemy za uwagę."
                    )

            return f"Przypomnienie: Dokument '{document.name}' wygasa {document.expiration_date.strftime('%d.%m.%Y')}."

        except Exception as e:
            logger.error(f"Błąd podczas generowania przypomnienia: {e}")
            return None
        finally:
            db.close()
