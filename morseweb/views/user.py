import pyramid.security

from pyramid.view import view_config

from ..models import DBSession
from ..models.user import User

@view_config(route_name='user', renderer='jsonp')
def user(request):
    """User details
    """
    user = None
    user_id = pyramid.security.authenticated_userid(request)
    if user_id:
        user = DBSession.query(User).get(user_id)

        return {'user': { 'id': user.id,
                          'shortname': user.shortname },
                "success": True }

    return {'user': None, "success": True }
