import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

import openai
import pytz
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

from bot.config import OPENAI_API_KEY
from bot.data import document_types
from webapp.database import SessionLocal
from webapp.models import User, Document

logger = logging.getLogger(__name__)


class CrewManager:
    """
    Implementacja menedżera Crew AI do analizy dokumentów i ich zawartości.
    Obsługuje zaawansowane analizy dokumentów przy użyciu zespołu specjalistycznych agentów AI.
    """

    def __init__(self, api_key=None):
        """
        Inicjalizacja menedżera.

        Args:
            api_key: Klucz API OpenAI
        """
        self.api_key = api_key or OPENAI_API_KEY
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,
            api_key=self.api_key,
            max_tokens=4000
        )
        logger.info("Zainicjalizowano CrewManager z funkcją analizy dokumentów i integracją Crew AI")

    def _determine_document_type_with_ai(self, document_name):
        """
        Używa OpenAI API do określenia typu dokumentu na podstawie jego nazwy.

        Args:
            document_name: Nazwa dokumentu

        Returns:
            dict: Informacje o dokumencie
        """
        client = openai.OpenAI(api_key=self.api_key)

        prompt = f"""
        Na podstawie nazwy dokumentu: "{document_name}", określ:
        1. Typ dokumentu (po polsku)
        2. Listę pól, które typowo zawiera ten dokument (po polsku)
        3. Krótki opis zawartości dokumentu (po polsku)
        4. Kto jest typowym wystawcą tego dokumentu (po polsku)
        5. Jak wygląda proces odnowienia tego dokumentu (po polsku)

        Zwróć odpowiedź w formacie JSON, dokładnie według poniższej struktury:
        {{
            "type": "typ dokumentu",
            "fields": ["pole1", "pole2", "pole3", ...],
            "content": "opis zawartości dokumentu",
            "issuer": "wystawca dokumentu",
            "renewal_process": "proces odnowienia dokumentu"
        }}
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # lub inny dostępny model
                messages=[
                    {"role": "system",
                     "content": "Jesteś ekspertem od polskich dokumentów urzędowych i identyfikacyjnych. Odpowiadasz tylko w języku polskim i zawsze w formacie JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Niższa temperatura dla bardziej przewidywalnych odpowiedzi
                response_format={"type": "json_object"}
            )

            # Parsowanie odpowiedzi JSON
            result = json.loads(response.choices[0].message.content)

            # Upewnij się, że mamy wszystkie potrzebne pola
            required_fields = ["type", "fields", "content", "issuer", "renewal_process"]
            for field in required_fields:
                if field not in result:
                    if field == "fields":
                        result[field] = ["Nazwa", "Data wydania", "Data ważności"]
                    else:
                        result[field] = "Brak informacji"

            logger.info(f"AI określiło typ dokumentu: {result['type']}")
            return result

        except Exception as e:
            logger.error(f"Błąd podczas określania typu dokumentu przez AI: {e}")
            # Domyślna struktura w przypadku błędu
            return {
                "type": "Dokument urzędowy",
                "fields": ["Wydawca", "Posiadacz", "Data wydania", "Data ważności"],
                "content": "Dokument o charakterze urzędowym.",
                "issuer": "Urząd administracji publicznej",
                "renewal_process": "Wymaga złożenia wniosku w odpowiednim urzędzie. Czas odnowienia: 2-3 tygodnie."
            }

    def _extract_document_content(self, document):
        """
        Ekstrahuje zawartość dokumentu na podstawie jego metadanych.
        Jeśli nie może znaleźć typu dokumentu w słowniku, używa OpenAI API
        do automatycznego określenia typu dokumentu.

        Args:
            document: Obiekt dokumentu z bazy danych

        Returns:
            dict: Zawartość dokumentu
        """
        # Symulowanie zawartości na podstawie nazwy dokumentu
        doc_name = document.name.lower() if document.name else "dokument"

        # Ustalenie typu dokumentu na podstawie nazwy
        doc_type = None
        for key in document_types.keys():
            if key in doc_name:
                doc_type = document_types[key]
                break

        # Jeśli nie znaleziono pasującego typu, użyj OpenAI API
        if not doc_type:
            try:
                doc_type = self._determine_document_type_with_ai(doc_name)
                logger.info(f"Użyto AI do określenia typu dokumentu '{doc_name}'")
            except Exception as e:
                logger.error(f"Błąd podczas określania typu dokumentu przez AI: {e}")
                # Fallback jeśli AI zawiedzie
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
        Analizuje dokument i jego zawartość przy użyciu zespołu specjalistów Crew AI.

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

            # Ekstrakcja "zawartości" dokumentu
            doc_content = self._extract_document_content(document)

            # Obliczenia na podstawie daty wygaśnięcia
            current_date = datetime.now(pytz.UTC)
            days_left = (document.expiration_date - current_date).days if document.expiration_date else 30

            # Tworzenie zespołu agentów Crew AI do analizy dokumentu
            try:
                # Agent specjalista od dokumentów
                document_expert = Agent(
                    role="Ekspert ds. Dokumentów",
                    goal="Analizować dokumenty urzędowe i identyfikować ich typ, zawartość oraz wymogi prawne",
                    backstory="""
                    Jesteś ekspertem od polskich dokumentów urzędowych z wieloletnim doświadczeniem w administracji publicznej.
                    Twoja specjalizacja to identyfikacja typów dokumentów, analiza ich zawartości oraz doradztwo w kwestii procedur
                    administracyjnych związanych z ich odnowieniem.
                    """,
                    allow_delegation=True,
                    verbose=True,
                    llm=self.llm,
                    max_iterations=2
                )

                # Agent specjalista od procedur prawno-administracyjnych
                legal_expert = Agent(
                    role="Ekspert Prawny",
                    goal="Doradzać w kwestiach prawnych związanych z dokumentami i procedurami urzędowymi",
                    backstory="""
                    Jesteś prawnikiem specjalizującym się w prawie administracyjnym w Polsce.
                    Posiadasz dogłębną wiedzę na temat procedur administracyjnych, terminów,
                    wymagań formalnych oraz konsekwencji prawnych związanych z dokumentami urzędowymi.
                    """,
                    allow_delegation=True,
                    verbose=True,
                    llm=self.llm,
                    max_iterations=2
                )

                # Agent ds. terminów i powiadomień
                reminder_expert = Agent(
                    role="Specjalista ds. Terminów",
                    goal="Analizować terminy ważności dokumentów i rekomendować optymalny harmonogram odnowienia",
                    backstory="""
                    Jesteś ekspertem od zarządzania terminami ważności dokumentów. Twoja specjalność
                    to analiza czasowa, planowanie wyprzedzające oraz optymalizacja procesów odnowienia dokumentów.
                    Doradzasz, kiedy najlepiej rozpocząć proces odnawiania i jakie kroki podjąć w jakim terminie.
                    """,
                    allow_delegation=True,
                    verbose=True,
                    llm=self.llm,
                    max_iterations=2
                )

                # Zadania dla agentów
                document_analysis_task = Task(
                    description=f"""
                    Przeprowadź szczegółową analizę dokumentu: {document.name}

                    Informacje o dokumencie:
                    - Typ dokumentu: {doc_content['document_type']}
                    - Format pliku: {doc_content['file_format']}
                    - Rozmiar pliku: {doc_content['file_size']}
                    - Data ważności: {doc_content['expiration_date']}

                    Zadanie:
                    1. Zidentyfikuj dokładny typ dokumentu i jego znaczenie prawne
                    2. Określ, jakie informacje zawiera ten dokument
                    3. Ustal typowego wystawcę tego dokumentu i jego rolę
                    4. Oceń konsekwencje związane z wygaśnięciem tego dokumentu

                    Przedstaw swoją analizę w języku polskim, w sposób zwięzły i przystępny.
                    Używaj profesjonalnego słownictwa administracyjnego.
                    """,
                    agent=document_expert,
                    expected_output="Szczegółowa analiza dokumentu w języku polskim, zawierająca jego typ, znaczenie, zawartość i konsekwencje wygaśnięcia."
                )

                legal_analysis_task = Task(
                    description=f"""
                    Przeprowadź analizę prawno-administracyjną dokumentu: {document.name}

                    Informacje o dokumencie:
                    - Typ dokumentu: {doc_content['document_type']}
                    - Typowy wystawca: {doc_content['issuer']}
                    - Data ważności: {doc_content['expiration_date']}
                    - Pozostało dni: {days_left}

                    Zadanie:
                    1. Określ prawne konsekwencje wygaśnięcia tego dokumentu
                    2. Zidentyfikuj procedury administracyjne konieczne do jego odnowienia
                    3. Wskaż podstawy prawne dotyczące tego typu dokumentu
                    4. Przedstaw potencjalne komplikacje prawne i jak ich uniknąć

                    Przedstaw swoją analizę prawną w języku polskim, w sposób zrozumiały dla osoby bez wykształcenia prawniczego.
                    """,
                    agent=legal_expert,
                    expected_output="Analiza prawna w języku polskim, zawierająca procedury odnowienia, konsekwencje prawne i zalecenia."
                )

                reminder_analysis_task = Task(
                    description=f"""
                    Przeanalizuj harmonogram odnowienia dokumentu: {document.name}

                    Informacje o dokumencie:
                    - Typ dokumentu: {doc_content['document_type']}
                    - Data ważności: {doc_content['expiration_date']}
                    - Pozostało dni: {days_left}
                    - Proces odnowienia: {doc_content['renewal_process']}

                    Zadanie:
                    1. Określ optymalny harmonogram działań związanych z odnowieniem dokumentu
                    2. Zaproponuj konkretne daty rozpoczęcia procesu odnowienia
                    3. Zidentyfikuj potencjalne opóźnienia w procesie i jak im zapobiec
                    4. Wskaż, jakie dokumenty i materiały należy przygotować i kiedy

                    Stwórz plan działania w języku polskim, z konkretnymi datami i krokami do wykonania.
                    """,
                    agent=reminder_expert,
                    expected_output="Harmonogram odnowienia dokumentu w języku polskim, z konkretnymi datami i rekomendacjami."
                )

                # Tworzenie zespołu Crew AI
                document_crew = Crew(
                    agents=[document_expert, legal_expert, reminder_expert],
                    tasks=[document_analysis_task, legal_analysis_task, reminder_analysis_task],
                    verbose=2,
                    process=Process.sequential
                )

                # Uruchomienie analizy
                result = document_crew.kickoff()

                # Jeśli mamy pełny wynik z Crew AI, używamy go
                if result and isinstance(result, list) and len(result) >= 3:
                    document_analysis = result[0]
                    legal_analysis = result[1]
                    reminder_analysis = result[2]

                    formatted_result = f"""
*ANALIZA DOKUMENTU: {document.name}*

📄 *Typ dokumentu:* {doc_content['document_type']}
⏱️ *Pozostały czas:* {days_left} dni
📅 *Data wygaśnięcia:* {doc_content['expiration_date']}

*ANALIZA EKSPERTA DS. DOKUMENTÓW:*
{document_analysis}

*ANALIZA PRAWNA:*
{legal_analysis}

*HARMONOGRAM ODNOWIENIA:*
{reminder_analysis}
"""
                    logger.info(f"Wygenerowano kompletną analizę zespołu Crew AI dla dokumentu {document_id}")
                    return formatted_result

                # Fallback na uproszczoną analizę, jeśli Crew AI nie zwróciło pełnych wyników
                logger.warning("Nie uzyskano pełnych wyników z Crew AI, używam analizy zapasowej")

            except Exception as e:
                logger.error(f"Błąd podczas analizy dokumentu z Crew AI: {e}")
                logger.info("Przechodzę do analizy zapasowej bez Crew AI")

            # Analiza zapasowa, jeśli Crew AI zawiedzie
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
        Używa zespołu Crew AI do stworzenia spersonalizowanej wiadomości.

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

            # Próba użycia CrewAI do stworzenia spersonalizowanej wiadomości
            try:
                # Agent specjalizujący się w komunikacji
                communication_expert = Agent(
                    role="Specjalista ds. Komunikacji",
                    goal="Tworzyć skuteczne, personalizowane wiadomości przypominające",
                    backstory="""
                    Jesteś ekspertem od komunikacji z wieloletnim doświadczeniem w tworzeniu skutecznych
                    wiadomości przypominających. Potrafisz dostosować ton, styl i treść wiadomości
                    do różnych kanałów komunikacji oraz pilności sprawy. Twoje wiadomości są jasne,
                    zwięzłe i motywujące do działania.
                    """,
                    verbose=True,
                    llm=self.llm
                )

                # Zadanie dla agenta komunikacji
                reminder_task = Task(
                    description=f"""
                    Przygotuj spersonalizowaną wiadomość przypominającą o wygasającym dokumencie.

                    Informacje o użytkowniku:
                    - Imię: {user.first_name}
                    - Nazwisko: {user.last_name if user.last_name else ''}

                    Informacje o dokumencie:
                    - Nazwa dokumentu: {document.name}
                    - Typ dokumentu: {doc_content['document_type']}
                    - Data wygaśnięcia: {doc_content['expiration_date']}
                    - Pozostało dni: {days_left}
                    - Proces odnowienia: {doc_content['renewal_process']}

                    Kanał komunikacji: {reminder_type.upper()}

                    Wytyczne:
                    - Jeśli kanał to 'telegram': Stwórz pełną wiadomość z formatowaniem Markdown, emotikonami i szczegółami
                    - Jeśli kanał to 'sms': Stwórz krótką (max 160 znaków), zwięzłą wiadomość bez formatowania
                    - Jeśli kanał to 'voice': Stwórz tekst do odczytania przez syntezator mowy, używaj naturalnego języka mówionego

                    Wiadomość powinna:
                    - Być w języku polskim
                    - Zawierać jasne przypomnienie o terminie ważności
                    - Sugerować następne kroki do podjęcia
                    - Mieć odpowiedni ton (pilny dla terminów < 30 dni, informacyjny dla dłuższych)

                    Zwróć TYLKO treść wiadomości, bez dodatkowych komentarzy czy metadanych.
                    """,
                    agent=communication_expert,
                    expected_output="Spersonalizowana wiadomość przypominająca w języku polskim"
                )

                # Tworzenie jednoosobowego zespołu do generowania wiadomości
                reminder_crew = Crew(
                    agents=[communication_expert],
                    tasks=[reminder_task],
                    verbose=1,
                    process=Process.sequential
                )

                # Uruchomienie generowania wiadomości
                message = reminder_crew.kickoff()

                if message and isinstance(message, str) and len(message) > 10:
                    logger.info(f"Wygenerowano spersonalizowaną wiadomość CrewAI dla dokumentu {document_id}")
                    return message

                logger.warning("Nie uzyskano poprawnej wiadomości z CrewAI, używam szablonu zastępczego")

            except Exception as e:
                logger.error(f"Błąd podczas generowania wiadomości z CrewAI: {e}")
                logger.info("Przechodzę do generowania szablonowego")

            # Tworzenie spersonalizowanego przypomnienia w zależności od typu dokumentu i kanału (fallback)
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

    async def generate_document_report(self, user_id):
        """
        Generuje raport o wszystkich dokumentach użytkownika z zaleceniami.

        Args:
            user_id: ID użytkownika

        Returns:
            str: Raport o dokumentach
        """
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return "Nie znaleziono użytkownika"

            documents = db.query(Document).filter(Document.user_id == user_id).all()
            if not documents:
                return "Nie znaleziono dokumentów dla tego użytkownika"

            # Przygotowanie danych o dokumentach dla Crew AI
            docs_data = []
            current_date = datetime.now(pytz.UTC)

            for doc in documents:
                if doc.expiration_date:
                    days_left = (doc.expiration_date - current_date).days
                    docs_data.append({
                        "name": doc.name,
                        "type": self._extract_document_content(doc)["document_type"],
                        "expiration_date": doc.expiration_date.strftime("%d.%m.%Y"),
                        "days_left": days_left
                    })

            # Użycie Crew AI do wygenerowania raportu
            try:
                # Agent analityk dokumentów
                document_analyst = Agent(
                    role="Analityk Dokumentów",
                    goal="Analizować kolekcję dokumentów i tworzyć syntetyczne raporty z rekomendacjami",
                    backstory="""
                    Jesteś ekspertem analitykiem dokumentów specjalizującym się w zarządzaniu dokumentami
                    osobistymi i urzędowymi. Potrafisz analizować zbiory dokumentów, identyfikować priorytety,
                    wzorce i ryzyka. Twoje raporty są przejrzyste, wnikliwe i zawierają praktyczne rekomendacje.
                    """,
                    verbose=True,
                    llm=self.llm
                )

                # Zadanie dla analityka
                report_task = Task(
                    description=f"""
                    Przygotuj kompleksowy raport o wszystkich dokumentach użytkownika {user.first_name} {user.last_name if user.last_name else ''}.

                    Lista dokumentów:
                    {json.dumps(docs_data, indent=2, ensure_ascii=False)}

                    Zadanie:
                    1. Przeanalizuj wszystkie dokumenty i ich terminy ważności
                    2. Zidentyfikuj priorytety - dokumenty wymagające natychmiastowej uwagi
                    3. Zaproponuj harmonogram odnowień dokumentów
                    4. Wskaż potencjalne synergie (dokumenty, które można odnowić razem)
                    5. Przedstaw rekomendacje dotyczące zarządzania dokumentami

                    Raport powinien być w języku polskim, sformatowany w Markdown, z wyraźnymi sekcjami
                    i praktycznymi zaleceniami. Użyj emotikonów dla zwiększenia czytelności.
                    """,
                    agent=document_analyst,
                    expected_output="Kompleksowy raport o dokumentach użytkownika w języku polskim, w formacie Markdown"
                )

                # Tworzenie zespołu do generowania raportu
                report_crew = Crew(
                    agents=[document_analyst],
                    tasks=[report_task],
                    verbose=1,
                    process=Process.sequential
                )

                # Uruchomienie generowania raportu
                report = report_crew.kickoff()

                if report and isinstance(report, str) and len(report) > 100:
                    logger.info(f"Wygenerowano raport dokumentów dla użytkownika {user_id}")
                    return report

                logger.warning("Nie uzyskano poprawnego raportu z CrewAI, używam raportu zastępczego")

            except Exception as e:
                logger.error(f"Błąd podczas generowania raportu z CrewAI: {e}")

            # Raport zastępczy, jeśli CrewAI zawiedzie
            current_date = datetime.now(pytz.UTC)

            report = f"# Raport dokumentów dla {user.first_name} {user.last_name if user.last_name else ''}\n\n"

            # Kategorie priorytetów
            urgent_docs = []
            soon_docs = []
            later_docs = []

            for doc in documents:
                if not doc.expiration_date:
                    continue

                days_left = (doc.expiration_date - current_date).days

                if days_left <= 30:
                    urgent_docs.append((doc, days_left))
                elif days_left <= 90:
                    soon_docs.append((doc, days_left))
                else:
                    later_docs.append((doc, days_left))

            # Sekcja dokumentów pilnych
            if urgent_docs:
                report += "## ⚠️ Dokumenty wymagające natychmiastowej uwagi\n\n"
                for doc, days in sorted(urgent_docs, key=lambda x: x[1]):
                    doc_content = self._extract_document_content(doc)
                    report += f"* **{doc.name}** ({doc_content['document_type']})\n"
                    report += f"  * Wygasa za: **{days} dni** ({doc.expiration_date.strftime('%d.%m.%Y')})\n"
                    report += f"  * Zalecane działanie: Natychmiast rozpocznij proces odnowienia\n\n"

            # Sekcja dokumentów do odnowienia wkrótce
            if soon_docs:
                report += "## 🕒 Dokumenty do odnowienia w najbliższym czasie\n\n"
                for doc, days in sorted(soon_docs, key=lambda x: x[1]):
                    doc_content = self._extract_document_content(doc)
                    report += f"* **{doc.name}** ({doc_content['document_type']})\n"
                    report += f"  * Wygasa za: **{days} dni** ({doc.expiration_date.strftime('%d.%m.%Y')})\n"
                    report += f"  * Zalecane działanie: Zaplanuj odnowienie w kalendarzu\n\n"

            # Sekcja pozostałych dokumentów
            if later_docs:
                report += "## 📋 Pozostałe dokumenty\n\n"
                for doc, days in sorted(later_docs, key=lambda x: x[1]):
                    doc_content = self._extract_document_content(doc)
                    report += f"* **{doc.name}** ({doc_content['document_type']})\n"
                    report += f"  * Wygasa za: **{days} dni** ({doc.expiration_date.strftime('%d.%m.%Y')})\n\n"

            # Rekomendacje
            report += "## 💡 Rekomendacje\n\n"
            report += "1. Przygotuj dokumenty potrzebne do odnowienia z wyprzedzeniem\n"
            report += "2. Sprawdź aktualne procedury i wymogi w odpowiednich urzędach\n"
            report += "3. Rozważ odnowienie kilku dokumentów jednocześnie, jeśli to możliwe\n"
            report += "4. Ustaw przypomnienia w kalendarzu na 1-2 miesiące przed terminem wygaśnięcia\n"
            report += "5. Przechowuj kopie dokumentów w bezpiecznym miejscu\n"

            return report

        except Exception as e:
            logger.error(f"Błąd podczas generowania raportu dokumentów: {e}")
            return f"Wystąpił błąd podczas generowania raportu: {str(e)}"
        finally:
            db.close()

    async def translate_document_to_english(self, filename: str, save_to: str = None) -> str:
        """
        Tłumaczy dokument z języka polskiego na angielski z zachowaniem formatu Markdown.

        Funkcja wykorzystuje model GPT-4o do przetłumaczenia dokumentu na język angielski. Dokument
        przesyłany jest jako plik wejściowy do API OpenAI, a następnie tłumaczony zgodnie z określonymi
        zasadami (styl formalny, pełna zgodność merytoryczna, formatowanie Markdown).

        Args:
            filename (str): Ścieżka do pliku z dokumentem w języku polskim.
            save_to (str, optional): Ścieżka do pliku, do którego ma zostać zapisany wynik tłumaczenia (jeśli podana).

        Returns:
            str: Przetłumaczony tekst w języku angielskim w formacie Markdown lub komunikat o błędzie.
        """
        client = openai.OpenAI(api_key=self.api_key)
        try:
            file = client.files.create(
                file=open(filename, "rb"),
                purpose="user_data"
            )
        except Exception as e:
            print(f"[ERROR] Error openning file: {e}")
            return f"[ERROR] {e}"
        
        response = client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "file_id": file.id,
                        },
                        {
                            "type": "input_text",
                            "text": """Jesteś doświadczonym tłumaczem dokumentów specjalizującym się w tłumaczeniu formalnych
    i nieformalnych tekstów z języka polskiego na angielski. Dbasz o zachowanie kontekstu, tonu
    oraz formatu źródłowego dokumentu. Twoje tłumaczenia są przejrzyste, wierne oryginałowi,
    a wynikowy tekst sformatowany jest w stylu Markdown (nagłówki, listy, pogrubienia itd. gdzie to potrzebne).
    Przetłumacz poniższy dokument z języka polskiego na angielski.
    Zasady:
    - Zachowaj pełną zgodność merytoryczną.
    - Użyj formatu Markdown (np. # nagłówki, **pogrubienia**, *kursywa*, listy itd.).
    - Nie pomijaj żadnych fragmentów.
    - Styl ma być przejrzysty i profesjonalny.
    """
                        },                        
                    ]
                }
            ]
        )

        return response.output_text
