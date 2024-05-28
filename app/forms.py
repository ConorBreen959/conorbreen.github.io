from flask_appbuilder.forms import DynamicForm
from flask_wtf.file import FileRequired
from wtforms import FileField


class DataUploadForm(DynamicForm):
    filename = FileField(
        "Filename",
        description="Upload Data File",
        validators=[FileRequired()],
    )
