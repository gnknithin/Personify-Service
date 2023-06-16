import json
from typing import Any, Dict, List

import swagger_ui
from apispec import APISpec
from apispec.exceptions import APISpecError
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.tornado import TornadoPlugin
from infra.constants._string import GenericConstants, SwaggerConstants
from interfaces.http.tornado.tornado_app import MainApplication


class SwaggerMiddleware():
    @staticmethod
    def initialize(port: int, app: MainApplication):
        SwaggerMiddleware.generate_swagger_file(
            handlers=app.handlers,
            port=port
        )

        swagger_ui.api_doc(
            app,
            config_path=SwaggerConstants.API_OUTPUT_FILE,
            url_prefix=SwaggerConstants.URL_PREFIX,
            title=SwaggerConstants.TITLE,
            editor=True
        )

    @staticmethod
    def generate_swagger_file(
        handlers: List[Any],
        port: int,
        file_location: str = SwaggerConstants.API_OUTPUT_FILE
    ) -> None:
        """Automatically generates Swagger spec file based on RequestHandler
        docstrings and saves it to the specified file_location.

        Args:
            handlers ([list]): RequestHandler to generate auto documentation
            port (int): Service instance exposed port
            file_location ([str]): file location
        """
        spec = APISpec(
            title=SwaggerConstants.TITLE,
            version=SwaggerConstants.CURRENT_MAJOR_API_VERSION,
            openapi_version=SwaggerConstants.OPEN_API_VERSION,
            info=dict(
                description=SwaggerConstants.DESCRIPTION,
                contact=dict(
                    name=SwaggerConstants.AUTHOR_NAME,
                    email=SwaggerConstants.AUTHOR_EMAIL
                ),
                license=dict(
                    name=None,
                    url=None
                )
            ),
            tags=[],
            plugins=[TornadoPlugin(), MarshmallowPlugin()],
            servers=[
                {
                    'url': f'http://localhost:{port}/',
                    'description': 'Local environment',
                }
            ]
        )
        # Add Security
        _bearerAuth: Dict[Any, Any] = dict()
        _bearerAuth["type"] = "http"
        _bearerAuth["scheme"] = "bearer"
        _bearerAuth["bearerFormat"] = "JWT"
        _bearerAuth["example"] = "Bearer eyJhbGciOiJIUzI1NiJ9eyJoZWxsbyI6IndvcmxkIn0"
        spec.components.security_scheme("bearerAuth", _bearerAuth)

        for handler in handlers:
            try:
                spec.path(urlspec=handler)
            except APISpecError:
                pass

        with open(file_location, 'w', encoding=GenericConstants.UTF8) as file:
            json.dump(spec.to_dict(), file, ensure_ascii=False, indent=4)
