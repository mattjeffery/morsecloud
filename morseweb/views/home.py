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


@view_config(route_name='home')
def home(request):
    """
        Home page
    """
    user = None
    user_id = pyramid.security.authenticated_userid(request)
    if user_id:
        user = DBSession.query(User).get(user_id)

    return Response(str(pyramid.security.authenticated_userid(request)))
