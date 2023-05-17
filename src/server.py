import logging
from argparse import Namespace

from bootstrap import ApplicationBootstrap
from infra.constants._string import ApplicationConstants, GenericConstants
from infra.io.loop import MainIOLoop
from infra.logging.logger import Logger
from infra.parser.argument_parser import ArgumentParser
from interfaces.http.swagger.swagger_middlewear import SwaggerMiddleware
from interfaces.http.tornado.tornado_app import MainApplication


def main(
    args: Namespace = ArgumentParser.parse_arguments()
):
    _bootstrap = ApplicationBootstrap(bootstrap_args=args)
    _app = MainApplication(
        bootstrap=_bootstrap,
        debug=args.debug
    )
    SwaggerMiddleware.initialize(
        port=args.port,
        app=_app
    )
    _loop = MainIOLoop.setup()
    Logger.log(
        _bootstrap.logger,
        logging.INFO,
        message=GenericConstants.STARTING,
        service_name=ApplicationConstants.SERVICE_NAME,
        port=args.port
    )
    _loop.create_task(
        MainApplication.run_server(
            app_bootstrap=_bootstrap,
            app=_app,
            port=args.port
        )
    )

    try:
        _loop.run_forever()
    except KeyboardInterrupt:
        # signal.SIGINT
        pass
    finally:
        _loop.stop()
        Logger.log(
            _bootstrap.logger,
            logging.INFO,
            message=GenericConstants.SHUTTING_DOWN,
            service_name=ApplicationConstants.SERVICE_NAME
        )
        if _bootstrap.server is not None:
            _bootstrap.server.stop()
        _loop.run_until_complete(_loop.shutdown_asyncgens())

        _loop.close()
        Logger.log(
            _bootstrap.logger,
            logging.INFO,
            message=GenericConstants.STOPPED,
            service_name=ApplicationConstants.SERVICE_NAME
        )


if __name__ == '__main__':
    main()
