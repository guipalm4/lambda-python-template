import json
import pytest
from unittest.mock import MagicMock
from src.handler import lambda_handler, process_request


def create_mock_context():
    """Cria um contexto mock para os testes"""
    context = MagicMock()
    context.function_name = "test-function"
    context.memory_limit_in_mb = 256
    context.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
    context.aws_request_id = "test-request-id"
    context.get_remaining_time_in_millis.return_value = 30000
    return context


def test_handler_success():
    """Testa execução com sucesso"""
    event = {"body": {"name": "test"}, "httpMethod": "POST"}
    context = create_mock_context()
    
    response = lambda_handler(event, context)
    
    assert response["statusCode"] == 200
    data = json.loads(response["body"])
    assert data["message"] == "Success!"


def test_handler_validation_error():
    """Testa erro de validação"""
    event = {}
    context = create_mock_context()
    
    response = lambda_handler(event, context)
    
    assert response["statusCode"] == 400


def test_process_request():
    """Testa processamento da requisição"""
    event = {"body": {"test": "data"}}
    result = process_request(event)
    
    assert result["message"] == "Success!"
    assert result["data"] == {"test": "data"}


def test_empty_event():
    """Testa evento vazio"""
    with pytest.raises(ValueError):
        process_request({})


def test_create_response():
    """Testa criação de resposta"""
    from src.handler import create_response
    
    response = create_response(200, {"test": "data"})
    
    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"
    assert json.loads(response["body"])["test"] == "data"