# NotABug 2.0 Federated Project Management Network

Motivation
----------

Git was created as a distributed version control system (VCS), in contrast to the VCS systems that were most widely used at the time, which denote one replica as the canonical upstream master source.  Existing project hosting websites soon began supporting git and some new ones sprung up as well; but even the new ones were modelled upon the traditional "hub" paradigm; with a single canonical upstream replica and all other replicas implicitly and permantly relegated as "forks".  This type of website well serves the traditional purpose of facilitating collaboration and end-user participation; but not at all, in the decentralized spirit of Git.

Indeed, it is usually the case, even with Git, that one replica will be designated as the canonical upstream; so this retro-fitting of Git upon the tradition hub model is not often contested.  Philisphically speaking though, this has the consequence of casting all software projects and development teams as hierarchical in nature; which is often undesirable, as it is antithetical to truly open project "structures" such as adhocracy.

Furthermore, the centralized infrastructure, which in nearly all current public instances, is operated by a commercial third-party and contingent on it's profitability, is a liability to anyone relying on it for their long-term infrastructure.  Remember Google Code?

The goal of this project is to support the familiar collaborative features of the centralized web hosts with a decentralized design that, like Git itself, does not rely on a central host and can be self-hosted by anyone; with all such independent peers cooperating to form a larger logical network of inter-operable services.  Also, becasue this system is intended to be operated by anyone, even on modest hardware such as their personal computers, ultra efficiency and security are also high-priority goals.  For example, no long-running processes will be allowed; instead, all Git operations will be fully preemptible to prevent the "slow loris" bottle-necks; which are a serious limitation and security issue for existing self-hosted solutions such as Gogs, the system that NotABug is currently using.


Design Goals
------------

* transparent authentication and collaboration across federated instances
* participating servers may be private access or public
* server operators may be decide whether or not to allow public registrations
* installing a home-server should be trivial to setup and maintain
* licensing compliance should be trivial to maintain
* users should never need to trust any server in the network other than their home-server
* users never send any contact details to other participating servers
* users should never need to run any javascript from other participating servers
* fully API accessible - even the reference website (which will be the NotABug-2.0 front-end) will be just another API client - this would naturally allow for adapters to other services that expose a similar API such as github, gogs, and pagure
* users can interact with foreign repos in all of the typical collaborative ways just as if they had an account on each foreign host
* allow most (or ideally all) collaborative interactions with or without a web browser (e.g. via email, custom clients, etc)
* the preceding, closely related, three bullet points are intended to allow interfaces to be maximally customizable; so that for examples: A) people who rely on accessibility features could run a home instance which is particularly well suited to screen readers - B) the cool kids can use or create snazzy CSS websites - C) yet others could interact with the service on a headless server using mutt


How It Works
------------

* everyone can view repos on public hosts without logging in (just as you would expect)
* users can create an account on any public instance or may host their own - (this server will be henceforth referred to as your "home-server")
* users can create repos on their home-server only
* users can fork foreign repos to their home-server without logging in to the foreign host
* users can send merge requests, open issues, post comments, subscribe to updates, and "star" repos without logging in to the foreign host
* all of the above interactions will be possible with or without a web browser (e.g. via email)
* savvy admins can interact with the system by implementing the protocols in custom clients
* participating hosts validate the identity of foreign users against that user's home-server
* server instances will verify and vouch for the identity of it's users using the server SSL signature
* authentication is entirely based on bearer tokens that the foreign server can validate as being minted by the user's home-server
* instances can optionally send the user's GPG public key for verifying commits/comments
* instances can optionally sign commits/comments automatically on their user's behalf using a local GPG keychain
* instances will occasionally poll other instances for updates of issues to which their local users are subscribed in order to notify their local users (e.g. on-site alerts, email alerts) - delivery of such alerts is determined by the user-specified notification settings controlled *entirely* by each user's home-server


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
Then: fred is asked to enter (or select) the domain of his home-server
When: fred indicates the domain of his home-server as 'fred.org'
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
Then: fred is asked to enter (or select) the domain of his home-server
When: fred indicates the domain of his home-server as 'fred.org'
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
When: barney logs into his home-server 'barney.com'
Then: he sees a notification icon which is a link to 'barney.com/barney/barney-made-this/notifications'
When: barney visits 'barney.com/barney/barney-made-this/notifications'
Then: barney sees a link to the PR issue from user 'fred@fred.org' 'barney.com/barney/barney-made-this/issues/42'
```


NOTES / RFCs:

only some potentially confusing cross-server use-cases are addressed here - but not the most obvious straigt-forward cases such as "a user views their own fork" and "a user comments on their own fork" - those o/c can be added later if these stories become acceptance tests - feel free to add your own issues/questions/comments on the [wiki][wiki]

1. all example workflows above are entirely atomic - e.g.
  * the obvious issue arises along with pre-emptable operations such as what if two merge requests exists with the same tartget branch and they are both accepted simulteneously from two different clients with write access to that repo (or otherwise two machines are pushing to the same branch simulteneously) - whatever the answer it must be sane - one of the clients push/merge must be rejected or a new branch created for one of them
  * the system can never be put into a insane state such as if fred posts an edit to a comment while barney (or fred) is deleting that same comment (or the entire repo) simulteneously on another machine - either the new edit is posted and then deleted - or the original comment is deleted first then the new edit is posted as a new comment - or the comment (or repo) is deleted first then fred gets an informative error
  * although not strictly an issue of atomicity - there is a somewhat related issue - if fred posts a merge request to barney's repo on a foreign server and barney deletes or rebases that branch either before the merge request arrives or after it is posted then the simplest thing to do would be to delete the merge request and it's issue also - or else if barney accepts the merge then the deleted branch (or some new one) would need to be recreated based on the closest common commit - also if the target branch is deleted or rebased after the merge is completed then the PR issue perhaps could also be deleted then because it is not clear whether the deleted commits should be kept in the db (never to be reaped as long as the orphaned PR issue is still accessible on the website) - to be clear, git would reap them after 30? days but i think sites such as gogs and github keep these orphaned commits for as long as some issue references them so that they can be viewed although the UI would never allow them to be merged - however, if the orphaned PR issue was not yet closed or if it is possible to re-opened it then it could remain viable to be merged a second time - this is something to think about because presumably the PR issue would live on the destination server which presumably would not have any reliable knowlege of any other forks (even the PR source itself may not exist at merge time) - so clearly the destination repo would need to actually perform the merge in advance at the moment the PR is sent and store it (conflicts and all) in a temporary branch (or however the backend handles it) until the actual merge is accepted or rejected or else there would be no way to present the diff without redirecting to the source server (indeed - it may not be possible to present the diff at all if the source repo is offline) - in all cases the system should be sane at all times - worst case: dummy users, commits, comments, etc and empty pages or JSON responses; but no segfaults or 404s, and no merge buttons that can not complete

    [(click here to comment on RFC #1)][RFC-1]

2. all example workflows above are entirely autonomous - ie. regardless of which user initialtes an event or, which client is used, or which project is the source or target - the initialting user's home-server mediates every interaction - all instances have full authority over their own data and zero authority over data onother instances

    [(click here to comment on RFC #2)][RFC-2]

3. all example workflows above are entirely symetrical - ie. every occurance of 'fred' and 'fred's home-server' could be replaced with 'barney' and 'barney's home-server' with no loss of generality - no server has any more or less capability than or authority over any other

    [(click here to comment on RFC #3)][RFC-3]

4. the "user forks a foreign repo" scenario above is a streamlined version of the one originally suggested that had fred press the "login" button on the foreign site - that immediately would be a source of confusion - no one will press the 'login' on a site where they know they have no credentials - it then had fred being redirected to a dummy page on his homeserver 'fred.org/remotes/barney.com/barney/barney-made-this' where he could then press the 'fork' button - that seems like a unnecessary redirect to an unnecessary page which represents data that the home-server does not yet have - the user should be able to simply press the 'fork' button on the foreign site and be redirected immediately to the newly created fork on the home-server (guarded by the pass-through login check)

    [(click here to comment on RFC #4)][RFC-4]

5. the 'unseen-alerts' db array mentioned in the "user posts a merge request on a foreign repo" scenario is for example presented on the web page 'barney.com/barney/barney-made-this/notifications' and cleared when the user next visits the URL associated with each alert such as in the "user receives notifications for important events" story (issue #18)

    [(click here to comment on RFC #5)][RFC-5]


[wiki]:  https://notabug.org/NotABug.org/notabug-2.0/wiki
[RFC-1]: https://notabug.org/NotABug.org/notabug-2.0/wiki/rfc-1
[RFC-2]: https://notabug.org/NotABug.org/notabug-2.0/wiki/rfc-2
[RFC-3]: https://notabug.org/NotABug.org/notabug-2.0/wiki/rfc-3
[RFC-4]: https://notabug.org/NotABug.org/notabug-2.0/wiki/rfc-4
[RFC-5]: https://notabug.org/NotABug.org/notabug-2.0/wiki/rfc-5
