import json
import pytest
from unittest.mock import MagicMock, patch
from src.handler import lambda_handler, process_request


def create_mock_context():
    """Cria um contexto mock para os testes"""
    context = MagicMock()
    context.function_name = "test-function"
    context.memory_limit_in_mb = 256
    context.invoked_function_arn = (
        "arn:aws:lambda:us-east-1:123456789012:function:test-function"
    )
    context.aws_request_id = "test-request-id"
    context.get_remaining_time_in_millis.return_value = 30000
    return context


def create_api_gateway_event(method="POST", path="/test", body=None):
    """Cria evento mock do API Gateway"""
    return {
        "httpMethod": method,
        "path": path,
        "headers": {"Content-Type": "application/json", "User-Agent": "test-agent"},
        "body": json.dumps(body) if body else None,
        "requestContext": {"identity": {"sourceIp": "127.0.0.1"}},
    }


def test_handler_success():
    """Testa execução com sucesso e logs estruturados"""
    event = create_api_gateway_event("POST", "/test", {"name": "test"})
    context = create_mock_context()

    response = lambda_handler(event, context)

    assert response["statusCode"] == 200
    data = json.loads(response["body"])
    assert data["message"] == "Success!"
    assert "trace_id" in data
    assert "X-Trace-ID" in response["headers"]


def test_handler_validation_error():
    """Testa erro de validação com logs estruturados"""
    event = {}
    context = create_mock_context()

    response = lambda_handler(event, context)

    assert response["statusCode"] == 400
    data = json.loads(response["body"])
    assert "error" in data
    assert "trace_id" in data


def test_process_request_with_json_body():
    """Testa processamento com body JSON"""
    event = {"body": '{"test": "data", "number": 123}', "httpMethod": "POST"}

    result = process_request(event, "test-trace-123")

    assert result["message"] == "Success!"
    assert result["data"]["test"] == "data"
    assert result["data"]["number"] == 123
    assert result["trace_id"] == "test-trace-123"


def test_process_request_with_invalid_json():
    """Testa processamento com JSON inválido"""
    event = {"body": '{"invalid": json}', "httpMethod": "POST"}  # JSON mal formado

    result = process_request(event, "test-trace-456")

    assert result["message"] == "Success!"
    assert result["data"] == {}  # Body vazio por JSON inválido
    assert result["trace_id"] == "test-trace-456"


def test_empty_event():
    """Testa evento vazio"""
    with pytest.raises(ValueError, match="Event cannot be empty"):
        process_request({}, "test-trace-789")


def test_create_response_with_trace():
    """Testa criação de resposta com trace_id"""
    from src.handler import create_response

    response = create_response(200, {"test": "data"}, "trace-123")

    assert response["statusCode"] == 200
    assert response["headers"]["X-Trace-ID"] == "trace-123"

    data = json.loads(response["body"])
    assert data["test"] == "data"
    assert data["trace_id"] == "trace-123"


@patch("src.handler.logger")
def test_logging_flow(mock_logger):
    """Testa fluxo de logs estruturados"""
    event = create_api_gateway_event("GET", "/users")
    context = create_mock_context()

    response = lambda_handler(event, context)

    # Verifica se logs foram chamados
    assert mock_logger.info.called
    assert mock_logger.debug.called

    # Verifica estrutura dos logs
    calls = mock_logger.info.call_args_list
    assert len(calls) >= 2  # Log de entrada e saída

    # Verifica se trace_id está presente nos logs
    for call in calls:
        if call[1] and "extra" in call[1]:
            assert "trace_id" in call[1]["extra"]
