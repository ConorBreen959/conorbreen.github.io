import pandas as pd

from flask import g, render_template, jsonify, request, redirect, url_for
from flask_appbuilder import BaseView, SimpleFormView, has_access, expose
from flask_appbuilder.widgets import ListWidget
from flask_login import current_user

from app import appbuilder
from app.forms import DataUploadForm, CopernicusForm
from app.utils.flexible_visualisation import build_graph
from app.utils.copernicus import calculate_retrogrades


class CopernicusWidget(ListWidget):
    template = "widgets/copernicus_form.html"


class CopernicusView(SimpleFormView):
    route_base = "/copernicus"
    form = CopernicusForm
    form_title = "Copernicus"
    edit_widget = CopernicusWidget

    @expose("/show/", methods=("GET", "POST"))
    def show_graph(self):
        g = calculate_retrogrades(2010, "mars")
        return jsonify(render_template("graph.html", graph=g, title="Retrograde"))


class GraphWidget(ListWidget):
    template = "widgets/graph_form.html"


class GraphView(SimpleFormView):
    route_base = "/graph"
    form = DataUploadForm
    form_title = "Flexible Graphing"
    edit_widget = GraphWidget

    @expose("/show/", methods=("GET", "POST"))
    def show_graph(self):
        lims_file = request.files["filename"]
        filename = lims_file.filename.split(".")[0]
        title = " ".join(filename.split("_")).title()
        data = pd.read_csv(lims_file)

        g = build_graph(data)
        return jsonify(render_template("graph.html", graph=g, title=title))


class HomeView(BaseView):
    route_base = "/home"

    @has_access
    @expose("/user/")
    def user(self):
        user = g.user

        if user.is_anonymous:
            return redirect(url_for("AuthDBView.login"))
        greeting = f"Hello {current_user}"
        return self.render_template("logged_user.html", greeting=greeting)


class HealthView(BaseView):
    route_base = "/health"

    @expose("/check/")
    def check(self):
        greeting = "Hello World"
        return self.render_template("logged_user.html", greeting=greeting)


@appbuilder.app.after_request
def add_header(response):
    response.cache_control.private = True
    response.cache_control.public = False
    response.headers["Cache-Control"] = "no-store, max-age=0"
    return response


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )
