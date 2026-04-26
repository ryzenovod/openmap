.PHONY: install run test lint format migrate seed ci

install:
	pip install -e .[dev]

run:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	ruff check app tests
	black --check app tests

format:
	ruff check --fix app tests
	black app tests

migrate:
	alembic upgrade head

seed:
	python -m app.scripts.seed

ci:
	python -m compileall app alembic tests
	$(MAKE) lint
	$(MAKE) test
