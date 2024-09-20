#!/bin/bash
set -e

# Install pgvector extension
echo "Installing pgvector extension..."

# Install necessary build tools
apt update
apt install -y postgresql-server-dev-14 build-essential

# Download and install pgvector
PGVECTOR_VERSION="0.5.2"
wget https://github.com/pgvector/pgvector/archive/refs/tags/${PGVECTOR_VERSION}.tar.gz
tar -xvf ${PGVECTOR_VERSION}.tar.gz
cd pgvector-${PGVECTOR_VERSION}
make && make install

# Clean up
cd ..
rm -rf pgvector-${PGVECTOR_VERSION} ${PGVECTOR_VERSION}.tar.gz

echo "pgvector extension installed successfully."

# Exit
exit 0
