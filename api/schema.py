from marshmallow import Schema, fields, EXCLUDE, validate


class SuccessSchema(Schema):
    result = fields.String()


class BadRequestSchema(Schema):
    error = fields.Integer()


class FibNumber(Schema):
    N = fields.Integer()


class FibNumbersList(Schema):
    fibonacci_sequence = fields.List(fields.Integer())


class GenerateDict(Schema):
    total_int = fields.String()
    total_deciaml = fields.String()


class BookSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=5, max=50))
    author_id = fields.Integer()

    class Meta:
        unknown = EXCLUDE
