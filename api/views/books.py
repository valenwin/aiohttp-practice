from json import JSONDecodeError

import sqlalchemy as sa
from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from marshmallow import ValidationError

from api import schema
from api.context_managers import session_manager
from api.models import Book
from api.schema import BookSchema


class BooksView(web.View):
    @docs(
        tags=["Books"],
        summary="Display list of Books",
        description="List of Books with data",
    )
    async def get(self):
        query = sa.select(Book).select_from(Book)
        async with session_manager() as session:
            result = tuple(
                {"id": i.id, "name": i.name}
                for i in (await session.execute(query)).scalars()
            )
        return web.json_response({"result": result})

    @docs(
        tags=["Books"],
        summary="Create Book",
        description="Create a new Books objects",
    )
    @request_schema(
        schema=schema.BookSchema()
    )
    @response_schema(
        schema=schema.BadRequestSchema(),
        code=400,
        description="Return unsuccessful response with dict",
    )
    async def post(self):
        try:
            request_data = await self.request.json()
        except JSONDecodeError:
            raise web.HTTPBadRequest(reason="Unable to parse data.")

        # Define validation schema
        book_schema = BookSchema()
        try:
            validated_data = book_schema.load(request_data)
            print(44, validated_data)
        except ValidationError:
            return web.json_response(
                book_schema.error_messages, status=web.HTTPBadRequest.status_code
            )

        query = sa.insert(Book).values(validated_data)
        async with session_manager() as session:
            result = await session.execute(query)
            print(result)

        return web.json_response({"result": request_data})
