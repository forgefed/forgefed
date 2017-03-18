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
* instances can optionally send the user's GPG public key for verifying commits/comments
* instances can optionally sign commits/comments automatically using the local GPG keychain
* instances will occasionally poll other instances for updates of issues to which their local users are subscribed in order to notify their local users (e.g. on-site alerts, email alerts) - delivery is determined by the notification settings controlled *entirely* by each user's home server


Example User Stories
--------------------

```
Background:
Given: that fred.org and barney.com are public instances implementing the protocol above
And: user 'fred' creates an account on fred.org
And: user 'barney' creates an account on barney.com
Then: user 'fred' is assigned the repo URL namespace 'fred.org/fred/'
And: user 'barney' is assigned the repo URL namespace 'barney.com/barney/'
Then: user 'barney' creates a repo 'barney.com/barney/barney-made-this'


Scenario: user forks a foreign repo
When: fred visits 'barney.com/barney/barney-made-this'
And: fred presses the 'fork' button
Then: fred is asked to enter (or select) the domain of his home server
When: fred indicates the domain of his home server as 'fred.org'
Then: fred is redirected to 'fred.org/login' which is a pass-through if he is already signed in
When: fred is authenticated
Then: the 'fred.org' server clones the 'barney-made-this repo' into fred's namespace
And: the 'fred.org' server posts a notification addressed to the 'barney.com' server indicating that user 'fred@fred.org' has forked the repo 'barney/barney-made-this'
And: fred is redirected to 'fred.org/fred/barney-made-this'
And: the web page at 'fred.org/fred/barney-made-this' indicates it's parent fork with a link to 'barney.com/barney/barney-made-this'
And: the web page at 'barney.com/barney/barney-made-this/forks'
indicates it's child fork with a link to 'fred.org/fred/barney-made-this'


Scenario: user posts a merge request on a foreign repo
Given: that fred has forked 'barney.com/barney/barney-made-this' as 'fred.org/fred/barney-made-this'
And: fred has pushed new commits to his 'barney-made-this' fork
And: fred visits 'fred.org/fred/barney-made-this'
When: fred presses the 'merge request' button
Then: the 'fred.org' server posts a notification addressed to the 'barney.com' server indicating that user 'fred@fred.org' has posted a merge request to the repo 'barney/barney-made-this'
And: the 'barney.com' server creates a 'PR' type issue (e.g. ID# '42')
And: the 'barney.com' server adds the event to an 'unseen-alerts' db array for user 'barney'
And: the 'barney.com' server optionally notifies barney per barney's preferences
And: fred is redirected to the 'PR' type issue at 'barney.com/barney/barney-made-this/issues/42'


Scenario: user posts a comment on a foreign repo issue
When: fred visits 'barney.com/barney/barney-made-this/issues/42'
And: fred fills the 'comment' textbox and presses the 'send' button
Then: fred is asked to enter (or select) the domain of his home server
When: fred indicates the domain of his home server as 'fred.org'
Then: fred is redirected to 'fred.org/login' which is a pass-through if he is already signed in
When: fred is authenticated
Then: the 'fred.org' server posts a notification addressed to the 'barney.com' server indicating that user 'fred@fred.org' has posted a comment to the repo issue at 'barney.com/barney/barney-made-this/issues/42'
And: the 'barney.com' server creates a new comment (e.g. ID# '2')
And: the 'barney.com' server adds the event to an 'unseen-alerts' db array for user 'barney'
And: the 'barney.com' server optionally notifies barney per barney's preferences
And: fred is redirected to the issue at 'barney.com/barney/barney-made-this/issues/42#comment-2'


Scenario: user receives notifications for important events
Given: user 'fred@fred.org' has posted a merge request to the repo 'barney/barney-made-this'
Then: the 'unseen-alerts' db array for user 'barney' contains a reference to the 'PR' type issue with ID# '42' as posted by user 'fred@fred.org'
And: barney optionally receives an email notification with a link to 'barney.com/barney/barney-made-this/issues/42'
When: barney logs into his home server 'barney.com'
Then: he sees a notification icon which is a link to 'barney.com/barney/barney-made-this/notifications'
When: barney visits 'barney.com/barney/barney-made-this/notifications'
Then: barney sees a link to the PR issue from user 'fred@fred.org' 'barney.com/barney/barney-made-this/issues/42'
```


NOTES / RFCs:

1. only the potentially confusing cross-server use-cases are addressed here - but not the most obvious straigt-forward cases such as "a user views their own fork" and "a user comments on their own fork" - those o/c can be added later if these stories become acceptance tests

2. all example workflows above are entirely atomic - e.g.
  * the obvious issue arises along with pre-emptable operations such as what if two merge requests exists with the same tartget branch and they are both accepted simulteneously from two different clients with write access to that repo (or otherwise two machines are pushing to the same branch simulteneously) - whatever the answer it must be sane - one of the clients push/merge must be rejected or a new branch created for one of them
  * the system can never be put into a insane state such as if fred posts an edit to a comment while barney (or fred) is deleting that same comment (or the entire repo) simulteneously on another machine - either the new edit is posted and then deleted - or the original comment is deleted first then the new edit is posted as a new comment - or the comment (or repo) is deleted first then fred gets an informative error
  * although not strictly an issue of atomicity - there is a somewhat related issue - if fred posts a merge request to barney's repo on a foreign server and barney deletes or rebases that branch either before the merge request arrives or after it is posted then the simplest thing to do would be to delete the merge request and it's issue also - or else if barney accepts the merge then the deleted branch (or some new one) would need to be recreated based on the closest common commit - also if the target branch is deleted or rebased after the merge is completed then the PR issue perhaps could also be deleted then because it is not clear whether the deleted commits should be kept in the db (never to be reaped as long as the orphaned PR issue is still accessible on the website) - to be clear, git would reap them after 30? days but i think sites such as gogs and github keep these orphaned commits for as long as some issue references them so that they can be viewed although the UI would never allow them to be merged - however, if the orphaned PR issue was not yet closed or if it is possible to re-opened it then it could remain viable to be merged a second time - this is something to think about because presumably the PR issue would live on the destination server which presumably would not have any reliable knowlege of any other forks (even the PR source itself may not exist at merge time) - so clearly the destination repo would need to actually perform the merge in advance at the moment the PR is sent and store it (conflicts and all) in a temporary branch (or however the backend handles it) until the actual merge is accepted or rejected or else there would be no way to present the diff without redirecting to the source server (indeed - it may not be possible to present the diff at all if the source repo is offline) - in all cases the system should be sane at all times - worst case: dummy users, commits, comments, etc and empty pages or JSON responses; but no segfaults or 404s, and no merge buttons that can not complete

3. all example workflows above are entirely autonomous - ie. regardless of which user initialtes an event or, which client is used, or which project is the source or target - the initialting user's home server mediates every interaction - all instances have full authority over their own data and zero authority over data onother instances

4. all example workflows above are entirely symetrical - ie. every occurance of 'fred' and 'fred's home server' could be replaced with 'barney' and 'barney's home server' with no loss of generality - no server has any more or less capability than or authority over any other

5. the "user forks a foreign repo" scenario above is a streamlined version of the one originally suggested that had fred press the "login" button on the foreign site - that immediately would be a source of confusion - no one will press the 'login' on a site where they know they have no credentials - it then had fred being redirected to a dummy page on his homeserver 'fred.org/remotes/barney.com/barney/barney-made-this' where he could then press the 'fork' button - that seems like a unnecessary redirect to an unnecessary page which represents data that the home server does not yet have - the user should be able to simply press the 'fork' button on the foreign site and be redirected immediately to the newly created fork on the home server (guarded by the pass-through login check)

6. the 'unseen-alerts' db array mentioned in the "user posts a merge request on a foreign repo" scenario is for example presented on the web page 'barney.com/barney/barney-made-this/notifications' and cleared when the user next visits the URL associated with each alert such as in the "user receives notifications for important events" story (issue #18)
