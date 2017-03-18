# NotABug 2.0 Federated Version Control System

Motivation
----------

Git was created as a distributed version control system, in contrast to the popular systems which denote one replica as the canonical upstream master source. Existing project hosting websites soon began supporting git and some new ones sprung up as well; but they all used the traditional "hub" paradigm that people were accustomed to. This type of website facilitates collaboration and end-user participation but is not at all in the spirit of git. The goal of this project is to support the familiar collaborative features of the centralized web hosts with a decentralized design that, like git itself, does not rely on a central host and can be self-hosted by anyone, with all such independent peers cooperating to form a larger logical network.


Design Goals
------------

* transparent authentication and collaboration across federated instances
* federated servers may be private access or public
* installing a home server and complying with licensing should be trivial to setup and maintain
* users should not need to trust any server in the network other than their home server
* users never send any contact details to, nor run any javascript on the other servers
* users can interact with foreign repos in all of the typical collaborative ways just as if they had an account on each foreign host
* allow most or ideally all collaborative interactions without a web browser (e.g. custom clients or email)
* fully API accessible - even the reference website is just another client - this would naturally allow for adapters to other services such as github, pagure, gittea


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


Pending Ideas
-------------

still have to come up with a good ui to move to repositories on a different instance though - downside of this system is that url bars don't work entirely as you'd expect. You go to a third party site, you click the login button and you end up back at your home site's interface - this needs to be somewhat streamlined

for example - if you click a link to https://gits.cool-project.org and you hit the login button you end up back at notabug.org/remotes/cool-project.org on your 'home' interface - you can then fork and clone and comment as if it were on your home site - but I wonder if this is maybe confusing

the upside is you get to keep all your preferences across instances
the downside is that initially people may not expect this behavior
particularly people who rely on accessibility features may be helped a lot by this as they could run a home instance which is particularly well suited to screen readers

another upside is that not every implementer of the protocol will have to necessarily deal with ui for cross-site functionality for now I think that this can be fixed with some documentation/ui but if it turns out to be a disaster it can be changed to be more like others
