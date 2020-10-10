from flask import Blueprint

bp_name = "tracing"
tracing_bp = Blueprint(bp_name, __name__, url_prefix="/")
