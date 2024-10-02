from src.database.postgres import get_db_connection


def create_required_tables():
    # check if vector extension is loaded
    # and table exists
    connection = get_db_connection()
    cursor = connection.cursor()

    # SQL query to find similar sentences
    sql_query = """
        -- Load vector extension if not loaded
        CREATE EXTENSION IF NOT EXISTS vector;

        -- Create table with columns for phrase and embedding
        CREATE TABLE IF NOT EXISTS new_embedding (
            id SERIAL PRIMARY KEY,
            phrase VARCHAR(512) NOT NULL,
            hash VARCHAR(64) NOT NULL,
            embedding VECTOR(768)  --Adjust the dimension as needed
        );    
        
        -- Create an index on the hash column
        CREATE INDEX IF NOT EXISTS idx_hash ON new_embedding(hash);
    """
    cursor.execute(sql_query)
    connection.commit()
    cursor.close()
    connection.close()
