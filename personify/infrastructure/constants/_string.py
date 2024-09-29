from typing import Final


class ApplicationConstants:
    LOGGER_NAME: Final = "personify"
    SERVICE_NAME = "personify"


class ConfigurationConstants:
    LOGGER = "logger"


class GenericConstants:
    UTF8 = "UTF-8"
    CHARSET = "charset"
    ERRORS = "errors"
    SUCCESS = "success"
    STATUS_CODE = "status_code"
    MESSAGE = "message"
    REQUEST_ID = "request_id"
    METHOD = "method"
    URI = "uri"
    IP = "ip"
    CODE = "code"
    REQUEST = "REQUEST"
    UNCAUGHT_EXCEPTION = "Uncaught exception"
    RESPONSE = "RESPONSE"
    DECOMPRESS_REQUEST = "decompress_request"
    STARTING = "STARTING"
    SHUTTING_DOWN = "SHUTTING DOWN"
    STOPPED = "STOPPED"


class MessagesConstants:
    MSG_UNKNOWN_ENDPOINT = "Unknown Endpoint"
    MSG_VALIDITY_IN_CASE_OF_FAILURE = "".join(
        ["Validity of this data envelope In case of failure it will return FALSE"]
    )
    MSG_RESULT_OF_SERVICE_CALL = "Result status of service call - SHOULD BE FALSE"
    MSG_REASON_FOR_FAILED_REQUEST = "".join(
        [
            "Reason for failed request (sender).",
            " ",
            "Could be a string or a dictionary",
        ]
    )
    MSG_BAD_PARAMETER_INPUT_FORMAT = "Bad parameter input format"
    MSG_BAD_PARAMETER_INPUT_CONTENT = "Bad parameter input content"
    MSG_SERVER_TIMEOUT = "Server timeout - please try again"
    MSG_INVALID_SCHEMA_VALIDATION = "Invalid-Schema-Validation JSON body"
    MSG_EMPTY_REQUEST_BODY = "Empty request body"


class HttpMethodConstants:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class HttpConstants:
    HEADER_CONTENT_TYPE = "Content-Type"
    MIME_TYPE_JSON = "application/json"
    OPERATIONS = [
        HttpMethodConstants.GET,
        HttpMethodConstants.POST,
        HttpMethodConstants.PUT,
        HttpMethodConstants.DELETE,
        HttpMethodConstants.PATCH,
    ]
    READONLY_OPERATIONS = ["GET", "HEAD", "OPTIONS"]
    WRITE_OPERATIONS = [
        HttpMethodConstants.POST,
        HttpMethodConstants.PUT,
        HttpMethodConstants.PATCH,
    ]
