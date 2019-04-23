# ForgeFed - Federation Protocol for Forge Services

Motivation
----------

Git was created as a distributed version control system (VCS), in contrast to the VCS systems that were most widely used at the time, which denote one replica as the canonical upstream master source.  Existing project hosting websites (forges) soon began supporting git and some new ones sprung up as well; but even the new ones were modeled upon the traditional "hub" paradigm (star topology, in networking lingo); with a single canonical upstream replica and all other replicas implicitly and permanently designated as "forks".  This type of website well serves the traditional purpose of facilitating collaboration and end-user participation; but very much in discordance with the decentralized nature of Git.

Indeed, it is standard practice, even with Git, that one replica will be designated as the canonical upstream; so this retro-fitting of Git upon the tradition hub model is not often contested.  Philosophically speaking though, this has the consequence of casting all software projects and development teams as hierarchical in nature; which is often undesirable, as it is antithetical to truly open project "structures" such as adhocracy.

The goal of this project is to support the familiar collaborative features of the centralized web hosts with a decentralized, federated design that, like Git itself, does not rely on a central host, does not impose a hierarchical, master/fork collaboration structure, and can be self-hosted by anyone; with all such independent peers cooperating to form a larger logical network of inter-operable services.


Design Goals
------------

* Transparent authentication and collaboration across federated instances
* Participating servers may be private access or public
* Users should never need to trust any server in the network other than their home-server
* Users never send any login credentials to other participating servers
* Users should never need to run any JavaScript from other participating servers
* Users can interact with foreign repos in all of the typical collaborative ways, just as if they had an account on each foreign host
* Allow most (or ideally all) collaborative interactions with or without a web browser (e.g. via email, custom clients, etc)
* The preceding, closely related, two bullet points are intended to allow interfaces to be maximally customizable; so that for examples:
  - A) People who rely on accessibility features could run a home instance or client which is particularly well suited to screen readers
  - B) The cool kids can use or create snazzy CSS websites
  - C) Yet others could interact with the service on a headless server using mutt


How It Works
------------

* Everyone can view repos on public hosts without logging in (just as you would expect)
* Users can create an account on any public instance or may host their own - (this server will be henceforth referred to as the "home-server")
* Users never interact directly with any foreign host
* All users interaction with foreign hosts are mediated by the user's home-server
* Users can create repos on their home-server only
* Users can fork foreign repos to their home-server without signing-in to the foreign host
* Users can send merge requests, open tracker issues, post comments, subscribe to updates, and "star" foreign repos without signing-in to the foreign host
* All of the above interactions will be possible with or without a web browser (e.g. via email)
* Savvy admins and users can interact with the system by implementing the protocols in custom services and clients
* Participating hosts validate the identity of foreign users against that user's home-server
* Server instances will verify and vouch for the identity of it's users using HTTP signatures
* Instances can optionally send the user's GPG public key for verifying commits/comments
* Instances should notify foreign hosts of events to which their local users are subscribed, so that it may notify their local users (e.g. on-site alerts, email alerts)
* Instances should also periodically poll other instances for such events for maximal robustness


See [EXAMPLE_WORKFLOWS.md](EXAMPLE_WORKFLOWS.md) for some general ideas on how users could interact with the system.
