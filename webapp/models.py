from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, BigInteger, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from webapp.database import Base

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
    # Добавляем новые поля
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    telegram_reminder_sent = Column(Boolean, default=False)
    sms_reminder_sent = Column(Boolean, default=False)
    call_reminder_sent = Column(Boolean, default=False)

    # Relacja z użytkownikiem
    user = relationship("User", back_populates="documents")


class Statistic(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    message_count = Column(Integer, default=0)
    user_count = Column(Integer, default=0)
    document_count = Column(Integer, default=0)
    last_activity = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @classmethod
    def get_or_create(cls, db):
        """Pobierz istniejący rekord statystyk lub utwórz nowy, jeśli nie istnieje"""
        stats = db.query(cls).first()
        if not stats:
            stats = cls()
            db.add(stats)
            db.commit()
            db.refresh(stats)
        return stats
