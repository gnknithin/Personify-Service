import logging
from http import HTTPStatus
from typing import Any, Dict, OrderedDict

from infra.constants._string import GenericConstants
from interfaces.http.tornado.handlers.base_handler import BaseRequestHandler
from interfaces.http.tornado.schemas.base_schema import BaseSuccessSchema


class HealthHandler(BaseRequestHandler):
    def initialize(
        self,
        logger: logging.Logger,
        schema_method_validators: Dict[Any, Any]
    ) -> None:
        super().initialize(logger, schema_method_validators)

    async def get(self):
        """Check system health
        ---
        tags: [System]
        summary: Returns Ok for successful request
        description: Ok for successful response
        responses:
            200:
                description: Successfully return Ok
                content:
                    application/json:
                        schema:
                            BaseSuccessSchema

            400:
                description: Invalid request format
                content:
                    application/json:
                        schema:
                            BadRequestSchema

            404:
                description: Invalid request content
                content:
                    application/json:
                        schema:
                            NotFoundSchema

            500:
                description: Server error
                content:
                    application/json:
                        schema:
                            ServerErrorSchema
        """
        _info : Dict[Any,Any] = dict()
        _info[GenericConstants.SUCCESS] = False
        _loaded: OrderedDict[Any,Any] = BaseSuccessSchema().load(data=_info)
        self.build_response(
            status=HTTPStatus.OK,
            data=_loaded
        )
