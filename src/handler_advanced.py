import json
import os
import uuid
from typing import Any, Dict

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext
from src.utils import log_performance, log_data_summary

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
    """Função principal do Lambda com logs avançados"""
    trace_id = str(uuid.uuid4())[:8]

    # Log de entrada estruturado
    logger.info(
        "Lambda execution started",
        extra={
            "trace_id": trace_id,
            "function_name": context.function_name,
            "remaining_time_ms": context.get_remaining_time_in_millis(),
            "memory_limit_mb": context.memory_limit_in_mb,
            "request_id": context.aws_request_id,
            "method": event.get("httpMethod"),
            "path": event.get("path"),
        },
    )

    try:
        result = process_request_with_tracking(event, trace_id)

        logger.info(
            "Lambda execution completed successfully",
            extra={
                "trace_id": trace_id,
                "status": "success",
                "response_size_bytes": len(json.dumps(result)),
            },
        )

        return create_response(200, result, trace_id)

    except Exception as e:
        logger.error(
            "Lambda execution failed",
            extra={
                "trace_id": trace_id,
                "error_type": type(e).__name__,
                "error_message": str(e),
            },
            exc_info=True,
        )
        return create_response(500, {"error": "Internal server error"}, trace_id)


@log_performance
def process_request_with_tracking(
    event: Dict[str, Any], trace_id: str
) -> Dict[str, Any]:
    """Processa requisição com tracking de performance"""
    if not event:
        raise ValueError("Event cannot be empty")

    # Log do resumo dos dados
    log_data_summary(event, trace_id, "input_validation")

    # Sua lógica de negócio aqui
    return {
        "message": "Success!",
        "data": event.get("body", {}),
        "environment": os.getenv("ENVIRONMENT", "dev"),
        "trace_id": trace_id,
    }


def create_response(status: int, data: Any, trace_id: str = None) -> Dict[str, Any]:
    """Cria resposta padronizada com headers de rastreamento"""
    if trace_id and isinstance(data, dict):
        data["trace_id"] = trace_id

    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "X-Trace-ID": trace_id or "unknown",
        },
        "body": json.dumps(data, ensure_ascii=False),
    }
