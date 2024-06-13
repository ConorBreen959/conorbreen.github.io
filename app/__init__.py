import logging
import os
import sys

from flask import Flask, redirect, request
from flask_alembic import Alembic
from flask_appbuilder import AppBuilder, Base
from flask_appbuilder.menu import Menu, MenuItem
from flask_mail import Mail

from .landing import MyIndexView
from .manager import seed_users


mail = Mail()
alembic = Alembic()
appbuilder = AppBuilder(indexview=MyIndexView, base_template="base_layout.html")


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    from .config import Config

    app.config.from_object(Config())

    logging.basicConfig(
        stream=sys.stdout,
        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
    )
    logging.getLogger().setLevel(logging.DEBUG)

    @app.before_request
    def check_url():
        allowed_domain = os.environ.get("ALLOWED_DOMAIN")
        if (
            app.config["FLASK_ENV"] in ["prod", "uat"]
            and allowed_domain not in request.url
        ):
            return redirect(allowed_domain, code=301)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models import db

    alembic.init_app(app, db)
    db.init_app(app)
    app.app_context().push()
    alembic.upgrade()
    mail.init_app(app)
    Base.query = db.session.query_property()
    appbuilder.init_app(app, db.session)

    if alembic.compare_metadata() and app.config["FLASK_ENV"] == "dev":
        alembic.revision("dev_migration")
        alembic.upgrade()
    seed_users()
    register_views()
    Menu.adjust_menu = adjust_menu
    appbuilder.menu.adjust_menu()
    MenuItem.is_active = is_active
    return app


def register_views():
    from app.views import (
        HomeView,
        HealthView,
        GraphView,
        CopernicusView
    )

    appbuilder.add_view_no_menu(HomeView())
    appbuilder.add_view_no_menu(HealthView())
    appbuilder.add_view(
        GraphView,
        "Graph View",
        icon="fa-table",
        category="Graphs",
        category_icon="fa-file-pdf-o"
    )
    appbuilder.add_view(
        CopernicusView,
        "Copernicus View",
        icon="fa-table",
        category="Graphs",
        category_icon="fa-file-pdf-o"
    )
    appbuilder.security_cleanup()


def adjust_menu(self):
    old_menu = self.menu
    new_menu = old_menu[1:]
    new_menu.append(old_menu[0])
    self.menu = new_menu


def is_active(self):
    if self.childs:
        for c in self.childs:
            if c.is_active():
                return True
    else:
        if request.path == self.get_url():
            return True
        else:
            if self.baseview:
                if request.blueprint == self.baseview.blueprint.name:
                    return True
    return False