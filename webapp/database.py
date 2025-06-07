from contextlib import contextmanager

import psycopg2

from bot.config import PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD

CONNECTION_STRING = f"host={PGHOST} port={PGPORT} dbname={PGDATABASE} user={PGUSER} password={PGPASSWORD}"


@contextmanager
def get_db():
    conn = psycopg2.connect(CONNECTION_STRING)
    try:
        yield conn
    finally:
        conn.close()


def get_db_connection():
    return psycopg2.connect(CONNECTION_STRING)
