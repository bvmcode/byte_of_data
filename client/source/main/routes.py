from flask import Blueprint, render_template
from source.main.tasks import something

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def route_test() -> str:
    return render_template("main/test.html")

@main_blueprint.route("/foo")
def celery_test():
    task = something.delay()
    return 'hello world'
