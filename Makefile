.PHONY: app install db docker-dev docker

VENV = .venv
PYTHON = $(VENV)/bin/python
dotenv = env $(shell cat .env | xargs)

install:
	@test -d api/$(VENV) || python3 -m venv api/$(VENV)
	api/$(PYTHON) -m ensurepip --upgrade
	api/$(PYTHON) -m pip install --upgrade pip
	api/$(PYTHON) -m pip install -r api/requirements.txt
	cd cardMakerFE && npm install
	@if [ ! -f package.json ]; then npm init -y; fi
	npm install --save-dev concurrently

db:
	@if docker ps -a --format '{{.Names}}' | grep -q '^db$$'; then \
		echo "▶️  DB container exists."; \
		if ! docker ps --format '{{.Names}}' | grep -q '^db$$'; then \
			echo "⏯️  Starting existing DB container..."; \
			docker start db; \
		else \
			echo "✅ DB is already running."; \
		fi \
	else \
		echo "📦 DB container not found. Pulling and starting..."; \
		docker-compose -f docker-compose-dev.yml up -d --build db; \
	fi

	@echo "⏳ Waiting for DB to become healthy..."
	@sleep 10

	@echo "🛠️  Initializing DB via create_db()"
	cd api && bash -c "set -a && source ../.env && .venv/bin/python -c 'from create_db import create_db; create_db()'"

app: db
	@echo "🚀 Starting app with concurrently..."
	npx concurrently \
		--names "API,FRONTEND" \
		--prefix-colors "blue,magenta" \
		"cd api && $(PYTHON) main.py" \
		"cd cardMakerFE && npm run dev"

docker-dev:
	docker-compose -f docker-compose-dev.yml up -d
	cd cardMakerFE && npm run dev

docker:
	docker-compose up -d
