# routing rules

def add_routes(config, **settings):
    """Add routing rules"""
    config.add_route('user', '/api/user')
    config.add_route('play', '/api/play.aiff')
    
    config.add_route('soundcloud_callback', '/api/soundcloud/oauth-callback')
    config.add_route('soundcloud_connect', '/api/soundcloud/connect')

    return config
