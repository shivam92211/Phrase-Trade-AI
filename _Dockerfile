# Use the official PostgreSQL image
FROM postgres:latest

# Set environment variables (optional)
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=good
ENV POSTGRES_DB=vector_db

# Install required dependencies for vector extension
RUN apt-get update && apt-get install -y \
    postgresql-server-dev-all \
    build-essential \
    git

# Clone the vector extension repository
# RUN git clone https://github.com/tensorchord/pgvector.git /usr/src/pgvector
RUN git clone https://github.com/pgvector/pgvector.git /usr/src/pgvector


# Build and install the vector extension
RUN cd /usr/src/pgvector && \
    make && make install

# Run the PostgreSQL service
CMD ["postgres"]
