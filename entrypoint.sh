#!usr/bin/env bash

alembic revision --autogenerate -m "add tables"
alembic upgrade head
uvicorn --host 0.0.0.0 --port 8000 app.main:app