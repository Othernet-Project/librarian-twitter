import json
import logging

from sqlize import Replace
from librarian_core.utils import to_datetime


IMPORT_QUERY = Replace('tweets',
                       cols=('id', 'handle', 'text', 'image', 'created'))


def check_for_tweets(supervisor):
    """ Checks the configured tweetdir for .json files and creates an
        import_from_file task in the queue """
    config = supervisor.config
    db = supervisor.exts.databases['twitter']
    fsal_client = supervisor.exts.fsal
    (success, dirs, files) = fsal_client.list_dir(config['twitter.tweetdir'])

    for f in files:
        path = f.path
        if path[-5:] == '.json':
            parse_json(path, db)
            logging.debug("Twitter: removing imported file: {}".format(path))
            fsal_client.remove(f.rel_path)
        else:
            logging.debug('Twitter: not a json: {}'.format(path))


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
