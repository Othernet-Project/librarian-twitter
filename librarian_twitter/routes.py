from librarian_core.contrib.templates.renderer import view

from .twitter import HANDLE_RE


EXPORTS = {
    'routes': {'required_by': ['librarian_core.contrib.system.routes.routes']}
}


@view('twitter/twitter')
def list_feed(handle):
    handles = handle.split(' ')
    return({'handles': handles})


@view('twitter/twitter')
def main_feed():
    processed = list_feed('outernetforall')
    return processed


def routes(config):
    print('ADDING TWITTER ROUTE')
    return (
        ('twitter:default', main_feed, 'GET', '/twitter/', {}),
        ('twitter:list', list_feed, 'GET',
         '/twitter/<handle:re:{}>'.format(HANDLE_RE), {}),
    )
