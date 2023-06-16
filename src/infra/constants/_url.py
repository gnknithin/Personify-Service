
class HandlerConstants():
    ROOT = "/"
    HEALTH_URI = "/health"
    API = "/api"
    VERSION_1 = "/v1"


class APIPathConstants():
    BASE_VERSION_1 = f'{HandlerConstants.API}{HandlerConstants.VERSION_1}'


class UserActionConstants():
    SIGNUP = "/signup"
    SIGNIN = "/signin"
    CONTACT = "/contact"
    CONTACT_BY_ID = "/contact/{contact_id}"
    CONTACT_BY_ID_REGEX = "/contact/(?P<contact_id>[a-zA-Z0-9-]+)/?"


class APIEndpointV1():
    SIGNUP_URI = f'{APIPathConstants.BASE_VERSION_1}{UserActionConstants.SIGNUP}'
    SIGNIN_URI = f'{APIPathConstants.BASE_VERSION_1}{UserActionConstants.SIGNIN}'
    CONTACT_URI = f'{APIPathConstants.BASE_VERSION_1}{UserActionConstants.CONTACT}'
    # ruff: noqa: E501
    CONTACT_BY_ID_URI = f'{APIPathConstants.BASE_VERSION_1}{UserActionConstants.CONTACT_BY_ID}'
    # ruff: noqa: E501
    CONTACT_BY_ID_URI_REGEX = f'{APIPathConstants.BASE_VERSION_1}{UserActionConstants.CONTACT_BY_ID_REGEX}'
