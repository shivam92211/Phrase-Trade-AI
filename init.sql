-- Execute this command to create the database and table

-- Create the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with columns for phrase and embedding
CREATE TABLE IF NOT EXISTS new_embedding (
    id SERIAL PRIMARY KEY,
    phrase VARCHAR(521) NOT NULL,
    embedding VECTOR(768)  -- Adjust the dimension as needed
);