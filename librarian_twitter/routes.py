import os

from bottle import request
from bottle_utils.i18n import i18n_url
from librarian_core.contrib.templates.renderer import view
from .twitter import (init_pager, retrieve_tweets, twitter_count, list_handles,
                      rows_to_dicts)


EXPORTS = {
    'routes': {'required_by': ['librarian_core.contrib.system.routes.routes']}
}


class Tweet(dict):
    def __init__(self, data, data_path):
        self.path = data_path
        self.data = data

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, key):
        return key in self.data

    def get(self, key):
        return self.data.get(key)

    @property
    def image_path(self):
        full_path = '/'.join([self.path, 'img',
                              self.data['id'] + self.data['image']])
        full_path = full_path.replace( '//', '/')
        return request.app.get_url('files:direct', path=full_path)



@view('twitter/twitter')
def twitter_list():
    """ List tweets based on query parameters """

    # TODO: Query param 'section' is now used that can be either 'tweets' or
    # 'handles'. When request is XHR, appropriate partial should be rendered.

    datadir = request.app.config['twitter.tweetdir']
    db = request.db['twitter']
    # parse search query
    handle = request.params.getunicode('h', '').strip()
    # get twitter count
    item_count = twitter_count(db, handle)
    pager = init_pager(request, item_count)
    tweets = retrieve_tweets(db, handle, pager)
    tweets = tweets
    handles = list_handles(db)

    tweet_count = len(tweets)
    tweet_list = (Tweet(t, datadir) for t in tweets)

    return dict(tweets=tweet_list,
                tweet_count=tweet_count,
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
