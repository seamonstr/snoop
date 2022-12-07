from werkzeug.utils import import_string
import flask

# There's a hard requirement to explicitly publish the SQLAlchemy
# engine because any blueprint that declares a model needs to
# subclass db.engine.Model.  Hence, this hardcoded import.  The
# db extension will still be registered in the normal way by
# register_extensions()
from . import db


db = db.db


def register_extensions(app: flask.Flask):
    for ext in app.config.get("EXTENSIONS", []):
        mod = import_string(ext)
        app.logger.debug(f"Initialising extension {mod} from {ext}")
        mod.configure(app)
