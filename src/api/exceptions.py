from __future__ import annotations


class ApiError(Exception):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


class BadRequestError(ApiError):
    def __init__(self, code: str, message: str, details: dict[str, str] | None = None) -> None:
        super().__init__(status_code=400, code=code, message=message, details=details)


class NotFoundError(ApiError):
    def __init__(self, code: str, message: str, details: dict[str, str] | None = None) -> None:
        super().__init__(status_code=404, code=code, message=message, details=details)


class ConflictError(ApiError):
    def __init__(self, code: str, message: str, details: dict[str, str] | None = None) -> None:
        super().__init__(status_code=409, code=code, message=message, details=details)


class UnprocessableEntityError(ApiError):
    def __init__(self, code: str, message: str, details: dict[str, str] | None = None) -> None:
        super().__init__(status_code=422, code=code, message=message, details=details)


class UpstreamServiceError(ApiError):
    def __init__(self, code: str, message: str, details: dict[str, str] | None = None) -> None:
        super().__init__(status_code=502, code=code, message=message, details=details)
