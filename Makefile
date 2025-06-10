.PHONY: help clean install test lint format deploy-dev deploy-prod

help:
	@echo "Available commands:"
	@echo "  make install        Install dependencies"
	@echo "  make install-dev    Install development dependencies"
	@echo "  make test           Run tests"
	@echo "  make lint           Run linters"
	@echo "  make format         Format code"
	@echo "  make clean          Clean build artifacts"
	@echo "  make build          Build SAM application"
	@echo "  make deploy-dev     Deploy to development"
	@echo "  make deploy-prod    Deploy to production"

clean:
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache
	rm -rf .aws-sam
	rm -rf __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

install:
	pip install -r requirements.txt

install-dev: install
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest tests/ --cov=src --cov-report=term-missing

lint:
	flake8 src tests
	mypy src
	bandit -r src/

format:
	isort src tests
	black src tests

build:
	sam build

deploy-dev:
	sam deploy --stack-name python-lambda-dev --parameter-overrides Environment=dev --no-confirm-changeset

deploy-prod:
	sam deploy --stack-name python-lambda-prod --parameter-overrides Environment=prod --no-confirm-changeset
