from aiohttp import web
from aiohttp_apispec import docs, response_schema, request_schema
from api import schema


class GetFibonacci(web.View):
    @staticmethod
    def fib(n):
        num1, num2 = 1, 1
        for i in range(n - 1):
            num1, num2 = num2, num1 + num2
        return num1

    def get_fib_seq(self, num):
        i = 2
        fib_arr = [0, 1]
        if num < len(fib_arr):
            return fib_arr
        while i <= num:
            fib_arr.append(self.fib(i))
            i += 1
        return fib_arr

    @docs(
        tags=["Fibonacci sequence"],
        summary="Get Fibonacci numbers and display sequence in response",
        description="Get Fibonacci numbers that less that N, "
        "where N is number in request body(but max should be 1M)",
    )
    @request_schema(
        schema=schema.FibNumber(),
        required=True,
    )
    @response_schema(
        schema=schema.FibNumbersList(),
        code=201,
        description="Return success response with dict",
    )
    @response_schema(
        schema=schema.BadRequestSchema(),
        code=400,
        description="Return unsuccessful response with dict",
    )
    async def post(self) -> web.Response:
        data = await self.request.json()
        number = data.get("N")
        if number > 1000000:
            return web.json_response(
                {
                    "fibonacci_sequence": "Max number for Fibonacci sequence is 1 000 000."
                }
            )
        return web.json_response({"fibonacci_sequence": self.get_fib_seq(number)})
