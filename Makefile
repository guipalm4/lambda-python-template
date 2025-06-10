.PHONY: help install test format clean deploy local

help: ## Mostra comandos
   @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências
	@echo "📦 Instalando..."
	pip install -r requirements.txt -r requirements-dev.txt

test: ## Executa testes
	@echo "🧪 Testando..."
	PYTHONPATH=. pytest tests/ -v --cov=src

format: ## Formata código
	@echo "🎨 Formatando..."
	black src/ tests/

clean: ## Limpa arquivos
	@echo "🧹 Limpando..."
	rm -rf .pytest_cache htmlcov .coverage __pycache__
	find . -name "__pycache__" -delete

deploy: ## Deploy na AWS
	@echo "🚀 Deploy..."
	sam build && sam deploy --guided

local: ## API local
	@echo "🌐 Iniciando local..."
	sam build && sam local start-api --port 3000