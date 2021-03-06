==========
FriendlyDB
==========

``friendlydb`` is a small & fast following/followers database written in
Python. It can be either used directly from your Python code or over HTTP
with small web API.

FriendlyDB isn't meant to be a full user system; it should be used to augment
an existing system to track relationships.


Usage
=====

Using FriendlyDB from Python looks like::

    from friendlydb.db import FriendlyDB

    # Give Friendly a directory to work in.
    fdb = FriendlyDB('/usr/data/friendly')

    # Grab a user by their username.
    daniel = fdb['daniel']

    # Follow a couple users.
    daniel.follow('alice')
    daniel.follow('bob')
    daniel.follow('joe')

    # Check the following.
    daniel.following()
    # Returns:
    # [
    #     'alice',
    #     'bob',
    #     'joe',
    # ]

    # Check joe's followers.
    fdb['joe'].followers()
    # Returns:
    # [
    #     'daniel',
    # ]

    # Unfollow.
    daniel.unfollow('bob')

    # Check the following.
    daniel.following()
    # Returns:
    # [
    #     'alice',
    #     'joe',
    # ]

    # Dust off & nuke everything from orbit.
    fdb.clear()

Using FriendlyDB from HTTP looks like (all trailing slashes are optional)::

    # In one shell, start the server.
    python friendlydb/server.py -d /tmp/friendly

    # From another, run some URLs.
    curl -X GET http://127.0.0.1:8008/
    # {"version": "0.5.0"}

    curl -X GET http://127.0.0.1:8008/daniel/
    # {"username": "daniel", "following": [], "followers": []}

    curl -X POST http://127.0.0.1:8008/daniel/follow/alice/
    # {"username": "daniel", "other_username": "alice", "followed": true}
    curl -X POST http://127.0.0.1:8008/daniel/follow/bob/
    # {"username": "daniel", "other_username": "bob", "followed": true}
    curl -X POST http://127.0.0.1:8008/daniel/follow/joe/
    # {"username": "daniel", "other_username": "joe", "followed": true}

    curl -X POST http://127.0.0.1:8008/daniel/unfollow/joe/
    # {"username": "daniel", "other_username": "joe", "unfollowed": true}

    curl -X GET http://127.0.0.1:8008/daniel/
    # {"username": "daniel", "following": ["alice", "bob"], "followers": []}

    curl -X GET http://127.0.0.1:8008/daniel/is_following/alice/
    # {"username": "daniel", "other_username": "alice", "is_following": true}

    curl -X GET http://127.0.0.1:8008/alice/is_followed_by/daniel/
    # {"username": "alice", "other_username": "daniel", "is_followed_by": true}

    curl -X GET http://127.0.0.1:8008/alice/is_followed_by/joe/
    # {"username": "alice", "other_username": "joe", "is_followed_by": false}


Requirements
============

* Python 2.6+
* (Optional) gevent for the HTTP server
* (Optional) unittest2 for running tests


Installation
============

Only from this github repo using pip, or cloning


Performance
===========

You can scope out FriendlyDB's performance for yourself by running the
included ``benchmark.py`` script.

In tests on a 2011 MacBook Pro (i7), the benchmark script demonstrated:

* created 1,000,000 relationships between 10,000 users: 7.3 minutes
* avg time to fetch a user's followers: 0.0008 seconds
* never exceeding 40Mb of RAM RSS


Running Tests
=============

``friendlydb`` is maintained with passing tests at all times. Simply run::

    python -m unittest2 tests


Notes
=============

This is a forked/patched version of the original as licensed below. The original has now been converted to support Redis rather than file-based storage, so this repo reverts those changes to allow file-based storage to be used. And the approach to file-based storage included a bug where the number of subdirectories in friendlydb/ exceeds the subdirectory limit of 32,000 under ext3. This has been fixed in this repo.

https://github.com/toastdriven/friendlydb/issues/2

These revisions are not backwards compatible without converting any existing directory structure. Included is a template Django command script to be adapted to suit any applications which need to be converted from the old directory structure to this patched version. The conversion script has worked for me, but it is written in a very basic way.



License
=======

New BSD license.

:author: Daniel Lindsley
:version: 0.5.0
:date: 2012-01-30
