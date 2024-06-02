import os

from flask_appbuilder.const import AUTH_DB

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    FLASK_ENV = os.environ.get("FLASK_ENV")
    if FLASK_ENV in ["dev", "devtest"]:
        dotenv_path = f".env.{FLASK_ENV}"
        from dotenv import load_dotenv, find_dotenv

        load_dotenv(find_dotenv(dotenv_path))

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    TESTING = os.getenv("TESTING", "False").lower() == "true"
    WTF_CSRF_ENABLED = os.environ.get("WTF_CSRF_ENABLED", "True").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY")

    DATE_FORMAT = "%d %b, %Y"

    ERROR_LOG = "error.log"

    # ------------------------------
    # GLOBALS FOR APP Builder
    # ------------------------------
    # Uncomment to setup Your App name
    APP_NAME = os.environ.get("APP_NAME", "Conor Breen")
    APP_ICON = os.environ.get("APP_ICON", "/static/img/logo-colour.png")

    # ----------------------------------------------------
    # AUTHENTICATION CONFIG
    # ----------------------------------------------------
    # The authentication type
    AUTH_TYPE = AUTH_DB

    # Will allow user self registration
    AUTH_USER_REGISTRATION = True

    # The default user self registration role
    AUTH_USER_REGISTRATION_ROLE = "BaseUser"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Config for Flask-WTF Recaptcha necessary for user registration
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")

    # API access token expiry
    JWT_ACCESS_TOKEN_EXPIRES = 10

    # Flask-Mail Config
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_PORT = 587

    # Roles
    FAB_ROLES = {
        "Public": [
            ["MyIndexView", "menu_access"],
        ],
        "BaseUser": [
            ["UserDBModelView", "can_userinfo"],
            ["UserDBModelView", "userinfoedit"],
            ["UserDBModelView", "resetmypassword"],
            ["UserDBModelView", "can_edit"],
            ["ResetMyPasswordView", "can_this_form_get"],
            ["ResetMyPasswordView", "can_this_form_post"],
            ["UserInfoEditView", "can_this_form_get"],
            ["UserInfoEditView", "can_this_form_post"],
            ["HomeView", "can_user"],
        ],
        "SuperUser": [
            ["List Users", "menu_access"],
            ["Security", "menu_access"],
            ["UserDBModelView", "can_list"],
            ["UserDBModelView", "can_show"],
            ["UserDBModelView", "can_delete"],
            ["UserDBModelView", "resetpasswords"],
            ["ResetPasswordView", "can_this_form_get"],
            ["ResetPasswordView", "can_this_form_post"],
            ["Graph View", "menu_access"],
            ["GraphView", "can_landing"],
            ["GraphView", "can_this_form_get"],
            ["GraphView", "can_this_form_post"],
            ["GraphView", "can_show_graph"],
        ],
    }

    # ---------------------------------------------------
    # Image and file configuration
    # ---------------------------------------------------

    # The file upload folder, when using models with files
    UPLOAD_FOLDER = BASEDIR + "/app/static/uploads/"
