#!venv/bin/python
from pathlib import Path

import argparse
import asyncio
import logging

from aiohttp import web
from alembic import command
from alembic.config import Config

from api.app import create_app
from api.settings import load_config

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    logging.warning("Uvloop is not available")

parser = argparse.ArgumentParser(
    description="Simple Aiohttp server",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument("--host", help="Host to listen")
parser.add_argument("--port", help="Port to accept connections")
parser.add_argument(
    "--reload",
    action="store_true",
    help="Reload server when code is changed. For development purposes",
)
# for migrations
parser.add_argument("--migrate", action="store_true", help="Migrate database")
parser.add_argument("--revision", action="store_true", help="Create new migration revision")
parser.add_argument("--show", action="store_true", help="Show migrations")
parser.add_argument("--downgrade", action="store_true", help="Downgrade db migration")
parser.add_argument(
    "-c",
    "--config",
    dest="config_file",
    help="Path to configuration file",
)

args = parser.parse_args()
config = load_config(path=Path(args.config_file).parent, custom_config=args.config_file)

# Auto-reload
if args.reload:
    import aioreloader

    aioreloader.start()

if __name__ == '__main__':
    if args.migrate:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(config=alembic_cfg, revision="head")
    elif args.revision:
        alembic_cfg = Config("alembic.ini")
        message = input("Revision comment: ")
        command.revision(config=alembic_cfg, autogenerate=True, message=message)
    elif args.show:
        alembic_cfg = Config("alembic.ini")
        command.show(config=alembic_cfg, rev="head")
    elif args.downgrade:
        alembic_cfg = Config("alembic.ini")
        revision = input("Downgrade revision (-1 for previous, Enter to skip): ")
        if revision:
            command.downgrade(alembic_cfg, revision)
    else:
        app = create_app(config=config)
        web.run_app(
            app=app,
            host=config.get("host", args.host),
            port=config.get("port", args.port),
        )
