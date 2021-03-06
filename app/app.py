import os
import logging
import sys

import flask

from flask_sslify import SSLify

from . import handlers
from . import redis_utils

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    level=logging.DEBUG,
    stream=sys.stderr,
)

ENV = os.environ.get("ENV", "PROD")

redis_url = os.environ.get("REDIS_URL", None)

redis = redis_utils.setup_redis(redis_url) if redis_url else None

app = flask.Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

if not ENV == "DEV":
    sslify = SSLify(app)

logger = app.logger

routes = [
	('/', 'index', handlers.pages.front_page, ['GET']),
	('/home', 'home', handlers.pages.home_page, ['GET']),
]

for path, endpoint, handler, methods in routes:
	app.add_url_rule(path, endpoint, handler, methods=methods)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500