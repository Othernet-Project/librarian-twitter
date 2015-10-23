from bottle import request

from bottle_utils.i18n import i18n_url

from librarian_core.contrib.templates.renderer import view

from .twitter import init_pager, retrieve_tweets, twitter_count, list_handles,\
    rows_to_dicts


EXPORTS = {
    'routes': {'required_by': ['librarian_core.contrib.system.routes.routes']}
}


@view('twitter/twitter')
def twitter_list():
    """ List tweets based on query parameters """
    db = request.db['twitter']
    # parse search query
    handle = request.params.getunicode('h', '').strip()
    # get twitter count
    item_count = twitter_count(db, handle)
    pager = init_pager(request, item_count)
    tweets = retrieve_tweets(db, handle, pager)
    tweets = rows_to_dicts(tweets)
    handles = list_handles(db)
    return dict(tweets=tweets,
                handle=handle,
                handles=handles,
                pager=pager,
                vals=request.params.decode(),
                base_path=i18n_url('twitter'),
                view=request.params.get('view'))


def routes(config):
    return (
        ('twitter:list', twitter_list, 'GET', '/twitter/', {}),
    )
