from typing import List

from interfaces.web.handlers.tornado.ui import UI_HANDLERS
from tornado.routing import URLSpec

PERSONIFY_HANDLERS: List[URLSpec] = UI_HANDLERS
