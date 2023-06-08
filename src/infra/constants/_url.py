
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


class APIEndpointV1():
    SIGNUP_URI = f'{APIPathConstants.BASE_VERSION_1}{UserActionConstants.SIGNUP}'
    SIGNIN_URI = f'{APIPathConstants.BASE_VERSION_1}{UserActionConstants.SIGNIN}'
