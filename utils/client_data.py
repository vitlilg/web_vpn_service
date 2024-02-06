def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_device_info(request):
    user_agent = getattr(request, 'user_agent', None)
    if not user_agent:
        return ''
    if not (user_agent.device.brand and user_agent.device.model):
        device = user_agent.get_device()
    else:
        device = f'{user_agent.device.brand} {user_agent.device.model}'
    os = f'{user_agent.os.family} {user_agent.os.version_string}'
    browser = f'{user_agent.browser.family} {user_agent.browser.version_string}'
    return f'{device}; {os}; {browser}'
