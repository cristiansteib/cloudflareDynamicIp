from argparse import ArgumentParser
import sys

APP_NAME = 'cloudflare-dynamic-ip'


def parse_args():
    parser = ArgumentParser(
        description='--'
    )

    parser.add_argument(
        "-t",
        "--test",
        default=False,
        action="store_true",
        help="Test the configuration files"
    )

    parser.add_argument(
        "-c",
        "--config-directory",
        action="store",
        default="/etc/" + APP_NAME,
        help="Path to the configs files"
    )

    if 'test' not in sys.argv:



        parser.add_argument(
            "-l",
            "--log-directory",
            action="store",
            default="/var/log/" + APP_NAME,
            help="Path to log files"
        )

        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            default=False,
            help="Show what is going on"
        )

        parser.add_argument(
            "-d",
            "--dry-run",
            action="store_true",
            default=False,
            help="Dry run, show what is going to do but don't make any changes"
        )


        parser.add_argument(
            "--demonize",
            "--demonize",
            action="store_true",
            default=False,
            help=""
        )


    return parser.parse_args()
