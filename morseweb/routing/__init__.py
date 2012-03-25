# routing rules

def add_routes(config, **settings):
    """Add routing rules"""
    config.add_route('user', '/api/user')
    
    config.add_route('encode', '/api/encode{ext}')
    config.add_route('decode', '/api/decode')

    config.add_route('soundcloud_callback', '/api/soundcloud/oauth-callback')
    config.add_route('soundcloud_connect', '/api/soundcloud/connect')

    return config
