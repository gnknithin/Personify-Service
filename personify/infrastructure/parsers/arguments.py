import argparse
from typing import Optional, Sequence


class PersonifyArgumentParser:
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def parse_arguments(
        input_args: Optional[Sequence[str]] = None,
    ) -> argparse.Namespace:
        inputs_parser = argparse.ArgumentParser(
            prog="Personify Server", description="Run Personify Service"
        )

        _ = inputs_parser.add_argument(
            "-p",
            "--port",
            type=int,
            default=8888,
            help="port number for %(prog)s server to listen; 'default: %(default)s",
        )

        _ = inputs_parser.add_argument(
            "-d", "--debug", action="store_true", help="turn on debug logging"
        )

        parsed_input_args = inputs_parser.parse_args(args=input_args, namespace=None)
        return parsed_input_args
