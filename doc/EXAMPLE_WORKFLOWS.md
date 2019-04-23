Example User Stories
--------------------

Note that these are just some possible workflows implementations. Naturally, each forge is free to implement their interfaces, workflows, and as much of the ForgeFed spec as they see fit to honor and/or expose.

```
Background:
Given: that fred.org and barney.net are public instances implementing the protocol above
And:   user 'fred' creates an account on fred.org
And:   user 'barney' creates an account on barney.net
And:   user 'pebbles' creates an account on pebbles.info
Then:  user 'fred' is assigned the globally unique ID: 'fred@fred.org'
And:   user 'barney' is assigned the globally unique ID: 'barney@barney.net'
And:   user 'pebbles' is assigned the globally unique ID: 'pebbles@pebbles.info'
Then:  user 'fred' is assigned the repo URL namespace 'fred.org/fred/'
And:   user 'barney' is assigned the repo URL namespace 'barney.net/barney/'
And:   user 'pebbles' is assigned the repo URL namespace 'pebbles.info/pebbles/'
Then:  user 'barney' creates a repo 'barney.net/barney/barney-made-this'


Scenario: user forks a foreign repo
When: fred visits the 'barney.net/barney/barney-made-this'
And:  fred presses the 'fork' button
Then: fred is asked to enter (or select) the domain of his home-server
When: fred indicates the domain of his home-server as 'fred.org'
Then: fred is redirected to 'fred.org/login' which is a pass-through if he is already signed in
When: fred is authenticated
Then: the 'fred.org' server clones the 'barney-made-this repo' into fred's namespace
And:  the 'fred.org' server posts a notification to the 'barney.net' server indicating that user 'fred@fred.org' has forked the repo 'barney/barney-made-this'
And:  fred is redirected to 'fred.org/fred/barney-made-this'
And:  the web page at 'fred.org/fred/barney-made-this' indicates it's parent fork with a link to 'barney.net/barney/barney-made-this'
And:  the web page at 'barney.net/barney/barney-made-this/forks' indicates that it's child fork with a link to 'fred.org/fred/barney-made-this'


Scenario: user posts a merge request on a foreign repo
Given: that fred has forked 'barney.net/barney/barney-made-this' as 'fred.org/fred/barney-made-this'
And:   fred has pushed new commits to his 'barney-made-this' fork
And:   fred visits 'fred.org/fred/barney-made-this'
When:  fred presses the 'merge request' button
Then:  the 'fred.org' server posts a notification to the 'barney.net' server indicating that user 'fred@fred.org' has posted a merge request to the repo 'barney/barney-made-this' and that the commit data is accessible at 'fred.org/fred/barney-made-this.git#feature-branch'
And:   the 'barney.net' server clones the repo 'fred.org/fred/barney-made-this.git#feature-branch'
And:   the 'barney.net' server validates the pending merge status
And:   the 'barney.net' server creates a 'PR' type issue
And:   the 'barney.net' server adds the event to an 'unseen-alerts' db array for user 'barney'
And:   the 'barney.net' server sends barney an email notification
And:   the 'barney.net' server posts a notification to the 'fred.org' server confirming that the request initiated by user 'fred@fred.org' to create a 'PR' type issue was honored, and is accessible at the URL: 'barney.net/barney/barney-made-this/issues/42'
And:   fred is redirected to the 'PR' type issue at 'barney.net/barney/barney-made-this/issues/42' (or perhaps fred's home-server implements it's fork's issues as a mirror of the upstream issues and directs fred to that URL - the beauty of federation is that, either implementation could be equivalent and transparent to users)


Scenario: user posts a comment on a foreign repo issue
Given: that an issue exists at 'barney.net/barney/barney-made-this/issues/42'
When:  fred visits 'barney.net/barney/barney-made-this/issues/42'
And:   fred fills the 'comment' textbox and presses the 'send' button
Then:  fred is asked to enter (or select) the domain of his home-server
When:  fred indicates the domain of his home-server as 'fred.org'
Then:  fred is redirected to 'fred.org/login' which is a pass-through if he is already signed in
When:  fred is authenticated
Then:  the 'fred.org' server posts a notification addressed to the 'barney.net' server indicating that user 'fred@fred.org' has posted a comment to the repo issue at 'barney.net/barney/barney-made-this/issues/42'
And:   the 'barney.net' server creates a new comment
And:   the 'barney.net' server adds the event to an 'unseen-alerts' db array for user 'barney'
And:   the 'barney.net' server sends barney an email notification
And:   the 'barney.net' server posts a notification to the 'fred.org' server confirming that the request initiated by user 'fred@fred.org' to create an issue comment was honored, and is accessible at the URL: 'barney.net/barney/barney-made-this/issues/42#comment-2'
And:  fred is redirected to the issue at 'barney.net/barney/barney-made-this/issues/42#comment-2'


Scenario: subscribed user receives notifications for important events
Given: that user 'pebbles@pebbles.info' has subscribed to the repo 'barney.net/barney/barney-made-this'
When:  user 'fred@fred.org' creates a merge request at 'barney.net/barney/barney-made-this/issues/42'
Then:  the 'barney.net' server posts a notification to the 'pebbles.info' server indicating that user 'fred@fred.org' has posted a merge request at 'barney.net/barney/barney-made-this/issues/42'
And:   the 'pebbles.info' server adds the event to an 'unseen-alerts' db array for user 'pebbles'
And:   the 'pebbles.info' server sends pebbles an email notification
When:  pebbles visits 'pebbles.info/pebbles/notifications'
Then:  pebbles sees a link to the PR issue from user 'fred@fred.org' 'barney.net/barney/barney-made-this/issues/42'
```
