import json
import os
from typing import Any, Dict

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

# Simple configuration
logger = Logger()
tracer = Tracer()


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """Função principal do Lambda"""
    try:
        logger.info("Processing request", method=event.get("httpMethod"))
        
        # Sua lógica aqui
        result = process_request(event)
        
        return create_response(200, result)
        
    except ValueError as e:
        logger.warning("Validation error", error=str(e))
        return create_response(400, {"error": str(e)})
        
    except Exception as e:
        logger.error("Unexpected error", error=str(e))
        return create_response(500, {"error": "Internal server error"})


@tracer.capture_method
def process_request(event: Dict[str, Any]) -> Dict[str, Any]:
    """Processa a requisição do Lambda"""
    if not event:
        raise ValueError("Event cannot be empty")
    
    # Sua lógica de negócio aqui
    return {
        "message": "Success!",
        "data": event.get("body", {}),
        "environment": os.getenv("ENVIRONMENT", "dev")
    }


def create_response(status: int, data: Any) -> Dict[str, Any]:
    """Cria resposta padronizada"""
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(data, ensure_ascii=False)
    }