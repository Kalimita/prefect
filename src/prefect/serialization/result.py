from marshmallow import fields

from prefect.engine import result, results
from prefect.serialization.result_handlers import ResultHandlerSchema
from prefect.utilities.serialization import JSONCompatible, ObjectSchema, OneOfSchema


class GCSResultSchema(ObjectSchema):
    class Meta:
        object_class = results.GCSResult

    filepath = fields.String(allow_none=False)
    bucket = fields.String(allow_none=False)
    credentials_secret = fields.String(allow_none=True)


class PrefectResultSchema(ObjectSchema):
    class Meta:
        object_class = results.PrefectResult

    value = fields.String(allow_none=True)


class S3ResultSchema(ObjectSchema):
    class Meta:
        object_class = results.S3Result

    filepath = fields.String(allow_none=False)
    bucket = fields.String(allow_none=False)
    credentials_secret = fields.String(allow_none=True)


class ConstantResultSchema(ObjectSchema):
    class Meta:
        object_class = results.ConstantResult


class ResultSchema(ObjectSchema):
    class Meta:
        object_class = result.Result


class SafeResultSchema(ObjectSchema):
    class Meta:
        object_class = result.SafeResult

    value = JSONCompatible(allow_none=True)


class NoResultSchema(ObjectSchema):
    class Meta:
        object_class = result.NoResultType


class StateResultSchema(OneOfSchema):
    """
    Field that chooses between several nested schemas
    """

    # map class name to schema
    type_schemas = {
        "SafeResult": SafeResultSchema,
        "NoResultType": NoResultSchema,
        "GCSResult": GCSResultSchema,
        "PrefectResult": PrefectResultSchema,
        "S3Result": S3ResultSchema,
        "ConstantResult": ConstantResultSchema,
        "Result": ResultSchema,
    }
