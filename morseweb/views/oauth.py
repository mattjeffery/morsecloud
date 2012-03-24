import urllib
import urllib2
import simplejson
import transaction

import pyramid.settings
import pyramid.security

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError

from ..models import DBSession
from ..models.user import User

CONNECT_URL = "https://soundcloud.com/connect"
TOKEN_URL = "https://api.soundcloud.com/oauth2/token"
USER_URL = "https://api.soundcloud.com/me.json"

def json_request(url, params, method='GET'):
    """Make a request and parse the response as json
    """
    if method == 'GET':
        request = urllib2.urlopen(url+"?"+urllib.urlencode(params))
    else:
        request = urllib2.urlopen(url, urllib.urlencode(params))

    return simplejson.load(request)

@view_config(route_name='soundcloud_callback')
def soundcloud_callback(request):
    """Handle the sound cloud oauth callback
    """
    settings = pyramid.settings.get_settings()
    if request.GET.get('error'):
        pass

    else:
        params = dict(client_id=settings.get('soundcloud.client.id'),
                      client_secret=settings.get('soundcloud.client.secret'),
                      redirect_uri=settings.get('soundcloud.redirect_uri'),
                      grant_type='authorization_code',
                      code=request.GET.get('code'))

        token = json_request(TOKEN_URL, params, 'POST')

        #upgrade_page['access_token']
        #upgrade_page['scope']

        scuser = json_request(USER_URL, dict(oauth_token=token['access_token']))

        # find existing user
        user = DBSession.query(User).get(scuser['id'])

        # start transaction
        with transaction.manager:
            if user is None:
                # create new user
                user = User(id=scuser['id'],
                            name=scuser['username'],
                            shortname=scuser['permalink'],
                            access_token=token['access_token'])
                DBSession.add(user)
            else:
                # update the oauth token
                user.access_token=token['access_token']

        response = Response(str(user))

        headers = pyramid.security.remember(request, user.id)
        response.headerlist.extend(headers)

        return response

@view_config(route_name='soundcloud_connect')
def soundcloud_connect(request):
    """Redirect to the soundcloud connect auth page
    """
    settings = pyramid.settings.get_settings()
    params = dict(client_id=settings.get('soundcloud.client.id'),
                  client_secret=settings.get('soundcloud.client.secret'),
                  redirect_uri=settings.get('soundcloud.redirect_uri'),
                  response_type='code',
                  scope='non-expiring')
    connect_url = CONNECT_URL+"?"+urllib.urlencode(params)
    raise HTTPFound(connect_url)
