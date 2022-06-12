ASGI_APPLICATION = 'biblishelf_web.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('192.168.99.1', 6379)],
        },
    },
}