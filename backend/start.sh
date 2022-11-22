#! /usr/bin/env bash
cd backend

# Let the DB start
# python3 -m app.create_database

# Run migrations
alembic -c alembic.ini upgrade head

# Start the backend server
uvicorn app.main:app --host 0.0.0.0 --port 8000
#exec gunicorn app.main:app -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --timeout 240