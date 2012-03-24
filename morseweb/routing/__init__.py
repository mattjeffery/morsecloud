# routing rules

def add_routes(config, **settings):
    """Add routing rules"""
    config.add_route('home', '/')
    
    config.add_route('soundcloud_callback', '/soundcloud/oauth-callback')
    config.add_route('soundcloud_connect', '/soundcloud/connect')

    return config
