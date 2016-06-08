import json
import logging

from sqlize_pg import Replace

from librarian.core.exts import ext_container as exts
from librarian.core.utils import to_datetime
from librarian.tasks import Task


IMPORT_QUERY = Replace('tweets',
                       constraints=('id',),
                       cols=('id', 'handle', 'text', 'image', 'created'))


class CheckTweetsTask(Task):

    def run(self):
        """
        Checks the configured tweetdir for .json files and creates an
        import_from_file task in the queue.
        """
        db = exts.databases['twitter']
        tweet_dir = exts.config['twitter.tweetdir']
        (success, dirs, files) = exts.fsal.list_dir(tweet_dir)
        for f in files:
            if f.path[-5:] == '.json':
                parse_json(f.path, db)
                logging.debug("Twitter: removing imported file: %s", f.path)
                exts.fsal.remove(f.rel_path)
            else:
                logging.debug('Twitter: not a json: {}'.format(f.path))

    @classmethod
    def install(cls):
        refresh_rate = exts.config['twitter.refresh_rate']
        if not refresh_rate:
            return
        exts.tasks.schedule(cls(), delay=refresh_rate, periodic=True)


def parse_json(path, db):
    """ Makes a note in the log, opens json file, and imports each tweet """
    logging.debug("Twitter: importing {}".format(path))
    with open(path) as f:
        import_tweets(json.load(f), db)


def convert_timestamp(sdate, stime):
    return to_datetime(' '.join([sdate, stime, 'UTC']))


def get_tweet_params(tweet):
    params = {
        'id': tweet['id'],
        'handle': tweet['handle'],
        'text': tweet['text'],
        'created': convert_timestamp(tweet['date'], tweet['time']),
    }
    try:
        params['image'] = tweet['img']
    except KeyError:
        params['image'] = None
    return params


def import_tweet(tweet, db):
    """ Takes tweet and imports it into the database """
    db.execute(IMPORT_QUERY, get_tweet_params(tweet))


def import_tweets(tweets, db):
    return db.executemany(IMPORT_QUERY, (get_tweet_params(t) for t in tweets))
