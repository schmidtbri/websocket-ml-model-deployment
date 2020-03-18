"""Flask websocket application for hosting machine learning models."""
import os
import logging
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

from model_websocket_service.model_manager import ModelManager

# package metadata
__version_info__ = (1, 0, 0)
__version__ = '.'.join([str(i) for i in __version_info__])

logger = logging.getLogger(__name__)

app = Flask(__name__)

# this allows the application to be instantiated without any configuration for unit testing
if os.environ.get("APP_SETTINGS") is not None:
    app.config.from_object("model_websocket_service.config.{}".format(os.environ['APP_SETTINGS']))

bootstrap = Bootstrap(app)
socketio = SocketIO(app)


import model_websocket_service.endpoints   # noqa: E402
import model_websocket_service.views       # noqa: E402


@app.before_first_request
def instantiate_model_manager():
    """Run at application startup, loads all of the model found in the configuration."""
    logger.info("Loading models from configuration.")
    model_manager = ModelManager()
    model_manager.load_models(configuration=app.config["MODELS"])
    logger.info("Finished loading models from configuration.")


if __name__ == "__main__":
    socketio.run(app)
