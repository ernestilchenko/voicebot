# Zaktualizuj plik webapp/models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from webapp.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100), nullable=True)
    username = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacja z dokumentami
    documents = relationship("Document", back_populates="user")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    mime_type = Column(String(100), nullable=True)
    size = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Pola dotyczące daty ważności
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    telegram_reminder_sent = Column(Boolean, default=False)
    sms_reminder_sent = Column(Boolean, default=False)
    call_reminder_sent = Column(Boolean, default=False)
    # Dodatkowe pola do śledzenia połączeń głosowych
    call_attempts = Column(Integer, default=0)  # Liczba prób połączenia
    call_message_listened = Column(Boolean, default=False)  # Czy użytkownik odsłuchał wiadomość
    last_call_date = Column(DateTime(timezone=True), nullable=True)  # Data ostatniego połączenia

    # Nowe pole do przechowywania ścieżki do pliku w Google Cloud Storage
    gcs_file_path = Column(String(255), nullable=True)
    # Pole określające czy plik został pomyślnie przesłany do GCS
    gcs_uploaded = Column(Boolean, default=False)

    # Relacja z użytkownikiem
    user = relationship("User", back_populates="documents")
