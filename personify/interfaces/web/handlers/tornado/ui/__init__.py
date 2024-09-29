from typing import List

from interfaces.web.handlers.tornado.ui.admin_request_handler import AdminRequestHandler
from interfaces.web.handlers.tornado.ui.login_request_handler import LoginRequestHandler
from interfaces.web.handlers.tornado.ui.register_request_handler import (
    RegisterRequestHandler,
)
from interfaces.web.handlers.tornado.ui.welcome_request_handler import (
    WelcomeRequestHandler,
)
from tornado.routing import URLSpec

__all__: List[str] = [
    "AdminRequestHandler",
    "LoginRequestHandler",
    "RegisterRequestHandler",
    "WelcomeRequestHandler",
]

UI_HANDLERS: List[URLSpec] = [
    URLSpec(
        pattern="/",
        handler=WelcomeRequestHandler,
        kwargs=dict(),
        name="WelcomeRequestHandler",
    ),
    URLSpec(
        pattern="/register",
        handler=RegisterRequestHandler,
        kwargs=dict(),
        name="RegisterRequestHandler",
    ),
    URLSpec(
        pattern="/login",
        handler=LoginRequestHandler,
        kwargs=dict(),
        name="LoginRequestHandler",
    ),
    URLSpec(
        pattern="/admin",
        handler=AdminRequestHandler,
        kwargs=dict(),
        name="AdminRequestHandler",
    ),
]
