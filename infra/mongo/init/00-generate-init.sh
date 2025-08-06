#!/bin/bash
echo "[INIT] Generating Mongo init script..."
envsubst < /docker-entrypoint-initdb.d/01-db-template.jstpl > /docker-entrypoint-initdb.d/99-init.js
echo "[INIT] Mongo init script generated successfully."