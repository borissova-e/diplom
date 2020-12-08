from urllib.parse import urlencode

def receive_tocken():
    OAUTH_URl = 'https://oauth.vk.com/authorize'
    APP_ID = 7666552

    OAUTH_PARAMS = {
        'client_id': APP_ID,
        'display': 'page',
        'scope': 'photos',
        'response_type': 'token',
        'v': 5.122
    }

    link_for_tocken = ('?'.join(
        (OAUTH_URl, urlencode(OAUTH_PARAMS))
    ))

    return link_for_tocken

if __name__ == '__main__':
    print(receive_tocken())
