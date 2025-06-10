# 🚀 Lambda Python Template

Template **ultra simples** para AWS Lambda em Python com SDK atualizada.

## ⚡ Uso Rápido

```bash
# Setup
make install

# Teste
make test

# Deploy
make deploy
```

## 📝 Desenvolvimento

1. **Edite sua lógica** em `src/handler.py` na função `processar_requisicao()`
2. **Adicione testes** em `tests/test_handler.py`
3. **Execute** `make test`
4. **Deploy** com `make deploy`

## 🎯 Comandos

- `make install` - Instala dependências
- `make test` - Executa testes
- `make format` - Formata código
- `make local` - API local (localhost:3000)
- `make deploy` - Deploy na AWS
- `make clean` - Limpa arquivos

## 📊 Recursos

✅ **Python 3.12** (mais recente)  
✅ **AWS Lambda Powertools 3.2.0** (SDK atualizada)  
✅ **Logs estruturados** automáticos  
✅ **Tracing** com X-Ray  
✅ **Testes** incluídos  
✅ **Deploy** com SAM

## 🧪 Teste Local

```bash
# Iniciar API
make local

# Testar
curl -X POST http://localhost:3000/teste \
  -d '{"nome": "exemplo"}'
```

**Zero complexidade, máxima produtividade!** ⚡
