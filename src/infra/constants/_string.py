class ApplicationConstants():
    SERVICE_NAME = "personify-service"
    LOGGER_NAME = "personify-service"
    DATABSE_NAME_PERSONIFY = 'personify'
    TABLE_NAME_USERS = 'users'
    COLLECTION_NAME_CONTACTS = 'contacts'


class GenericConstants():
    UTF8 = "UTF-8"
    CHARSET = "charset"
    ERROR = "error"
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
    HEADER_USER_ID = "X-User-Id"
    HEADER_AUTHORIZATION = "Authorization"
    BEARER = "Bearer"


class ColumnComparisionOperatorConstant():
    EQUAL = "__eq__"


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
    MSG_ACCOUNT_ALREADY_EXISTS = "Account already exists"
    MSG_INVALID_PASSWORD = "Invalid password"


class SwaggerConstants():
    API_OUTPUT_FILE = "./src/interfaces/http/swagger/swagger.json"
    OPEN_API_VERSION = "3.0.2"
    CURRENT_MAJOR_API_VERSION = "v1"
    URL_PREFIX = "/api/docs"
    TITLE = "Personify Service API"
    DESCRIPTION = "A Personify Service API for User"
    AUTHOR_NAME = "Nithin"
    AUTHOR_EMAIL = "gnknithin@gmail.com"


class RegExPatternConstants():
    FQDN = r'(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{0,62}[a-zA-Z0-9]\.)+[a-zA-Z]{2,63}$)'
    # ruff: noqa: E501
    MONGO = r'^(mongodb(\+srv)?:((?:\/{2})?)((\w+?):(\w+?)@|:?@?))(\S+?):?(\d+)?\/(\w+)?(\?(\w+=\w+(\&)?)*)?$'
    # ruff: noqa: E501
    POSTGRES_PSYCOPG2 = r'^(postgresql(\+psycopg2))?:((?:\/{2})?)((\w+?):(\w+?)(@?)(\S+?)):?(\d+)?\/(\w+)?(\?(\w+=\w+(\&)?)*)?$'


class MongoConstants():
    ENVVAR_MONGODB_HOST = "MONGODB_HOST"
    ENVVAR_MONGODB_USERNAME = "MONGODB_USERNAME"
    ENVVAR_MONGODB_PASSWORD = "MONGODB_PASSWORD"
    ENVVAR_MONGODB_DATABASE = "MONGODB_DATABASE"


class PostgresConstants():
    ENVVAR_POSTGRES_HOST = "POSTGRES_HOST"
    ENVVAR_POSTGRES_USERNAME = "POSTGRES_USER"
    ENVVAR_POSTGRES_PASSWORD = "POSTGRES_PASSWORD"
    ENVVAR_POSTGRES_DATABASE = "POSTGRES_DATABASE"


class FieldNameConstants():
    ISO = "iso"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    OBJECT_ID = "_id"
    FILTER_BY = "filter_by"
    SKIP_TO = "skip_to"
    LIMIT_BY = "limit_by"
    USER_ID = "user_id"
    CONTACT_ID = "contact_id"
    FULL_NAME = "full_name"
    GENDER = "gender"
    DATE_OF_BIRTH = "date_of_birth"
    BIRTHDAY = "birthday"
    EMAIL = "email"
    USERNAME = "username"
    PASSWORD = "password"
    MOBILE = "mobile"
    ACTIVE = "active"


class MongoDBKeywordConstants():
    DOCUMENT = "document"
    DOCUMENTS = "documents"
    SESSION = "session"
    FILTER = "filter"
    SKIP = "skip"
    LIMIT = "limit"
    UPDATE = "update"
    UPSERT = "upsert"
    RETURN_DOCUMENT = "return_document"
    OPERATOR_SET = "$set"
    OPERATOR_IN = "$in"


class MigrateEngineConstants():
    CONNECTION = "connection"
    HEAD = "head"
    MIGRATION_CONFIG_FILE = "src/infra/data/migrations/alembic.ini"


class AlembicConstants():
    ENVVAR_APPLY_MIGRATIONS_NAME = 'APPLY_MIGRATIONS'
    ENVVAR_ALAMBIC_CONFIG_NAME = 'ALEMBIC_CONFIG'
