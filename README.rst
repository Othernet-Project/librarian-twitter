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
