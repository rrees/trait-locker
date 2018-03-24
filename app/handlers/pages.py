import logging

import flask

logger = logging.getLogger(__name__)

def front_page():
	logger.info('Test')
	logger.debug('Debug level output')
	return flask.render_template('index.html')