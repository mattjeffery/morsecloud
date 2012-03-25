import os

from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.renderers import JSONP

from .models import DBSession
from .routing import add_routes

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # load some config options from the env vars
    for option, value in settings.items():
        if value.startswith('$'):
            settings[option] = os.environ.get(value[1:])

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    authentication_policy = AuthTktAuthenticationPolicy(settings.get('auth.secret'))
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy,
                          settings=settings)

    config.add_renderer('jsonp', JSONP(param_name='callback'))

    config = add_routes(config, **settings)

    # static content
    config.add_static_view('', 'static/frontend', cache_max_age=3600)

    config.scan(".views")
    return config.make_wsgi_app()

