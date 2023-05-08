import json
import os

from infra.constants._string import GenericConstants, SwaggerConstants
from interfaces.http.swagger.swagger_middlewear import SwaggerMiddleware

from tests.utils.base_tests import MainApplicationTestSetup


class TestSwaggerMiddleware(MainApplicationTestSetup):

    def test_should_generate_api_specs_properly(self):
        # Arrange
        app = self.get_app()
        port = 8888
        # Act
        SwaggerMiddleware.generate_swagger_file(
            handlers=app.handlers,
            port=port
        )

        loaded_api_specs = None
        with open(
            SwaggerConstants.API_OUTPUT_FILE,
            'r',
            encoding=GenericConstants.UTF8
        ) as specs_file:
            loaded_api_specs = json.load(specs_file)

        # Assert
        assert os.path.isfile(SwaggerConstants.API_OUTPUT_FILE)
        assert os.path.getsize(SwaggerConstants.API_OUTPUT_FILE) > 0
        assert loaded_api_specs is not None

    def test_should_initialize_properly(self):
        # Arrange
        app = self.get_app()
        port = 8888
        # Act
        SwaggerMiddleware.initialize(
            port=port,
            app=app
        )

        loaded_api_specs = None
        with open(
            SwaggerConstants.API_OUTPUT_FILE,
            'r',
            encoding=GenericConstants.UTF8
        ) as specs_file:
            loaded_api_specs = json.load(specs_file)

        # Assert
        assert os.path.isfile(SwaggerConstants.API_OUTPUT_FILE)
        assert os.path.getsize(SwaggerConstants.API_OUTPUT_FILE) > 0
        assert loaded_api_specs is not None
