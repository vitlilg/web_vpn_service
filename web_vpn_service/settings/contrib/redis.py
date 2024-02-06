from web_vpn_service.settings.environment import env

REDIS_URL = env.str('REDIS_URL', 'redis://localhost:6379')
