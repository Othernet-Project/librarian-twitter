import json
import logging

from sqlize_pg import Replace
from librarian_core.contrib.databases.serializers import DateTimeDecoder


IMPORT_QUERY = Replace('tweets',
                       constraints=('id',),
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
            fsal_client.remove(path)
        else:
            logging.debug('Twitter: not a json: {}'.format(path))

    # Schedule next run
    refresh_rate = supervisor.config['twitter.refresh_rate']
    supervisor.exts.tasks.schedule(check_for_tweets,
                                   args=(supervisor,),
                                   delay=refresh_rate,
                                   periodic=False)


def parse_json(path, db):
    """ Makes a note in the log, opens json file, and imports each tweet """
    logging.debug("Twitter: importing {}".format(path))
    import_tweets(json.load(open(path), cls=DateTimeDecoder), db)


def get_tweet_params(tweet):
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
    return params


def import_tweet(tweet, db):
    """ Takes tweet and imports it into the database """
    import_query = db.Replace(
        'tweets', constraints=('id',),
        cols=('id', 'handle', 'text', 'image', 'created'))
    db.execute(import_query, get_tweet_params(tweet))


def import_tweets(tweets, db):
    db.executemany(IMPORT_QUERY, (get_tweet_params(t) for t in tweets))
