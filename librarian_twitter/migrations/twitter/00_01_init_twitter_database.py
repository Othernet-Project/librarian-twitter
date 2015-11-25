SQL = """
create table tweets
(
    id varchar primary key not null,                -- ID
    handle varchar,                                 -- handle
    text text,                                      -- tweets content
    image varchar default '{}',                     -- image for the tweet
    created timestamp not null                      -- creation timestamp
);
"""


def up(db, conf):
    db.executescript(SQL)
