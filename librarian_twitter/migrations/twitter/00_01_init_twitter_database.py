SQL = """
create table tweets
(
    handle varchar primary_key unique not null,     -- handle
    tweet text,                                     -- tweets content
    image varchar default '{}',                     -- image for the tweet
    created timestamp not null                      -- creation timestamp
);
"""


def up(db, conf):
    db.executescript(SQL)
