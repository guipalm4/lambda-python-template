import json
import time
from typing import Dict, Any
from aws_lambda_powertools import Logger

logger = Logger()


def log_performance(func):
    """Decorator para medir e logar performance"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        trace_id = kwargs.get('trace_id', 'unknown')
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            logger.info(
                "Function executed successfully",
                extra={
                    "trace_id": trace_id,
                    "function_name": func.__name__,
                    "duration_ms": round(duration * 1000, 2),
                    "status": "success"
                }
            )
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                "Function execution failed",
                extra={
                    "trace_id": trace_id,
                    "function_name": func.__name__,
                    "duration_ms": round(duration * 1000, 2),
                    "status": "error",
                    "error": str(e)
                },
                exc_info=True
            )
            raise
    
    return wrapper


def log_data_summary(data: Dict[str, Any], trace_id: str, operation: str = "processing"):
    """Loga resumo dos dados de forma estruturada"""
    if not isinstance(data, dict):
        data = {"raw_data": str(data)}
    
    summary = {
        "trace_id": trace_id,
        "operation": operation,
        "data_keys": list(data.keys()),
        "data_size": len(json.dumps(data)),
        "has_sensitive_data": any(key.lower() in ['password', 'token', 'secret'] for key in data.keys())
    }
    
    logger.debug("Data processing summary", extra=summary)
    return summary