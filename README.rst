=================
librarian-twitter
=================

A GUI for displaying downloaded twitter feeds.

Installation
------------

The component has the following dependencies:

- librarian-core_
- librarian-content_

To enable this component, add it to the list of components in librarian_'s
`config.ini` file, e.g.::

    [app]
    +components =
        librarian_twitter

And to make the menuitem show up::

    [menu]
    +main =
        twitter

Configuration
-------------

``twitter.refresh_rate``
    The interval of performing checks for new tweets, specified in seconds.
    Example::

        [twitter]
        refresh_rate = 60

``twitter.tweetdir``
    A filesystem path where downloaded tweets can be found. Example::

        [twitter]
        tweetdir = .appdata/tweets/

Development
-----------

In order to recompile static assets, make sure that compass_ and coffeescript_
are installed on your system. To perform a one-time recompilation, execute::

    make recompile

To enable the filesystem watcher and perform automatic recompilation on changes,
use::

    make watch

.. _librarian: https://github.com/Outernet-Project/librarian
.. _librarian-core: https://github.com/Outernet-Project/librarian-core
.. _librarian-content: https://github.com/Outernet-Project/librarian-content
.. _compass: http://compass-style.org/
.. _coffeescript: http://coffeescript.org/


Testing Tweets Locally
----------------------

Familiarity with the Twitter API is advised, as it's the primary way of
obtaining twitter data.

Tweets are just like any other file, but they live in ``.appdata/tweets``. They 
also get deleted immediately after ingestion. Tweets are a json notation text 
file that use 5 keys in an array. The keys are::

======   =========================================
name     value
======   =========================================
date     Date of broadcast, `yyyy-mm-dd` format
handle   Name of person who tweeted without the @
id       Twitter ID of the tweet in question
text     Content of the tweet
time     Time the tweet occured, `hh:mm:ss` format
======   =========================================

An example tweet::

  {
      "date": "2015-03-17",
      "handle": "BreakingNews",
      "id": "577895032209960960",
      "text": "RT @breakingpol: Illinois Rep. Aaron Schock is resigning his seat in Congress - @politico http://t.co/sgCkJiSSyP",
      "time": "18:11:27"
  }

Images may be provided and must be named ``$tweet-id``.ext. For example, if i had an image for the above tweet, it would 
belong at the path ``.appdata/tweets/img/577895032209960960.png``
