import logging
import tempfile

from urllib2 import urlopen, HTTPError, URLError

from mediagoblin.tools.response import json_response
from mediagoblin.submit.lib import get_upload_file_limits, submit_media, FileUploadLimit, UserUploadLimit, UserPastUploadLimit
from mediagoblin.plugins.api.tools import get_entry_serializable

_log = logging.getLogger(__name__)

def upload_handler(request):
	if request.GET.get('url') and request.GET.get('title') and request.user:
		upload_limit, max_file_size = get_upload_file_limits(request.user)
		try:
			f = urlopen(request.GET.get('url'))
			fname = request.GET.get('url')[request.GET.get('url').rfind('/')+1:]
			tmpfile = tempfile.NamedTemporaryFile()
			tmpfile.write(f.read)
			tmpfile.flush()
			local_file = open(tmpfile.name, "r")
			try:
				entry = submit_media(
					mg_app = request.app, user=request.user,
					submitted_file=local_file, filename=fname,
					title=request.GET.get('title'))
				entryinfo = get_entry_serializable(entry, request.urlgen)
				os.unlink(f.name)
				return json_response({'status':200, 'permalink':entryinfo['permalink']})
			except FileUploadLimit:
				return json_reponse({'status':400, 'error':'Past File size Upload Limit'})
			except UserUploadLimit:
				return json_response({'status':400, 'error':'Past User upload limit'})
			except UserPastUploadLimit:
				return json_response({'status':400, 'error':'Past upload limit'})
			except Exception as e:
				return json_response({'status':400, 'error':'Unspecified error'})

		except HTTPError as e:
			print("HTTP Error:", e.code, url)
			return json_response({'status':400, 'error':'unspecifice httperror'})
		except URLError as e:
			print("URL Error:", e.reason, url)
			return json_response({'status':400, 'error':'unspecified url error'})
	else:
		if not request.GET.get('url'):
			return json_response({'status':400, 'error':'No URL specified [GET, url]'})
		elif not request.GET.get('title'):
			return json_response({'status':400, 'error':'No title specified [GET, title]'})
		elif not request.user:
			return json_response({'status':401, 'error':'No user found'});
		else:
			return json_reponse({'status':400, 'error':'Unknown Error Occured'})
