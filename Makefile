.PHONY: help up down install-back install-front back front test lint migrate

help:            ## Liste des commandes
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-15s %s\n", $$1, $$2}'

up:              ## Démarre toute la stack (db + api + web)
	docker compose up -d --build

down:            ## Arrête la stack
	docker compose down

db:              ## Démarre uniquement PostgreSQL
	docker compose up -d db

install-back:    ## Installe le backend (uv)
	cd backend && uv sync --extra dev

install-front:   ## Installe le frontend
	cd frontend && npm install

back:            ## Lance l'API en mode dev
	cd backend && uv run uvicorn app.main:app --reload --port 8000

front:           ## Lance l'interface en mode dev
	cd frontend && npm run dev

migrate:         ## Applique les migrations
	cd backend && uv run alembic upgrade head

test:            ## Tests backend
	cd backend && uv run pytest

lint:            ## Lint backend
	cd backend && uv run ruff check app tests
