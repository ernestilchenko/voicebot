import logging
from crewai import Agent, Task, Crew, Process
from langchain.llms import OpenAI
from webapp.database import SessionLocal
from webapp.models import User, Document

logger = logging.getLogger(__name__)


class CrewManager:
    """
    Klasa zarządzająca zespołem agentów AI do wsparcia funkcji bota.
    """

    def __init__(self, api_key):
        """
        Inicjalizacja menedżera zespołu AI.

        Args:
            api_key: Klucz API do modelu języka (np. OpenAI)
        """
        self.llm = OpenAI(api_key=api_key)
        logger.info("Zainicjalizowano menedżera Crew AI")

    def create_document_analysis_crew(self, document_id):
        """
        Tworzy zespół AI do analizy dokumentu i generowania przypomnień.

        Args:
            document_id: ID dokumentu do analizy

        Returns:
            dict: Wyniki analizy dokumentu
        """
        db = SessionLocal()
        try:
            document = db.query(Document).filter(Document.id == document_id).first()
            user = db.query(User).filter(User.id == document.user_id).first()

            if not document or not user:
                logger.error(f"Nie znaleziono dokumentu lub użytkownika: document_id={document_id}")
                return None

            # Tworzenie agentów
            analyzer = Agent(
                role="Analityk Dokumentów",
                goal="Analizować dokumenty i określać optymalny harmonogram przypomnień",
                backstory="Jestem ekspertem w analizie dokumentów i tworzeniu harmonogramów przypomnień.",
                llm=self.llm
            )

            communicator = Agent(
                role="Specjalista Komunikacji",
                goal="Tworzyć spersonalizowane treści przypomnień dla różnych kanałów",
                backstory="Specjalizuję się w tworzeniu skutecznych wiadomości dla różnych kanałów komunikacji.",
                llm=self.llm
            )

            # Tworzenie zadań
            analysis_task = Task(
                description=f"Przeanalizuj dokument '{document.name}' dla użytkownika {user.first_name}. "
                            f"Dokument wygasa dnia {document.expiration_date}. "
                            f"Określ najlepszy harmonogram przypomnień.",
                agent=analyzer
            )

            communication_task = Task(
                description="Stwórz spersonalizowane treści przypomnień dla: 1) wiadomości Telegram, "
                            "2) wiadomości SMS, 3) skryptu połączenia głosowego. "
                            "Uwzględnij wyniki analizy.",
                agent=communicator,
                dependencies=[analysis_task]
            )

            # Tworzenie zespołu
            crew = Crew(
                agents=[analyzer, communicator],
                tasks=[analysis_task, communication_task],
                process=Process.sequential
            )

            # Uruchomienie zespołu
            results = crew.kickoff()

            logger.info(f"Zakończono analizę dokumentu {document_id} przez Crew AI")
            return results

        except Exception as e:
            logger.error(f"Błąd podczas analizy dokumentu przez Crew AI: {e}")
            return None
        finally:
            db.close()

    async def generate_custom_reminder(self, user_id, document_id, reminder_type):
        """
        Generuje spersonalizowane przypomnienie dla użytkownika.

        Args:
            user_id: ID użytkownika
            document_id: ID dokumentu
            reminder_type: Typ przypomnienia ('telegram', 'sms', 'voice')

        Returns:
            str: Spersonalizowana treść przypomnienia
        """
        db = SessionLocal()
        try:
            document = db.query(Document).filter(Document.id == document_id).first()
            user = db.query(User).filter(User.id == user_id).first()

            if not document or not user:
                return None

            # Agent do generowania przypomnień
            reminder_agent = Agent(
                role="Specjalista ds. Przypomnień",
                goal="Tworzyć skuteczne, spersonalizowane przypomnienia",
                backstory="Specjalizuję się w tworzeniu przypomnień, które skłaniają do działania.",
                llm=self.llm
            )

            # Zadanie
            reminder_task = Task(
                description=f"Stwórz spersonalizowane przypomnienie typu {reminder_type} dla użytkownika "
                            f"{user.first_name} dotyczące dokumentu '{document.name}', "
                            f"który wygasa {document.expiration_date}. "
                            f"Uwzględnij typ kanału komunikacji i dostosuj długość i ton wiadomości.",
                agent=reminder_agent
            )

            # Utworzenie prostego zespołu z jednym agentem
            crew = Crew(
                agents=[reminder_agent],
                tasks=[reminder_task],
                process=Process.sequential
            )

            # Wykonanie zadania
            result = crew.kickoff()

            return result

        except Exception as e:
            logger.error(f"Błąd podczas generowania przypomnienia przez Crew AI: {e}")
            return None
        finally:
            db.close()