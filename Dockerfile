# Use the official PostgreSQL 17 image as the base image
FROM postgres:17

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-17

# Clone and install pgvector
RUN git clone https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && \
    make install

# Clean up
RUN apt-get remove -y build-essential git postgresql-server-dev-17 && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /pgvector

# Set environment variables
ENV POSTGRES_DB=mydb
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword

# Copy initialization scripts
COPY ./init.sql /docker-entrypoint-initdb.d/

# Verify init.sql is copied
RUN ls -la /docker-entrypoint-initdb.d/

# Expose the PostgreSQL port
EXPOSE 5432

# Set the default command to run when starting the container
CMD ["postgres"]