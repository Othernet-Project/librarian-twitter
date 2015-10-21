from librarian_ui.paginator import Paginator

from squery import Select


HANDLE_RE = '.+'
TWEET_Q = Select(sets='tweets')
HANDLE_Q = Select('DISTINCT handle', sets='tweets')
COUNT_Q = Select('COUNT(*) as count', sets='tweets')


def rows_to_dicts(row_list):
    dict_list = []
    for tweet in row_list:
        dict_list.append(
            {
                'id': tweet[0],
                'handle': tweet[1],
                'tweet': tweet[2],
                'img': tweet[3],
                'timestamp': tweet[4],
            }
        )
    return dict_list


def retrieve_tweets(db, handle, pager):
    """ Takes a request context, a handle, and a pager and returns a list """
    offset, limit = pager.items
    q = TWEET_Q
    q.offset = offset
    q.limit = limit
    if handle != '':
        q.where = "handle like :handle"
    db.query(q, handle=handle)
    return db.results


def list_handles(db):
    q = HANDLE_Q
    db.execute(q)
    return db.results


def twitter_count(db, handle):
    """ Queries the database and returns a count of tweets for the given handle """
    q = COUNT_Q
    if handle != '':
        q.where = "handle like :handle"
    db.query(q, handle=handle)
    return db.result[0]


def init_pager(request, count):
    # parse pagination params
    page = Paginator.parse_page(request.params)
    per_page = Paginator.parse_per_page(request.params)
    pager = Paginator(count, page, per_page)
    return pager
