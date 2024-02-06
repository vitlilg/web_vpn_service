def ends_with_slash_in_link(link_url: str) -> str:
    slash = '' if link_url.endswith('/') else '/'
    return f'{link_url}{slash}'
