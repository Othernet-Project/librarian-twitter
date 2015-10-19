from librarian_ui.paginator import Paginator

from squery import Select


HANDLE_RE = '.+'
SEL_TWEETS = Select(sets='tweets')
COUNT_TWEETS = Select('COUNT(*) as count', sets='tweets')


def retrieve_tweets(db, handle, pager):
    """ Takes a request context, a handle, and a pager and returns a list """
    offset, limit = pager.items
    q = SEL_TWEETS
    q.offset = offset
    q.limit = limit
    if handle != '':
        q.where = 'handle = {}'.format(handle)
    db.execute(q)
    return db.results



def twitter_count(db, handle):
    """ Queries the database and returns a count of tweets for the given handle """
    q = COUNT_TWEETS
    if handle != '':
        q.where = 'handle = {}'.format(handle)
    db.execute(q)
    return db.result[0]


def init_pager(request, count):
    # parse pagination params
    page = Paginator.parse_page(request.params)
    per_page = Paginator.parse_per_page(request.params)
    pager = Paginator(count, page, per_page)
    return pager
