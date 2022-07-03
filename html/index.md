---
title: ForgeFed
---

ForgeFed is an upcoming federation protocol for enabling interoperability
between version control services. It's built as an extension to the
[ActivityPub] protocol, allowing users of any ForgeFed-compliant service to
interact with the repositories hosted on other instances.

The goal of the project is to support all of the major activities connected to
project management, including bug reports, merge requests, and notifications
across instances.


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
[here](https://codeberg.org/forgefed/forgefed/issues/87).
You can join our chat using [Matrix][] or on [Libera.Chat](https://libera.chat/) at #forgefed.

We publish specification drafts, implement them in our reference
implementation, and publish demos that demonstrate ForgeFed federation
features.

*As of June 2022*: After a long period of inactivity, new people are joining
the team and federation is being implemented in Gitea. There are also new
projects such as ForgeFriends, which are implementing ForgeFed.


# Implementations

- *[Vervis]* is the reference implementation of ForgeFed. It serves as a demo
platform for testing the protocol and trying new features
- [Gitea][] is implementing federation
- *[mcfi]* is another command line implementation for testing the protocol

# Project links

- [Issues tracker](https://codeberg.org/ForgeFed/ForgeFed/issues)
- [Forum](https://socialhub.activitypub.rocks/c/software/forgefed)
- [Funding plan](/funding-plan.html)
- Specifications:
    * [Behavior](/behavior.html)
    * [Modeling](/modeling.html)
    * [Vocabulary](/vocabulary.html)
- <a rel="me" href="https://floss.social/@forgefed">Fediverse</a>


[ActivityPub]:    https://www.w3.org/TR/activitypub/
[NotABug]:        https://notabug.org
[Pagure]:         https://pagure.io
[Vervis]:         https://dev.openheart.work/s/fr33domlover/r/vervis
[mcfi]:           https://notabug.org/zPlus/mcfi
[ForgeFed Forum]: https://talk.feneas.org/c/forgefed
[Gitea]:          https://gitea.io
[Matrix]:    https://matrix.to/#/#forgefed:libera.chat
