from datetime import date
from flask_appbuilder.forms import DynamicForm
from flask_wtf.file import FileRequired
from wtforms import FileField, DateField, SelectField


class DataUploadForm(DynamicForm):
    filename = FileField(
        "Filename",
        description="Upload Data File",
        validators=[FileRequired()],
    )


class CopernicusForm(DynamicForm):
    start_date = DateField("Start Date", default=date.today())
    end_date = DateField("End Date", default=date.today())
    objects = [
        ("", ""),
        ("Sun", "Sun"),
        ("Mercury", "mercury"),
        ("Venus", "venus"),
        ("Mars", "mars"),
        ("Jupiter", "jupiter"),
        ("Saturn", "saturn"),
    ]
    body = SelectField("Select Planetary Body", choices=objects)
