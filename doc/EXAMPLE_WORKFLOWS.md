Example User Stories
--------------------

Note that these are just some possible workflows implementations. Naturally, each forge is free to implement their interfaces, workflows, and as much of the ForgeFed spec as they see fit to honor and/or expose.

```
Background:
Given: 'fred.org' is Redmine tracker with VCS enabled, implementing the ForgeFed protocol partially
And:   'barney.net' is a complete forge, implementing the entire ForgeFed protocol
And:   'pebbles.me' is an Issue Tracker, implementing the ForgeFed protocol partially
Or:    'pebbles.me' is a Mastodon server, implementing the ForgeFed protocol minimally
Or:    'pebbles.me' is an email server, implementing the ForgeFed protocol minimally
Or:    'pebbles.me' is any custom peer, implementing the ForgeFed protocol minimally
And:   fred creates an account on 'fred.org'
And:   barney creates an account on 'barney.net'
And:   pebbles creates an account on 'pebbles.me'
And:   user 'fred' has permission to create new projects on 'fred.org'
Then:  user 'fred' is assigned the globally unique ForgeFed ID: 'fred@fred.org'
And:   user 'barney' is assigned the globally unique ForgeFed ID: 'barney@barney.net'
And:   user 'pebbles' is assigned the globally unique ForgeFed ID: 'pebbles@pebbles.me'
When:  barney creates a project: 'barney.net/barney/barney-made-this'
Then:  the following scenarios may apply


Scenario: user forks a foreign repo
Given: that fred is not logged into 'barney.net' as a registered user of 'barney.net'
When:  fred visits 'barney.net/barney/barney-made-this'
And:   fred presses the 'fork' button
Then:  fred is asked to enter (or select) the domain or IP of his home-server
When:  fred indicates the home-server as 'fred.org'
Then:  fred is redirected to 'fred.org/login' for authentication
When:  fred is authenticated
Then:  the 'fred.org' server creates a 'barney-made-this' project
And:   the 'fred.org' server clones the 'barney.net/barney/barney-made-this.git' repo as 'fred.org/barney-made-this/barney-made-this.git'
And:   the 'fred.org' server posts a request to the 'barney.net' server indicating that user 'fred@fred.org' has forked the repo 'barney/barney-made-this', which is accessible at the URL: 'fred.org/barney-made-this/barney-made-this.git'
When:  the 'barney.net' server receives the fork request from the 'fred.org' server
Then:  the web page at 'barney.net/barney/barney-made-this/forks' indicates fred's child fork, with a link to 'fred.org/barney-made-this'
And:   the 'barney.net' server posts a request to the 'fred.org' server, acknowledging the fork
When:  the 'fred.org' server receives the fork acknowledgment from the 'barney.net' server
Then:  fred is redirected to 'fred.org/barney-made-this'
And:   the web page at 'fred.org/barney-made-this' indicates it's parent fork, with a link to 'barney.net/barney/barney-made-this'


Scenario: user posts a merge request against a foreign repo
Given: that fred is logged into 'fred.org'
And:   fred is not logged into 'barney.net' as a registered user of 'barney.net'
And:   fred has forked 'barney.net/barney/barney-made-this' as 'fred.org/barney-made-this'
And:   fred has pushed new commits to the 'feature-branch' branch of his 'barney-made-this' fork
And:   fred visits 'fred.org/barney-made-this'
When:  fred presses the 'merge request' button
Then:  the 'fred.org' server posts a request to the 'barney.net' server indicating that user 'fred@fred.org' has posted a merge request against the repo 'barney/barney-made-this', and that the commit data is accessible at the URL: 'fred.org/barney-made-this/barney-made-this.git#feature-branch'
When:  the 'barney.net' server receives the MR request from the 'fred.org' server
Then:  the 'barney.net' server clones the repo 'fred.org/barney-made-this/barney-made-this.git', pending merge
And:   the 'barney.net' server creates a 'MR' type ticket (e.g. #42) as 'barney.net/barney/barney-made-this/issues/42'
And:   the 'barney.net' server posts a request to the 'fred.org' server, confirming that the request initiated by user 'fred@fred.org' to create a 'MR' type ticket was honored, and is accessible at the URL: 'barney.net/barney/barney-made-this/issues/42'
When:  the 'fred.org' server receives the MR acknowledgment from the 'barney.net' server
Then:  the 'fred.org' server replicates/mirrors the MR ticket #42 as 'fred.org/barney-made-this/42'
And:   fred is redirected to 'fred.org/barney-made-this/42'


Scenario: user posts a comment on a foreign ticket
Given: that pebbles's service is not a web server, but exposes 'pebbles.me/login' over HTTP, to authenticate her web browser session, with a callback redirect to attest such to the foreign forge
And:   a ticket exists at 'barney.net/barney/barney-made-this/issues/42'
When:  pebbles visits 'barney.net/barney/barney-made-this/issues/42'
And:   pebbles fills the 'comment' text-box and presses the 'send' button
Then:  pebbles is asked to enter the domain or IP of her home-server
When:  pebbles indicates the home-server as 'pebbles.me'
Then:  pebbles is redirected to 'pebbles.me/login' for authentication
When:  pebbles is authenticated
Then:  the 'pebbles.me' server posts a request to the 'barney.net' server indicating that user 'pebbles@pebbles.me' has posted a comment to the ticket at 'barney.net/barney/barney-made-this/issues/42'
When:  the 'barney.net' server receives the comment request from the 'pebbles.me' server
Then   the 'barney.net' server creates a new comment #420
And:   the 'barney.net' server posts a request to the 'pebbles.me' server confirming that the request initiated by user 'pebbles@pebbles.me' to create a ticket comment was honored, and is accessible at the URL: 'barney.net/barney/barney-made-this/issues/42#comment-420'
When:  the 'pebbles.me' server receives the comment acknowledgment from the 'barney.net' server
Then:  pebbles is redirected to the ticket comment at 'barney.net/barney/barney-made-this/issues/42#comment-420'

NOTE: that in the previous scenario pebbles's "server" is not necessarily a web server.
      "server" means only "ForgeFed-compatible service". In order for this scenario to work,


Scenario: user posts a comment on a foreign ticket, using own home-server only
Given: that fred is logged into 'fred.org'
And:   'fred.org/barney-made-this/' is a child fork of 'barney.net/barney/barney-made-this'
And:   fred visits 'fred.org/barney-made-this/42'
When:  fred fills the 'comment' text-box and presses the 'post' button
Then:  fred is optionally prompted for the remote fork, to which the comment should be posted
When:  the remote fork is decided to be 'barney.net' (it may be implicit, if only one known fork exists)
Then:  the 'fred.org' server posts a request to the 'barney.net' server indicating that user 'fred@fred.org' has posted a comment to the ticket at 'barney.net/barney/barney-made-this/issues/42'
When:  the 'barney.net' server receives the comment request from the 'fred.org' server
Then:  the 'barney.net' server creates a new comment #420
And:   the 'barney.net' server posts a request to the 'fred.org' server confirming that the request initiated by user 'fred@fred.org' to create a ticket comment was honored, and is accessible at the URL: 'barney.net/barney/barney-made-this/issues/42#comment-420'
When:  the 'fred.org' server receives the comment acknowledgment from the 'barney.net' server
Then   the 'fred.org' server replicates the comment #420 as 'fred.org/barney-made-this/42#comment-420'
And:   fred sees the new comment as 'fred.org/barney-made-this/42#comment-420'

NOTE: fred should not see the comment locally, unless/until barney.net acknowledges it
NOTE: fred may or may not be able to change the ticket state, edit/delete the comment, etc (the barney.net ACL governs that)
NOTE: that the previous scenario assumes that fred's issue tracker is a mirror,
      synchronized with barney's tracker - it could of course be local-only,
      independent of barney's tracker, in which case this scenario is not possible


Scenario: user posts a comment on a foreign ticket, without a web browser
Given: that pebbles's service is not a web server - it is a curl-based CLI client
And:   a ticket exists at 'barney.net/barney/barney-made-this/issues/42'
When:  pebbles fetches 'barney.net/barney/barney-made-this/issues'
Then:  pebbles sees a reference to 'barney.net/barney/barney-made-this/issues/42'
When:  pebbles selects that ticket, writes a comment, and saves the temporary file
Then:  the 'pebbles.me' server posts a request to the 'barney.net' server indicating that user 'pebbles@pebbles.me' has posted a comment to the ticket at 'barney.net/barney/barney-made-this/issues/42'
When:  the 'barney.net' server receives the comment request from the 'pebbles.me' server
Then   the 'barney.net' server creates a new comment #420
And:   the 'barney.net' server posts a request to the 'pebbles.me' server confirming that the request initiated by user 'pebbles@pebbles.me' to create a ticket comment was honored, and is accessible at the URL: 'barney.net/barney/barney-made-this/issues/42#comment-420'

NOTE: the astute reader will notice that this feature is ripe for spam;
      but the same would be the case if pebbles's service was webby.
      spam must always be anticipated in a publicly-writable federated system,
      which accepts "self-registration" from anyone, as most forges do.


Scenario: subscribed user receives notifications for important events
Given: the 'fred.org/barney-made-this' tracker is a synchronized replica of the 'barney.net/barney/barney-made-this' tracker
And:   pebbles has subscribed to the project: 'fred.org/barney-made-this'
And:   pebbles has also subscribed to the project: 'barney.net/barney/barney-made-this'
When:  fred adds a comment to ticket: 'fred.org/barney-made-this/barney-made-this/issues/42'
Then:  the 'fred.org' server posts a request to the 'barney.net' server indicating that user 'fred@fred.org' has posted a comment to the ticket at 'barney.net/barney/barney-made-this/issues/42'
When:  the 'barney.net' server receives the comment request from the 'fred.org' server
Then:  the 'barney.net' server creates a new comment #420
And:   the 'barney.net' server posts a request to the 'fred.org' server confirming that the request initiated by user 'fred@fred.org' to create a ticket comment was honored, and is accessible at the URL: 'barney.net/barney/barney-made-this/issues/42#comment-420'
And:   the 'barney.net' server posts a request to the 'pebbles.me' server indicating that user 'fred@fred.org' has posted a comment to 'barney.net/barney/barney-made-this/issues/42'
When:   the 'fred.org' server receives the comment acknowledgment from the 'barney.net' server
Then:  the 'fred.org' server posts a request to the 'pebbles.me' server indicating that user 'fred@fred.org' has posted a comment to 'fred.org/barney-made-this/42'
When:  pebbles logs into 'pebbles.me'
Then:  pebbles sees a link to or contents of the comment by user 'fred@fred.org' on 'fred.org/barney-made-this/42'
And:   pebbles sees a link to or contents of the comment by user 'fred@fred.org' on 'barney.net/barney/barney-made-this/issues/42'
And:   fred's comments, when viewed on 'fred.org/barney-made-this/42', will be denoted as "verified"
And:   if 'fred.org' has supplied a GPG key to 'barney.net' for user 'fred@fred.org', fred's comments, when viewed on 'barney.net/barney/barney-made-this/issues/42', will be denoted as "verified"
And:   if 'fred.org' has supplied a GPG key to 'pebbles.me' for user 'fred@fred.org', fred's comments, when viewed on locally,  will be verified locally
```
