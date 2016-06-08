from bottle_utils.i18n import i18n_url
from streamline import TemplateRoute

from librarian.core.contrib.templates.renderer import template
from librarian.core.exts import ext_container as exts

from .twitter import init_pager, retrieve_tweets, twitter_count, list_handles


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
        full_path = full_path.replace('//', '/')
        return i18n_url('files:direct', path=full_path)


class TwitterList(TemplateRoute):
    """
    List tweets based on query parameters.
    """
    name = 'twitter:list'
    path = '/twitter/'
    template_name = 'twitter/twitter'
    template_func = template

    def get(self):
        # TODO: Query param 'section' is now used that can be either 'tweets'
        # or 'handles'. When request is XHR, appropriate partial should be
        # rendered.
        datadir = self.config['twitter.tweetdir']
        db = exts.databases['twitter']
        # parse search query
        handle = self.request.params.getunicode('h', '').strip()
        # get twitter count
        item_count = twitter_count(db, handle)
        pager = init_pager(self.request, item_count)
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
                    vals=self.request.params.decode(),
                    base_path=i18n_url('twitter'),
                    view=self.request.params.get('view'))
