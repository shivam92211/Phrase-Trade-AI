import psycopg2
from config.settings import env


def get_db_connection():
    """
    Connect to the PostgreSQL database and return the connection object
    """

    # Check if the required environment variables are set
    if (
        not env.POSTGRES_USER
        or not env.POSTGRES_PASSWORD
        or not env.POSTGRES_DB
        or not env.POSTGRES_PORT
        or not env.POSTGRES_HOST
    ):
        raise ValueError("One or more required DB environment variables are not set.")

    try:
        connection = psycopg2.connect(
            user=env.POSTGRES_USER,
            password=env.POSTGRES_PASSWORD,
            dbname=env.POSTGRES_DB,
            port=env.POSTGRES_PORT,
            host=env.POSTGRES_HOST,
        )
        return connection

    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise
