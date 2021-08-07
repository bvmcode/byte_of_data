from flask import Blueprint, render_template

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def route_test() -> str:
    return render_template("main/test.html")
