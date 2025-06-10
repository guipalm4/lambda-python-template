import json
import logging
import os
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    """
    Formatter for structured JSON logs
    """
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "service": os.environ.get("AWS_LAMBDA_FUNCTION_NAME", "lambda-service"),
            "environment": os.environ.get("ENVIRONMENT", "development"),
        }
        
        # Add extra fields from the record
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        # Add any additional attributes passed via extra
        for key, value in record.__dict__.items():
            if key not in ["args", "asctime", "created", "exc_info", "exc_text", 
                          "filename", "funcName", "id", "levelname", "levelno", 
                          "lineno", "module", "msecs", "message", "msg", "name", 
                          "pathname", "process", "processName", "relativeCreated", 
                          "stack_info", "thread", "threadName", "extra"]:
                log_data[key] = value
        
        return json.dumps(log_data)

def get_logger(name: str = None) -> logging.Logger:
    """
    Get a configured logger instance with JSON formatting
    
    Args:
        name: Logger name (optional)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name or __name__)
    
    # Only configure the logger if it hasn't been configured yet
    if not logger.handlers:
        log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
        logger.setLevel(getattr(logging, log_level))
        
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        
        # Prevent propagation to root logger
        logger.propagate = False
    
    return CustomLogger(logger)

class CustomLogger:
    """
    Wrapper for the logger to support extra fields
    """
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def _log(self, level: int, msg: str, extra: Dict[str, Any] = None, **kwargs):
        if extra is None:
            extra = {}
        self.logger.log(level, msg, extra={"extra": extra}, **kwargs)
    
    def debug(self, msg: str, extra: Dict[str, Any] = None, **kwargs):
        self._log(logging.DEBUG, msg, extra, **kwargs)
    
    def info(self, msg: str, extra: Dict[str, Any] = None, **kwargs):
        self._log(logging.INFO, msg, extra, **kwargs)
    
    def warning(self, msg: str, extra: Dict[str, Any] = None, **kwargs):
        self._log(logging.WARNING, msg, extra, **kwargs)
    
    def error(self, msg: str, extra: Dict[str, Any] = None, **kwargs):
        self._log(logging.ERROR, msg, extra, **kwargs)
    
    def critical(self, msg: str, extra: Dict[str, Any] = None, **kwargs):
        self._log(logging.CRITICAL, msg, extra, **kwargs)
