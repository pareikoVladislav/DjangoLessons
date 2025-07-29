from typing import Any, Dict
from enum import Enum


class ErrorType(str, Enum):
    NOT_FOUND = "not_found"
    VALIDATION_ERROR = "validation_error"
    INTEGRITY_ERROR = "integrity_error"
    DATABASE_ERROR = "database_error"
    UNKNOWN_ERROR = "unknown_error"

    @classmethod
    def errors_list(cls):
        return [attr.value for attr in cls]


class ServiceResponse:
    def __init__(
            self,
            success: bool,
            data: Any = None,
            errors: Dict[str, Any] = None,
            message: str = None,
            error_type: ErrorType = None
    ):
        self.success = success
        self.data = data
        self.errors = errors or {}
        self.message = message
        self.error_type = error_type

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'success': self.success,
        }

        if self.data is not None:
            result['data'] = self.data

        if self.errors:
            result['errors'] = self.errors

        if self.message:
            result['message'] = self.message

        if self.error_type:
            result['error_type'] = self.error_type.value

        return result
