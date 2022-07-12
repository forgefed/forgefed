# ForgeFed - Federation Protocol for Forge Services

Motivation
----------

Distributed version control systems (VCS) were created to allow maximal flexibility of project management structures and code hosting, in contrast to the client-server version control systems that were most widely used at the time, which denote one replica as the canonical master source.  Existing project management / code hosting websites (aka: forges) soon began supporting these, and some new ones sprung up as well; but even the new ones were modeled upon the centralized "hub" paradigm (star topology, in networking lingo), with a single canonical "upstream" parent replica, and all other replicas implicitly and permanently designated as "downstream" child replicas (aka: forks).  This type of website well serves the traditional purpose of facilitating release distribution, collaboration, and end-user participation; but at the expense of re-centralizing the naturally distributed VCS.

Indeed, although distributed version control systems such as Git have become widely accepted as the de-facto state-of-the-art, it is still (and for good reason) the standard practice that one replica will be designated, albeit logically by convention, as the canonical upstream source; so this retro-fitting of distributed VCS onto the traditional centralized model, is not often contested.  Philosophically speaking though, this has the consequence of casting all software development as intrinsically hierarchical in nature; which is often undesirable, as it is antithetical to truly free and open, non-hierarchical project management "structures" such as adhocracy.

The goal of the ForgeFed project is to support the familiar collaborative features of centralized web forges with a decentralized, federated design that, by fully embracing the mostly forgotten merits distributed VCS, does not rely on a single authoritative central host, does not impose a hierarchical master/fork collaboration structure, and can be self-hosted by anyone; with all such independent peers cooperating to form a larger logical network of inter-operable and correlated services.

ForgeFed is not a new type of forge.  In fact, that would be counter to the primary motivation:  maximizing user options, tools, and work-flow preferences.  There are many freely-licensed and feature-rich forges in existence already.  Instead, ForgeFed is a set of extensions to the ActivtyPub communication protocol, which can be retro-fitted onto existing forges, with minimal intrusion into the internal code-base, in order to become inter-operable with any other similarly equipped forge.  Because the majority of forge offer roughly the same conventional feature-set, features also shared with other project management tools (eg: trackers, mailing lists); they can all be made to inter-operate without "re-inventing the wheel".  By using ActivtyPub as the communication protocol, participating ForgeFed services will be naturally accessible from the wider "Fediverse" as well, for whichever sub-set of interactions that such non-forge hosts/clients may support.


Design Goals
------------

* Transparent authentication and collaboration across federated instances
* Participating servers and their repos may be either private access or public
* Users should never need to trust any server in the network other than their home-server
* Users should never need to send any login credentials to other participating servers
* Users should never need to run any JavaScript from other participating servers
* Users should be able to interact with foreign repos in all of the typical collaborative ways, just as if they had an account on each foreign host
* Most (or ideally all) collaborative interactions should be accessible with or without a web browser (e.g. via email, custom clients, etc)
* The preceding, closely related, three bullet points are intended to allow interfaces to be maximally customizable; so that for examples:
  - A) People who rely on accessibility features could run a home instance or client which is particularly well suited to screen readers
  - B) The cool kids can use or create snazzy CSS/JS websites for web browsers
  - C) Yet others could interact with the same services on a headless server using mutt


How It Works
------------

* Everyone can view repos on public hosts without logging in (just as you would expect)
* Users can create an account on any public instance or may host their own - (this server will be henceforth referred to as that user's "home-server")
* Users can create repos on their home-server only
* Users can fork foreign repos to their home-server without signing-in to the foreign host
* Users can open tracker issues, post comments and votes, subscribe to updates (eg: "watch", "follow"), endorse foreign repos (eg: "favorite", "star"), and send merge requests (eg: "pull-requests" or raw patches), all without signing-in to the foreign host
* All non-trivial user interaction with foreign hosts are mediated by the user's home-server
* Users never need to interact directly with any foreign host; though it is possible for it to appear transparently as if doing so, albeit indirectly in reality
* All of the above interactions will be possible with or without a web browser (e.g. via email or CLI clients)
* Any project management tools (eg: bug trackers, code-review tools, forums, mailing lists) can interact with the system by implementing parts of the protocol selectively (eg: 'tickets', 'merge-requests', 'activity-stream')
* Savvy admins and users can interact with the system by implementing parts of the protocol in custom services and clients
* Home-servers will vouch for the identity of their users using HTTP signatures
* Home-servers will verify the identity of foreign users against credentials supplied by that user's home-server
* Home-servers could optionally sign submissions to foreign hosts with the user's GPG key, such as commits and comments, and send the public key along with the submission for verification
* Home-servers could log actions of foreign users for display purposes (listing remote forks, listing remote subscribers, displaying validated signatures, etc), as phantom, non-login, "foreign" users in their database
* Home-servers should notify foreign hosts of events to which their local users are subscribed, so that they may notify their local users (e.g. on-site alerts, email alerts, activity-pub "toots")
* Home-servers should also periodically poll remote hosts, which host repos and/or users to which their users are subscribed, for events that may have been missed due to one of the servers being offline at the time of the event, in order to ensure maximal robustness

The preceding bullet point is intended to encourage people to self-host their own forge, even if they do not maintain any projects themselves, and even if they host their forge with a laptop. That allows interacting with the forge while offline, without missing any incoming federated events nor dropping outgoing federated events. This would also allow forges to implement advanced features such as push-mirroring and robustly synchronizing the entire data-set of remote repos or migrating the entire project to another forge; so that their users could interact with foreign forges in all of the expected ways, while offline and/or without ever contacting foreign hosts directly.


See [EXAMPLE_WORKFLOWS.md](EXAMPLE_WORKFLOWS.md) for some general ideas on how users could interact with the system.
