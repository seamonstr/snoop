from werkzeug.utils import import_string
import flask


def register_blueprints(app: flask.Flask):
    bps = app.config.get("BLUEPRINTS")
    if bps is None:
        app.logger.warn("No blueprints configured; empty app.")
        return

    for bp in bps:
        module = import_string(bp)
        app.logger.debug(f"Registering blueprint {module} from {bp}")
        module.configure(app)
