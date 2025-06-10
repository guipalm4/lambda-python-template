import os
from typing import Any, Dict


class Config:
    """Configuration management for the Lambda function"""
    
    @classmethod
    def get_env(cls, key: str, default: Any = None) -> Any:
        """
        Get environment variable
        
        Args:
            key: Environment variable name
            default: Default value if not found
            
        Returns:
            Environment variable value or default
        """
        return os.environ.get(key, default)
    
    @classmethod
    def get_boolean(cls, key: str, default: bool = False) -> bool:
        """
        Get boolean environment variable
        
        Args:
            key: Environment variable name
            default: Default value if not found
            
        Returns:
            Boolean value of environment variable
        """
        value = cls.get_env(key)
        if value is None:
            return default
        return value.lower() in ('true', 't', 'yes', 'y', '1')
    
    @classmethod
    def get_int(cls, key: str, default: int = 0) -> int:
        """
        Get integer environment variable
        
        Args:
            key: Environment variable name
            default: Default value if not found
            
        Returns:
            Integer value of environment variable
        """
        value = cls.get_env(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default
    
    # Common configuration properties
    @property
    def environment(self) -> str:
        return self.get_env("ENVIRONMENT", "development")
    
    @property
    def log_level(self) -> str:
        return self.get_env("LOG_LEVEL", "INFO")
    
    @property
    def timeout_seconds(self) -> int:
        return self.get_int("TIMEOUT_SECONDS", 30)
