from pathlib import Path

from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_swagger import setup_swagger


def setup_docs(app):
    setup_aiohttp_apispec(
        app=app,
        title="API Documentation",
        version="v1",
        url="/api-docs/swagger.json",
    )


async def swagger(app) -> None:
    swagger_info = app["swagger_dict"]
    dpath = Path(__file__).parent / "spec.md"
    with open(dpath.resolve()) as swagger_file:
        desc = swagger_file.read()
    swagger_info["info"]["description"] = desc
    setup_swagger(
        app=app,
        swagger_url="/api-docs",
        swagger_info=swagger_info,
        ui_version=3,
    )
