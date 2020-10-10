from flask_apispec import doc, marshal_with

from helpers import BaseResource, ErrorResponseSchema


@doc(tags=["COVID Contact Tracing"])
@marshal_with(ErrorResponseSchema, code=404)
@marshal_with(ErrorResponseSchema, code=422)
class TracingBaseResource(BaseResource):
    pass
