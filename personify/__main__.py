import logging
from argparse import Namespace

from bootstrap.personify_bootstrap import PersonifyBootstrap
from infrastructure.constants._string import ApplicationConstants, GenericConstants
from infrastructure.io.event.use_asyncio import MainIOLoop
from infrastructure.logging.logger import Logger
from infrastructure.parsers.arguments import PersonifyArgumentParser
from interfaces.web.application.use_tornado import PersonifyWebApplication


def main() -> None:
    _args: Namespace = PersonifyArgumentParser().parse_arguments()
    _bootstrap = PersonifyBootstrap()
    _bootstrap.web_application = PersonifyWebApplication(
        bootstrap=_bootstrap, debug=_args.debug
    )
    _loop = MainIOLoop.setup()
    Logger.log(
        _bootstrap.logger,
        logging.INFO,
        message=GenericConstants.STARTING,
        service_name=ApplicationConstants.SERVICE_NAME,
        port=_args.port,
    )
    _ = _loop.create_task(
        coro=_bootstrap.web_application.run_server(
            personify_bootstrap=_bootstrap, port=_args.port
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
            service_name=ApplicationConstants.SERVICE_NAME,
        )
        if _bootstrap.server is not None:
            _bootstrap.server.stop()
        _loop.run_until_complete(_loop.shutdown_asyncgens())

        _loop.close()
        Logger.log(
            _bootstrap.logger,
            logging.INFO,
            message=GenericConstants.STOPPED,
            service_name=ApplicationConstants.SERVICE_NAME,
        )


if __name__ == "__main__":
    main()
