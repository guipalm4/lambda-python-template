import json
import traceback
from typing import Any, Dict

from src.config import Config
from src.exceptions import BusinessException
from src.utils.logger import get_logger

logger = get_logger()

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler function
    
    Args:
        event: AWS Lambda event
        context: AWS Lambda context
    
    Returns:
        Response dictionary
    """
    request_id = context.aws_request_id
    logger.info("Lambda invocation started", extra={
        "request_id": request_id,
        "event_type": event.get("type", "unknown")
    })
    
    try:
        # Parse input
        logger.debug("Processing event", extra={"event": event})
        
        # Process business logic
        result = process_event(event)
        
        # Prepare response
        response = {
            "statusCode": 200,
            "body": json.dumps(result),
            "headers": {
                "Content-Type": "application/json",
                "X-Request-ID": request_id
            }
        }
        
        logger.info("Lambda invocation completed successfully", extra={
            "request_id": request_id,
            "execution_time_ms": context.get_remaining_time_in_millis()
        })
        
        return response
        
    except BusinessException as be:
        logger.warning(f"Business exception: {str(be)}", extra={
            "request_id": request_id,
            "error_type": be.__class__.__name__
        })
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(be), "type": "business_error"}),
            "headers": {
                "Content-Type": "application/json",
                "X-Request-ID": request_id
            }
        }
        
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}", extra={
            "request_id": request_id,
            "error_type": e.__class__.__name__,
            "traceback": traceback.format_exc()
        })
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "request_id": request_id}),
            "headers": {
                "Content-Type": "application/json",
                "X-Request-ID": request_id
            }
        }

def process_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process the Lambda event
    
    Args:
        event: AWS Lambda event
    
    Returns:
        Processed result
    """
    # Implement your business logic here
    return {"message": "Hello from Lambda!"}
