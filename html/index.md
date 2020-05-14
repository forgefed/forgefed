ForgeFed is an upcoming federation protocol for enabling interoperability
between version control services. It's built as an extension to the
[ActivityPub] protocol, allowing users of any ForgeFed-compliant service to
interact with the repositories hosted on other instances.

The goal of the project is to support all of the major activities connected to
project management, including bug reports, merge requests, and notifications
across instances.

This website serves as the authoritative source for finding up to date information
about the project.


# Why ForgeFed?

The current state of code collaboration is dominated by centralized, proprietary
platforms. Free alternatives to these platforms exist (for example [NotABug] and
[Pagure]) but they do not solve the problem of centralization.

This project tries to address exactly this problem. Our wish is to devise a free
and standardized mechanism for enabling collaboration across any version control
platform.


# Project status

The best way to keep track of our progress is to follow us on the
[Fediverse](https://floss.social/@forgefed). Our roadmap is
[here](https://notabug.org/peers/forgefed/issues/87).

We publish specification drafts, implement them in our reference
implementation, and publish demos that demonstrate ForgeFed federation
features. Demos we've published:

1. [Ticket comment federation demo](https://socialhub.network/t/vervis-ticket-comment-federation-demo/599), May 2019
2. [Federated opening of new tickets](https://talk.feneas.org/t/vervis-demo-2-federated-opening-of-new-tickets/78), July 2019
3. [Push activities and repo following](https://talk.feneas.org/t/vervis-demo-3-push-activities-and-repo-following/177), October 2019

*As of February 10, 2020*: we're working towards finishing and announcing
[**Draft 1**](https://notabug.org/peers/forgefed/milestones). Vervis, the
reference implementation, already supports federation of:

- Repository following
- Repository push notifications to followers
- New issue creation
- Issue commenting

What remains to implement (federate) for the draft:

- The *Create flow* of issue creation
- Sending a patch / merge request

We hope to start getting NLNet funding, and to implement ForgeFed in an
existing forge, [Pagure](https://pagure.io).


# Work group

Community and development discussions are conducted on the [ForgeFed Forum], with
informal, real-time collaboration often taking place on the #peers IRC channel on
freenode.
In order to be most widely adopted, we strive to assemble the most diverse and
representative group including: users, implementers, and various domain experts.
Anyone who is experienced with working on existing forges or federated "social"
services, and anyone with experience in writing technical specification documents
is encouraged to join the working group.

- [Working Group](https://talk.feneas.org/t/working-group-instructions/196)
- [Community Group](https://talk.feneas.org/t/monthly-community-review-round-instructions/192)


# Implementations

- *[Vervis]* is the reference implementation of ForgeFed. It serves as a demo
platform for testing the protocol and trying new features
- *[mcfi]* is another command line implementation for testing the protocol

# Project links

- [Issues tracker](https://notabug.org/peers/forgefed/issues)
- [Wiki](https://notabug.org/peers/forgefed/wiki)
- [Forum](https://talk.feneas.org/c/forgefed)
- [Funding plan](/funding-plan.html)
- Specifications:
    * [Behavior](/behavior.html)
    * [Modeling](/modeling.html)
    * [Vocabulary](/vocabulary.html)
- [dokk](https://dokk.org/ForgeFed)
- <a rel="me" href="https://floss.social/@forgefed">Fediverse</a>


[ActivityPub]:    https://www.w3.org/TR/activitypub/
[NotABug]:        https://notabug.org
[Pagure]:         https://pagure.io
[Vervis]:         https://dev.angeley.es/s/fr33domlover/r/vervis
[mcfi]:           https://notabug.org/zPlus/mcfi
[ForgeFed Forum]: https://talk.feneas.org/c/forgefed
