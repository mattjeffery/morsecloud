import os

from pyramid.config import Configurator
from sqlalchemy import engine_from_config

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

    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    add_routes(config, **settings)

    config.scan()
    return config.make_wsgi_app()

