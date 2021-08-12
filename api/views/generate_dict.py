from _decimal import InvalidOperation
from decimal import Decimal

from aiohttp import web
from aiohttp_apispec import docs, response_schema
from api import schema


class GenerateDict(web.View):
    def get_digit(self, s):
        return "".join(filter(str.isdigit, s))

    def check_has_digit(self, s):
        return any(char.isdigit() for char in s)

    @docs(
        tags=["Generate dictionary"],
        summary="Generate dictionary",
        description="""
        {
            "<key(2N+1)>": "<value(2N+1)>",  # convert value(2N+1) to decimal or reversed string
            "<key(2N)>": "<value(2N)>",  # convert value(2N) to int or string
            "total_int": "<int_value>",
            "total_decimal": "<decimal_value>",
        }
        """,
    )
    @response_schema(
        schema=schema.GenerateDict(),
        code=200,
        description="Return success response with dict",
    )
    @response_schema(
        schema=schema.BadRequestSchema(),
        code=400,
        description="Return unsuccessful response with dict",
    )
    async def get(self) -> web.Response:
        """
        example input /api/v1/lets_dict/?key1=10&key2=12&key3=1440.66&key4=12233312
        """
        data = {}
        total_int = 0
        total_decimal = 0

        for k, v in self.request.rel_url.query.items():
            if self.check_has_digit(k):
                if int(self.get_digit(k)) % 2:
                    response_key = "<key({})>".format(self.get_digit(k))
                    try:
                        data[response_key] = str(Decimal(v))
                    except InvalidOperation:
                        raise web.HTTPBadRequest(reason="Unable to parse data.")
                    total_decimal += Decimal(v)
                else:
                    response_key = "<key({})>".format(self.get_digit(k))
                    try:
                        num = int(v)
                    except ValueError:
                        raise web.HTTPBadRequest(reason="Unable to parse data.")
                    data[response_key] = str(v)
                    total_int += num

        data["total_int"] = str(total_int)
        data["total_decimal"] = str(total_decimal)

        return web.json_response(data=data)
