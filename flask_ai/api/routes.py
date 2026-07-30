from flask import Blueprint

from api.health import health
from api.prediction import predict
from api.explain import explain

api_bp = Blueprint(

    "api",

    __name__

)

api_bp.add_url_rule(

    "/health",

    view_func=health,

    methods=["GET"]

)

api_bp.add_url_rule(

    "/predict",

    view_func=predict,

    methods=["POST"]

)

api_bp.add_url_rule(

    "/explain",

    view_func=explain,

    methods=["POST"]

)