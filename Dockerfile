FROM python:3.12-slim

WORKDIR /app

# Instalacja zależności systemowych potrzebnych do niektórych pakietów Pythona
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie plików requirements
COPY requirements.txt .

# Instalacja zależności Python
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu aplikacji
COPY . .

# Zmienne środowiskowe można przekazać z docker-compose lub podczas uruchamiania
# lub załadować z pliku .env wewnątrz kontenera
ENV PYTHONPATH=/app

# Uruchamianie bota
CMD ["python", "bot.py"]