from enum import IntEnum


class AppException(Exception):
    def __init__(self, msg, code=999, detail=None):
        super().__init__(msg)
        self.message = msg
        self.code = code
        self.detail = detail or {}


class ErrorCode(IntEnum):
    ValidationError = 1
    TimeoutError = 2
    HttpError = 4
    DisabledApi = 13
    UnknownError = 999
