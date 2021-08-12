from datetime import datetime

from aiohttp import web
from aiohttp_apispec import docs, response_schema
from api import schema


class GetCurrentTime(web.View):
    @docs(
        tags=["Current time"],
        summary="Display current time",
        description="Get current time and display in response",
    )
    @response_schema(
        schema=schema.SuccessSchema(),
        code=200,
        description="Return success response with dict",
    )
    @response_schema(
        schema=schema.BadRequestSchema(),
        code=400,
        description="Return unsuccessful response with dict",
    )
    async def get(self) -> web.Response:
        current_time = datetime.now().strftime("%H:%M:%S")
        return web.json_response({"result": str(current_time)})
