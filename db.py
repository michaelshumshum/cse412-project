import os

import psycopg2

_CONNNECTION = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)

CURSOR = _CONNNECTION.cursor()


def create_tables() -> None:
    """Create tables in the database if the don't exist already."""
    return


def cleanup() -> None:
    """Close the database connection."""
    CURSOR.close()
    _CONNNECTION.close()
