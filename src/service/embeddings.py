from database.postgres import get_db_connection
from genai.gemini import genai_model


# Function to check if a similar sentence exists with a distance less than 0.1
def sentence_exists(query_sentence) -> tuple[bool, str, str]:
    """
    Check if a similar sentence exists in the database with a distance less than 0.1
    :param query_sentence: The sentence to check
    :return: A tuple (exists, phrase) where exists is a boolean indicating if the sentence exists
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Generate the embedding for the query sentence
        query_embedding = genai_model.embed_documents([query_sentence])[
            0
        ]  # Get the embedding as a list
        query_embedding_str = ",".join(map(str, query_embedding))
        query_embedding_literal = f"[{query_embedding_str}]"

        # SQL query to find similar sentences
        sql_query = """
            SELECT phrase, hash, embedding <=> %s::vector AS distance
            FROM new_embedding
            ORDER BY distance
            LIMIT 1;
        """

        cursor.execute(sql_query, (query_embedding_literal,))
        result = cursor.fetchone()  # (phrase, hash, distance)
        print(result)
        if result:
            phrase, hash, distance = result
            if distance < 0.1:
                return True, phrase, hash  # Sentence exists
        return False, None, None  # Sentence doesn't exist
    except Exception as e:
        print(f"Error in sentence_exists: {e}")
        return False, None, None
    finally:
        cursor.close()
        connection.close()


# Function to add a new sentence to the database
def add_sentence(hash: str, sentence: str, embedding):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Convert embedding to string in the format 'x1, x2, ...'
        embedding_str = ",".join(map(str, embedding))
        embedding_literal = (
            f"[{embedding_str}]"  # Ensure it starts and ends with brackets
        )

        # SQL query to insert the new sentence
        insert_query = """
        INSERT INTO new_embedding (phrase, hash, embedding)
        VALUES (%s, %s, %s::vector);
        """
        cursor.execute(insert_query, (sentence, hash, embedding_literal))
        connection.commit()
    except Exception as e:
        print(f"Error in add_sentence: {e}")
        raise
    finally:
        cursor.close()
        connection.close()


def remove_sentence(hash: str):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # SQL query to remove the sentence
        delete_query = """
            DELETE FROM new_embedding
            WHERE hash = %s;
        """
        cursor.execute(delete_query, (hash,))
        connection.commit()
    except Exception as e:
        print(f"Error in remove_sentence: {e}")
        raise
    finally:
        cursor.close()
        connection.close()  # Close the connection
