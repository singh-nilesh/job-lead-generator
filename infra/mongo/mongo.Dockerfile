FROM mongo:6.0

# Install envsubst
RUN apt-get update && apt-get install -y gettext && rm -rf /var/lib/apt/lists/*

# Copy init files
COPY ./init /docker-entrypoint-initdb.d/

# Make script executable
RUN chmod +x /docker-entrypoint-initdb.d/*.sh && \
    touch /docker-entrypoint-initdb.d/99-init.js && \
    chmod 666 /docker-entrypoint-initdb.d/99-init.js

