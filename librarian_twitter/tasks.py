import json
import logging

from squery import Replace
from fsal.client import FSAL


def check_for_tweets(supervisor):
    """ Checks the configured tweetdir for .json files and creates an
        import_from_file task in the queue """
    config = supervisor.config
    db = supervisor.exts.databases['twitter']
    fsal_client = FSAL(config['fsal.socket'])
    (success, dirs, files) = fsal_client.list_dir(config['twitter.tweetdir'])

    for f in files:
        path = f.path
        if path[-5:] == '.json':
            parse_json(path, db)
            logging.debug("Twitter: removing imported file: {}".format(path))
            fsal_client.remove(path)
        else:
            logging.debug('Twitter: not a json: {}'.format(path))

    refresh_rate = supervisor.config['twitter.refresh_rate']
    supervisor.exts.tasks.schedule(check_for_tweets,
                                   args=(supervisor,),
                                   delay=refresh_rate,
                                   periodic=False)


def parse_json(path, db):
    logging.debug("Twitter: importing {}".format(path))
    for tweet in json.load(open(path)):
        import_tweet(tweet, db)


def import_tweet(tweet, db):
    q = Replace('tweets', cols=('id', 'handle', 'text', 'image', 'created'))
    params = {
        'id': tweet['id'],
        'handle': tweet['handle'],
        'text': tweet['text'],
        'created': tweet['time'],
    }
    try:
        params['image'] = tweet['img']
    except KeyError:
        params['image'] = None

    db.execute(q, params)
