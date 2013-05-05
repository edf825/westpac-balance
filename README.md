Introduction
------------

A pair of quick and dirty scripts using Westpac NZ's undocumented `gobal` service, 'reverse engineered' [1] from their Cash Tank app. Does not store usernames or passwords.

Usage
-----

Running `gettoken.py` will ask you for your username and password, then you'll be presented with a list of your accounts. Only one account at a time can be hooked up for passwordless fetching. [2]

The script will write the authentication token [3] to `~/.westpac-token`.

Running the `updatebalance.py` script will write the balance of your nominated account to `~/.westpac-balance`.

Security
--------

As far as I can tell, this service only lets you check the balance of one nominated account. There is no write access, you can't see multiple accounts (not with the same device ID anyway. Hmm...). Assuming I'm corrent about all this, it should be completely safe to be storing the authentication token in plain text.

Note
----

I suspect that there can only be one token per device ID. It's probably worth changing the `deviceid` constant at the top of `gettoken.py` just in case.

I'm not a python guy
--------------------

If my python sucks, get over it.

Disclaimer
----------

I'm not affiliated with Westpac NZ in any way. This isn't an official thing of theirs, blah blah, et cetera.

[1] Yes yes, a charitable term for basically pointing my Android phone at burp.

[2] A list of accounts and balances _can_ be fetched using `listaccts.xml`, but it requires a username and password every time.

[3] Really just the end of a URL chock full of all the stuff you need to use anything.
