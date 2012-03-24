import urllib
import urllib2
import simplejson
import logging

log = logging.getLogger(__name__)

def json_request(url, params, method='GET'):
    """Make a request and parse the response as json
    """

    log.debug("{0} request to {1} with params {2}".format(
                method, url, params))

    if method == 'GET':
        request = urllib2.urlopen(url+"?"+urllib.urlencode(params))
    else:
        request = urllib2.urlopen(url, urllib.urlencode(params))

    return simplejson.load(request)
