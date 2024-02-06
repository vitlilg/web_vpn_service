from datetime import timedelta

from web_vpn_service.settings.environment import env

# Authorization
AUTH_TOKEN_CHARACTER_LENGTH = 40
AUTH_HEADER_PREFIX = 'Token'
AUTO_REFRESH = False
TOKEN_TTL = timedelta(hours=10)
MIN_REFRESH_INTERVAL = 60

MAX_FILES_SIZE_FOR_UPLOAD = 104857600
LIST_ACCEPTED_FILE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'pdf', 'docx', 'doc', 'txt', 'webp']

HOST_API_DOMAIN = env.str('HOST_API_DOMAIN', 'http://localhost:8000')
