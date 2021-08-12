from aiohttp import web
from aiohttp_apispec import docs, response_schema
from api import schema


class CheckNameView(web.View):
    @docs(
        tags=["Name"],
        summary="Display name from URL",
        description="Get name from url and display in response",
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
        return web.json_response({"result": self.request.match_info.get("name")})
