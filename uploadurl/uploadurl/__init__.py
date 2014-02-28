import logging
import os
from mediagoblin.tools.pluginapi import get_config, register_routes

_log = logging.getLogger(__name__)

PLUGIN_DIR = os.path.dirname(__file__)

def setup_plugin():
	_log.info("Plugin loading")
	config = get_config('uploadurl')
	if config:
		_log.info('%r' % config)
	else:
		_log.info("no config found continuing")

	register_routes(('upload', '/upload', 'uploadurl.views:upload_handler'))
	
hooks = {'setup': setup_plugin}
