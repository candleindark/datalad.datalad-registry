"""Blueprint for /
"""
import logging

from flask import Blueprint
from flask import redirect
from flask import url_for
from werkzeug.wrappers import Response

lgr = logging.getLogger(__name__)
bp = Blueprint("root", __name__, url_prefix="")


@bp.route("/")
def root() -> Response:
    return redirect(url_for("overview.overview"))
