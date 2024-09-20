# Use the official PostgreSQL image as the base image
FROM postgres:14

# Set environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=great
ENV POSTGRES_DB=vector_db

# Install necessary build tools and pgvector
RUN apt-get update && \
    apt-get install -y postgresql-server-dev-14 build-essential wget && \
    wget https://github.com/pgvector/pgvector/archive/refs/tags/0.5.2.tar.gz && \
    tar -xvf 0.5.2.tar.gz && \
    cd pgvector-0.5.2 && \
    make && make install && \
    cd .. && \
    rm -rf pgvector-0.5.2 0.5.2.tar.gz && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy SQL and shell script files into the container
COPY init.sql /docker-entrypoint-initdb.d/
COPY init.sh /docker-entrypoint-initdb.d/

# Make sure init.sh is executable
RUN chmod +x /docker-entrypoint-initdb.d/init.sh

# Ensure the PostgreSQL database is set up
CMD ["docker-entrypoint.sh", "postgres"]
