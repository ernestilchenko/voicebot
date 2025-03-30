from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bot.config import DB_URL

# Utworzenie silnika bazodanowego
engine = create_engine(DB_URL)

# Tworzenie sesji
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Bazowa klasa dla modeli ORM
Base = declarative_base()


# Funkcja pomocnicza do uzyskania sesji DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
