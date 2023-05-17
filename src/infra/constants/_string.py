class ApplicationConstants():
    SERVICE_NAME = "personify-service"
    LOGGER_NAME = "personify-service"


class GenericConstants():
    UTF8 = "UTF-8"
    CHARSET = "charset"
    ERROR= "error"
    ERRORS = "errors"
    SUCCESS = "success"
    DATA = "data"
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
    UNCAUGHT_EXCEPTION = "Uncaught exception"
    STARTING = "STARTING"
    SHUTTING_DOWN = "SHUTTING DOWN"
    STOPPED = "STOPPED"
    REQUEST_ID = "request_id"
    METHOD = "method"
    URI = "uri"
    IP = "ip"
    CODE = "code"
    STATUS_CODE = "status_code"
    MESSAGE = "message"
    DECOMPRESS_REQUEST = "decompress_request"


class ConfigurationConstants():
    LOGGER = "logger"
    LOGGING = "logging"

class HttpMethodConstants():
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class HttpConstants():
    HEADER_CONTENT_TYPE = "Content-Type"
    MIME_TYPE_JSON = "application/json"
    OPERATIONS = [
        HttpMethodConstants.GET,
        HttpMethodConstants.POST,
        HttpMethodConstants.PUT,
        HttpMethodConstants.DELETE,
        HttpMethodConstants.PATCH
        ]
    READONLY_OPERATIONS = ["GET", "HEAD", "OPTIONS"]
    WRITE_OPERATIONS = [
        HttpMethodConstants.POST,
        HttpMethodConstants.PUT,
        HttpMethodConstants.PATCH
    ]


class MessagesConstants():
    MSG_UNKNOWN_ENDPOINT = "Unknown Endpoint"
    MSG_RESULT_OF_SERVICE_CALL = "Result status of service call - SHOULD BE FALSE"
    MSG_REASON_FOR_FAILED_REQUEST = "".join(
        [
            "Reason for failed request (sender).",
            " ",
            "Could be a string or a dictionary"
        ]
    )
    MSG_BAD_PARAMETER_INPUT_FORMAT = "Bad parameter input format"
    MSG_BAD_PARAMETER_INPUT_CONTENT = "Bad parameter input content"
    MSG_SERVER_TIMEOUT = "Server timeout - please try again"
    MSG_VALIDITY_IN_CASE_OF_FAILURE = "".join(
        ["Validity of this data envelope In case of failure it will return FALSE"]
    )
    MSG_INVALID_SCHEMA_VALIDATION = "Invalid-Schema-Validation JSON body"
    MSG_EMPTY_REQUEST_BODY = "Empty request body"
    MSG_WORKER_NOT_FOUND = "Worker not found"
    MSG_WORKER_IS_NOT_ACTIVE = "Worker is not active"
    MSG_FACILITY_IS_NOT_ACTIVE = "Facility is not active"
    MSG_INVALID_ID = "Invalid Id"
    MSG_INVALID_QUERY_ARGUMENTS = "Invalid query arguments"
    MSG_INVALID_NEGATIVE_INTEGER = "Invalid negative number"
    MSG_PARAMETERS_OUT_OF_RANGE = "Parameters are out of range"


class SwaggerConstants():
    API_OUTPUT_FILE = "./src/interfaces/http/swagger/swagger.json"
    OPEN_API_VERSION = "3.0.2"
    CURRENT_MAJOR_API_VERSION = "v1"
    URL_PREFIX = "/api/docs"
    TITLE = "Personify Service API"
    DESCRIPTION = "A Personify Service API for User"
    AUTHOR_NAME = "Nithin"
    AUTHOR_EMAIL = "gnknithin@gmail.com"