# NotABug 2.0 Federated Project Management Network

Motivation
----------

Git was created as a distributed version control system, in contrast to the popular systems which denote one replica as the canonical upstream master source. Existing project hosting websites soon began supporting git and some new ones sprung up as well; but they all used the traditional "hub" paradigm that people were accustomed to. This type of website facilitates collaboration and end-user participation but is not at all in the spirit of git. The goal of this project is to support the familiar collaborative features of the centralized web hosts with a decentralized design that, like git itself, does not rely on a central host and can be self-hosted by anyone, with all such independent peers cooperating to form a larger logical network.


Design Goals
------------

* transparent authentication and collaboration across federated instances
* participating servers may be private access or public
* installing a home server and complying with licensing should be trivial to setup and maintain
* users should not need to trust any server in the network other than their home server
* users never send any contact details to, nor run any javascript on the other servers
* fully API accessible - even the reference website is just another client - this would naturally allow for adapters to other services that expose a similar API such as github
* users can interact with foreign repos in all of the typical collaborative ways just as if they had an account on each foreign host
* allow most or ideally all collaborative interactions without a web browser (e.g. custom clients or email)
* the closely related preceding three bullet points are intended to allow interfaces to be maximally customizable - so that, for example, people who rely on accessibility features could run a home instance which is particularly well suited to screen readers - the cool kids can use or create snazzy CSS websites - yet others could interact with the service on a headless server using mutt


How It Works
------------

* everyone can view repos on public hosts without logging in just as you would expect
* users can create an account on any public instance or may host their own
* users can create repos on their home server only
* users can fork foreign repos to their home server without logging in to the remote host
* users can send merge requests, open issues, post comments, subscribe to updates, and "star" repos without logging in to the remote host
* allow the above interactions without a web browser via email
* savvy admins can interact with the system by implementing the protocols in custom clients
* remote hosts validate the identity of foreign users with that user's home server
* instances will verify and vouch for the identity of it's users using the server SSL signature
* authentication is entirely based on bearer tokens that the foreign server can validate were minted by the user's home server
* instances can optionally send the user's GPG public key and/or sign comments with it
* instances will co-ordinate to notify their local users of updates to subscribed issues - delivery is determined by the notification settings controlled *entirely* by each user's home server


Example User Stories
--------------------

```
Background:
Given: that notabug.org and barney.com are public instances implementing the protocol above
And: user 'fred' creates an account on notabug.org
And: user 'barney' creates an account on barney.com
Then: user 'fred' is assigned the repo URL namespace 'notabug.org/fred/'
And: user 'barney' is assigned the repo URL namespace 'barney.com/barney/'
Then: user 'barney' creates a repo 'barney.com/barney/barney-made-this'


Scenario: user forks a foreign repo
When: fred visits 'barney.com/barney/barney-made-this'
And: fred presses the 'fork' button
Then: fred is asked to enter (or select) the domain of his home server 'notabug.org'
When: fred indicates the domain of his home server as 'notabug.org'
Then: fred is redirected to 'notabug.org/login' which is a pass-through if he is already signed in
When: fred is authenticated
Then: the 'notabug.org' server clones the 'barney-made-this repo' into fred's namespace
And: the 'notabug.org' server posts a notification addressed to the 'barney.com' server indicating that user 'fred@notabug.org' has forked the repo 'barney/barney-made-this'
And: fred is redirected to 'notabug.org/fred/barney-made-this'
And: the web page at 'notabug.org/fred/barney-made-this' indicates it's parent fork with a link to 'barney.com/barney/barney-made-this'
And: the web page at 'barney.com/barney/barney-made-this/forks'
indicates it's child fork with a link to 'notabug.org/fred/barney-made-this'


Scenario: user posts a merge request on a foreign repo
Given: that fred has forked 'barney.com/barney/barney-made-this' as 'notabug.org/fred/barney-made-this'
And: fred has pushed new commits to his 'barney-made-this' fork
And: fred visits 'notabug.org/fred/barney-made-this'
When: fred presses the 'merge request' button
Then: the 'notabug.org' server posts a notification addressed to the 'barney.com' server indicating that user 'fred@notabug.org' has posted a merge request to the repo 'barney/barney-made-this'
And: the 'barney.com' server creates a 'PR' type issue (e.g. ID# '42')
And: the 'barney.com' server adds the event to an 'unseen-alerts' db array for user 'barney'
And: the 'barney.com' server optionally notifies barney per barney's preferences
And: fred is redirected to the 'PR' type issue at 'barney.com/barney/barney-made-this/issues/42'


Scenario: user posts a comment on a foreign repo issue
When: fred visits 'barney.com/barney/barney-made-this/issues/42'
And: fred fills the 'comment' textbox and presses the 'send' button
Then: fred is asked to enter (or select) the domain of his home server 'notabug.org'
When: fred indicates the domain of his home server as 'notabug.org'
Then: fred is redirected to 'notabug.org/login' which is a pass-through if he is already signed in
When: fred is authenticated
Then: the 'notabug.org' server posts a notification addressed to the 'barney.com' server indicating that user 'fred@notabug.org' has posted a comment to the repo issue at 'barney.com/barney/barney-made-this/issues/42'
And: the 'barney.com' server creates a new comment (e.g. ID# '2')
And: the 'barney.com' server adds the event to an 'unseen-alerts' db array for user 'barney'
And: the 'barney.com' server optionally notifies barney per barney's preferences
And: fred is redirected to the issue at 'barney.com/barney/barney-made-this/issues/42#comment-2'


Scenario: user receives notifications for important events
Given: user 'fred@notabug.org' has posted a merge request to the repo 'barney/barney-made-this'
Then: the 'unseen-alerts' db array for user 'barney' contains a reference to the 'PR' type issue with ID# '42' as posted by user 'fred@notabug.org'
And: barney optionally receives an email notification with a link to 'barney.com/barney/barney-made-this/issues/42'
When: barney logs into his home server 'barney.com'
Then: he sees a notification icon which is a link to 'barney.com/barney/barney-made-this/notifications'
When: barney visits 'barney.com/barney/barney-made-this/notifications'
Then: barney sees a link to the PR issue from user 'fred@notabug.org' 'barney.com/barney/barney-made-this/issues/42'
```
