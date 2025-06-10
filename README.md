# 🚀 Lambda Python Template

Template **ultra simples** para AWS Lambda em Python com **logs estruturados** e **rastreabilidade completa**.

## 📋 Índice

- [🚀 Início Rápido](#-início-rápido)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [⚙️ Configuração](#️-configuração)
- [🧪 Desenvolvimento Local](#-desenvolvimento-local)
- [📊 Sistema de Logs](#-sistema-de-logs)
- [🔧 Features Opcionais](#-features-opcionais)
- [🚀 Deploy](#-deploy)
- [🔍 Troubleshooting](#-troubleshooting)
- [📖 Exemplos](#-exemplos)

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.12+
- AWS CLI configurado
- SAM CLI instalado

### Setup em 2 minutos

```bash
# 1. Clonar/baixar template
git clone <seu-repo> minha-lambda
cd minha-lambda

# 2. Instalar dependências
make install

# 3. Testar
make test

# 4. Executar localmente
make local
```

### Primeiro teste

```bash
# Em outro terminal
curl -X POST http://localhost:3000/test \
  -H "Content-Type: application/json" \
  -d '{"name": "João", "action": "teste"}'
```

## 📁 Estrutura do Projeto

```
lambda-python-template/
├── src/
│   ├── handler.py              # 🎯 Handler principal (SEU FOCO)
│   ├── handler_advanced.py     # 🚀 Handler com performance tracking
│   └── utils.py                # 🔧 Utilitários de log
├── tests/
│   └── test_handler.py         # 🧪 Testes unitários
├── events/                     # 📂 Eventos de teste (opcional)
├── requirements.txt            # 📦 Dependências de produção
├── requirements-dev.txt        # 🛠️ Dependências de desenvolvimento
├── template.yaml               # ☁️ Template SAM
├── Makefile                    # ⚙️ Comandos úteis
├── test_local.py              # 🧪 Teste local direto
└── README.md                  # 📖 Esta documentação
```

### 🎯 Arquivos Principais

| Arquivo                   | Descrição                                   | Quando Usar                            |
| ------------------------- | ------------------------------------------- | -------------------------------------- |
| `src/handler.py`          | **Handler principal** com logs estruturados | Sempre - sua lógica vai aqui           |
| `src/handler_advanced.py` | Handler com performance tracking            | Quando precisar de métricas detalhadas |
| `src/utils.py`            | Decorators e helpers de log                 | Quando quiser funcionalidades extras   |
| `tests/test_handler.py`   | Testes unitários                            | Sempre - garante qualidade             |

## ⚙️ Configuração

### Variáveis de Ambiente

| Variável                  | Descrição                | Padrão      | Valores                             |
| ------------------------- | ------------------------ | ----------- | ----------------------------------- |
| `ENVIRONMENT`             | Ambiente de execução     | `dev`       | `dev`, `prod`                       |
| `LOG_LEVEL`               | Nível de log             | `INFO`      | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `POWERTOOLS_SERVICE_NAME` | Nome do serviço nos logs | `my-lambda` | Qualquer string                     |

### Configuração Local

```bash
# .env (criar se necessário)
ENVIRONMENT=dev
LOG_LEVEL=DEBUG
POWERTOOLS_SERVICE_NAME=minha-lambda
```

### Configuração no SAM

```yaml
# template.yaml - já configurado
Parameters:
  Environment:
    Type: String
    Default: dev
  LogLevel:
    Type: String
    Default: INFO
```

## 🧪 Desenvolvimento Local

### Opção 1: SAM Local (Recomendado)

```bash
# Iniciar API Gateway
make local

# Testar endpoint
curl -X POST http://localhost:3000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome": "Maria", "email": "maria@email.com"}'
```

### Opção 2: Teste Python Direto

```bash
# Executar sem SAM
python test_local.py

# Ou usar comando do Makefile
make test-direct
```

### Opção 3: Testes Unitários

```bash
# Executar todos os testes
make test

# Com cobertura detalhada
pytest tests/ -v --cov=src --cov-report=html
```

### 🔧 Comandos Disponíveis

| Comando        | Descrição                   | Uso                 |
| -------------- | --------------------------- | ------------------- |
| `make help`    | Lista todos os comandos     | Referência rápida   |
| `make install` | Instala dependências        | Setup inicial       |
| `make test`    | Executa testes unitários    | Desenvolvimento     |
| `make format`  | Formata código com Black    | Antes de commit     |
| `make local`   | API Gateway local           | Teste de integração |
| `make clean`   | Remove arquivos temporários | Limpeza             |
| `make deploy`  | Deploy na AWS               | Produção            |

## 📊 Sistema de Logs

### 🆔 Rastreabilidade Completa

**Cada requisição gera:**

- **Trace ID único** (8 caracteres): `abc12345`
- **Logs estruturados** em JSON
- **Headers de correlação**: `X-Trace-ID`

### 📋 Exemplo de Log

```json
{
  "timestamp": "2025-06-12T14:30:45.123Z",
  "level": "INFO",
  "message": "Request started",
  "service": "my-lambda",
  "trace_id": "abc12345",
  "method": "POST",
  "path": "/usuarios",
  "user_agent": "curl/7.68.0",
  "ip": "192.168.1.100"
}
```

### 🔍 Campos de Log Padrão

| Campo         | Descrição              | Exemplo       |
| ------------- | ---------------------- | ------------- |
| `trace_id`    | ID único da requisição | `abc12345`    |
| `method`      | Método HTTP            | `POST`, `GET` |
| `path`        | Caminho da requisição  | `/usuarios`   |
| `status_code` | Código de resposta     | `200`, `400`  |
| `error_type`  | Tipo do erro           | `ValueError`  |
| `duration_ms` | Tempo de execução      | `150.5`       |

### 📊 Tipos de Log

#### ✅ Logs de Sucesso

```python
# Log de entrada
logger.info("Request started", extra={"trace_id": trace_id, ...})

# Log de processamento
logger.debug("Processing request data", extra={...})

# Log de saída
logger.info("Request completed successfully", extra={...})
```

#### ⚠️ Logs de Erro

```python
# Erro de validação
logger.warning("Validation error occurred", extra={...})

# Erro crítico
logger.error("Unexpected error occurred", extra={...}, exc_info=True)
```

## 🔧 Features Opcionais

### 🚀 Performance Tracking

**Usar `handler_advanced.py` para métricas automáticas:**

```python
# Decorator automático de performance
@log_performance
def minha_funcao(data, trace_id):
    # Sua lógica
    return resultado
```

**Log gerado:**

```json
{
  "message": "Function executed successfully",
  "trace_id": "abc12345",
  "function_name": "minha_funcao",
  "duration_ms": 150.5,
  "status": "success"
}
```

### 📊 Análise de Dados

**Usar utilitário `log_data_summary`:**

```python
from src.utils import log_data_summary

# Análise automática dos dados
log_data_summary(request_data, trace_id, "validation")
```

**Log gerado:**

```json
{
  "trace_id": "abc12345",
  "operation": "validation",
  "data_keys": ["name", "email"],
  "data_size": 156,
  "has_sensitive_data": false
}
```

### 🔒 Detecção de Dados Sensíveis

**Automática para campos:**

- `password`, `token`, `secret`
- `api_key`, `auth`, `credential`

## 🚀 Deploy

### Deploy Simples

```bash
# Deploy interativo
make deploy

# Ou usando SAM diretamente
sam build && sam deploy --guided
```

### Deploy com Parâmetros

```bash
# Produção com logs mínimos
sam deploy --parameter-overrides \
  Environment=prod \
  LogLevel=WARNING
```

### Deploy CI/CD

```bash
# Em pipeline
sam build
sam deploy --no-confirm-changeset \
  --no-fail-on-empty-changeset \
  --parameter-overrides Environment=prod
```

## 🔍 Troubleshooting

### 🔎 Buscar por Trace ID

```bash
# CloudWatch Logs
aws logs filter-log-events \
  --log-group-name "/aws/lambda/minha-funcao" \
  --filter-pattern '{ $.trace_id = "abc12345" }'
```

### 📊 Buscar Erros por Tipo

```bash
# Erros de validação
aws logs filter-log-events \
  --log-group-name "/aws/lambda/minha-funcao" \
  --filter-pattern '{ $.error_type = "ValueError" }'
```

### ⚡ Performance Issues

```bash
# Requisições lentas (> 1000ms)
aws logs filter-log-events \
  --log-group-name "/aws/lambda/minha-funcao" \
  --filter-pattern '{ $.duration_ms > 1000 }'
```

### 🐛 Problemas Comuns

| Problema                        | Solução                                       |
| ------------------------------- | --------------------------------------------- |
| **SAM não funciona localmente** | Use `python test_local.py`                    |
| **Imports não encontrados**     | Execute `make install`                        |
| **Logs não aparecem**           | Configure `LOG_LEVEL=DEBUG`                   |
| **Trace ID não aparece**        | Verifique se está usando `handler.py` correto |

## 📖 Exemplos

### 🎯 Handler Básico

```python
# src/handler.py - sua lógica vai em process_request()
def process_request(event: Dict[str, Any], trace_id: str) -> Dict[str, Any]:
    # Extrair dados
    body = event.get("body", {})

    # Validar
    if not body.get("name"):
        raise ValueError("Nome é obrigatório")

    # Processar
    result = {
        "message": f"Olá, {body['name']}!",
        "processed_at": datetime.now().isoformat(),
        "trace_id": trace_id
    }

    return result
```

### 🚀 Handler Avançado

```python
# src/handler_advanced.py - com performance tracking
@log_performance
def process_user_data(user_data: Dict, trace_id: str) -> Dict:
    # Log automático de entrada e performance

    # Validação com log de dados
    log_data_summary(user_data, trace_id, "user_validation")

    # Sua lógica
    return {"user_id": 123, "status": "created"}
```

### 🧪 Evento de Teste Personalizado

```json
// events/criar-usuario.json
{
  "httpMethod": "POST",
  "path": "/usuarios",
  "body": "{\"name\": \"João\", \"email\": \"joao@email.com\"}",
  "headers": { "Content-Type": "application/json" }
}
```

```bash
# Testar evento específico
sam local invoke MyFunction --event events/criar-usuario.json
```

### 📱 Teste com CURL

```bash
# Criar usuário
curl -X POST http://localhost:3000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"name": "Maria", "email": "maria@email.com"}' \
  -v  # Ver headers incluindo X-Trace-ID

# Listar usuários
curl -X GET http://localhost:3000/usuarios

# Atualizar usuário
curl -X PUT http://localhost:3000/usuarios/123 \
  -H "Content-Type: application/json" \
  -d '{"name": "Maria Silva"}'
```

## 🎯 Próximos Passos

1. **Customize** `src/handler.py` com sua lógica
2. **Adicione testes** em `tests/test_handler.py`
3. **Configure** variáveis de ambiente no `template.yaml`
4. **Teste localmente** com `make local`
5. **Deploy** com `make deploy`

## 💡 Dicas Importantes

### ✅ Boas Práticas

- **Sempre usar trace_id** para correlação
- **Logar entrada e saída** de funções importantes
- **Usar log levels apropriados** (DEBUG para desenvolvimento)
- **Incluir contexto** nos logs de erro
- **Testar localmente** antes do deploy

### ❌ Evitar

- **Over-engineering** - mantenha simples
- **Logs sensíveis** - senhas, tokens, etc.
- **Logs excessivos** em produção
- **Strings hardcoded** - use variáveis de ambiente

---

## 🚀 **Template Pronto para Produção!**

- ✅ **Logs estruturados** para troubleshooting eficiente
- ✅ **Trace ID único** para correlação completa
- ✅ **Performance tracking** opcional
- ✅ **Testes incluídos** para garantir qualidade
- ✅ **Deploy simplificado** com SAM

**Comece a desenvolver agora!** 🎯
