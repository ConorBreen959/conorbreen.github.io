from flask import g, url_for, redirect
from flask_appbuilder import IndexView, expose


# class MyIndexView(IndexView):
#     @expose("/")
#     def index(self):
#         user = g.user
#
#         if user.is_anonymous:
#             return redirect(url_for("AuthDBView.login"))
#         return redirect(url_for("HomeView.user"))

class MyIndexView(IndexView):

    @expose("/")
    def index(self):
        return self.render_template("index.html")


class MyBaseView(IndexView):
    index_template = "my_base.html"
