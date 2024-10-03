import psycopg2
from config.settings import env


def get_db_connection():
    """
    Connect to the PostgreSQL database and return the connection object
    """

    # Check if the required environment variables are set
    if (
        not env.PG_VECTOR_DB_USER
        or not env.PG_VECTOR_DB_PASSWORD
        or not env.PG_VECTOR_DB
        or not env.PG_VECTOR_DB_PORT
        or not env.PG_VECTOR_DB_HOST
    ):
        raise ValueError("One or more required DB environment variables are not set.")

    try:
        connection = psycopg2.connect(
            user=env.PG_VECTOR_DB_USER,
            password=env.PG_VECTOR_DB_PASSWORD,
            dbname=env.PG_VECTOR_DB,
            port=env.PG_VECTOR_DB_PORT,
            host=env.PG_VECTOR_DB_HOST,
        )
        return connection

    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise
