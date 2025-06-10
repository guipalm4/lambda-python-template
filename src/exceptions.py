class BusinessException(Exception):
    """Base exception for business logic errors"""
    pass

class ValidationError(BusinessException):
    """Validation error exception"""
    pass

class ResourceNotFoundException(BusinessException):
    """Resource not found exception"""
    pass

class ExternalServiceException(Exception):
    """Exception for external service errors"""
    def __init__(self, service_name: str, message: str, status_code: int = None):
        self.service_name = service_name
        self.status_code = status_code
        super().__init__(f"{service_name} error: {message}")
