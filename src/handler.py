import json
import os
import uuid
from typing import Any, Dict

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

# Simple configuration with structured logging
logger = Logger(
    service="my-lambda",
    level=os.getenv("LOG_LEVEL", "INFO"),
    log_uncaught_exceptions=True,
)
tracer = Tracer()


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """Função principal do Lambda"""
    # Gerar trace_id único para rastreabilidade
    trace_id = str(uuid.uuid4())[:8]

    # Log de entrada com dados estruturados
    logger.info(
        "Request started",
        extra={
            "trace_id": trace_id,
            "method": event.get("httpMethod"),
            "path": event.get("path"),
            "user_agent": event.get("headers", {}).get("User-Agent"),
            "ip": event.get("requestContext", {}).get("identity", {}).get("sourceIp"),
        },
    )

    try:
        # Sua lógica aqui
        result = process_request(event, trace_id)

        # Log de sucesso
        logger.info(
            "Request completed successfully",
            extra={
                "trace_id": trace_id,
                "status_code": 200,
                "response_size": len(json.dumps(result)),
            },
        )

        return create_response(200, result, trace_id)

    except ValueError as e:
        # Log de erro de validação com contexto
        logger.warning(
            "Validation error occurred",
            extra={
                "trace_id": trace_id,
                "error_type": "ValidationError",
                "error_message": str(e),
                "event_data": event,
            },
        )
        return create_response(400, {"error": str(e)}, trace_id)

    except Exception as e:
        # Log de erro crítico com stack trace
        logger.error(
            "Unexpected error occurred",
            extra={
                "trace_id": trace_id,
                "error_type": type(e).__name__,
                "error_message": str(e),
                "event_data": event,
            },
            exc_info=True,  # Inclui stack trace completo
        )
        return create_response(500, {"error": "Internal server error"}, trace_id)


@tracer.capture_method
def process_request(event: Dict[str, Any], trace_id: str) -> Dict[str, Any]:
    """Processa a requisição do Lambda"""
    logger.debug(
        "Processing request data",
        extra={
            "trace_id": trace_id,
            "event_keys": list(event.keys()),
            "body_size": len(str(event.get("body", ""))),
        },
    )

    if not event:
        raise ValueError("Event cannot be empty")

    # Simular processamento com logs intermediários
    body = event.get("body", {})
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            logger.warning(
                "Invalid JSON in request body",
                extra={"trace_id": trace_id, "raw_body": body},
            )
            body = {}

    # Log de processamento bem-sucedido
    logger.debug(
        "Request processing completed",
        extra={
            "trace_id": trace_id,
            "processed_data_keys": list(body.keys()) if body else [],
            "environment": os.getenv("ENVIRONMENT", "dev"),
        },
    )

    # Sua lógica de negócio aqui
    return {
        "message": "Success!",
        "data": body,
        "environment": os.getenv("ENVIRONMENT", "dev"),
        "trace_id": trace_id,
    }


def create_response(status: int, data: Any, trace_id: str = None) -> Dict[str, Any]:
    """Cria resposta padronizada com headers de rastreamento"""
    # Adicionar trace_id na resposta para correlação
    if trace_id:
        if isinstance(data, dict):
            data["trace_id"] = trace_id

    response = {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "X-Trace-ID": trace_id
            or "unknown",  # Header personalizado para rastreamento
        },
        "body": json.dumps(data, ensure_ascii=False),
    }

    # Log da resposta final
    logger.debug(
        "Response created",
        extra={
            "trace_id": trace_id,
            "status_code": status,
            "response_headers": response["headers"],
        },
    )

    return response
