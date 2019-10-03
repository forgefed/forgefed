ForgeFed is a federation protocol for enabling interoperability between version
control services. It's built as an extension to the [ActivityPub] protocol,
allowing users of any ForgeFed-compliant service to interact with the repositories
hosted on other instances.

The goal of the project is to support all of the major activities connected to
project management, including bug reports, merge requests, and notifications
across instances.

This website serves as the official place where to find up to date information and
links about the project.


# Why ForgeFed?

The current state of code collaboration is dominated by centralized, proprietary
platforms. Free alternatives to these platforms exist (for example [NotABug] and
[Pagure]) but they do not solve the problem of centralization.

This project tries to address exactly this problem. Our wish is to devise a free
and standardized mechanism for enabling collaboration across any version control
platform.


# Project status

The specification and software produced but this working group is still in the
early stages, and there is still much work to do and ample design-space for
discussion and contributions.

So far the protocol supports:

- repository following
- repository push notifications to followers
- new issue creation


# Work group

Community and development discussions are conducted on the [ForgeFed Forum], with
informal, real-time collaboration often taking place on the #peers IRC channel on
freenode.
In order to be most widely adopted, we strive to assemble the most diverse and
representative group including: users, implementers, and various domain experts.
Anyone who is experienced with working on an existing forges or federated "social"
services, and anyone with experience in writing technical specification documents
is encouraged to join the work-group and/or contribute artifacts.


# Implementations

- *[Vervis]* is the reference implementation of ForgeFed. It serves as a demo
platform for testing the protocol and trying new features
- *[mcfi]* is another command line implementation for testing the protocol

# Project links

- [Issues tracker](https://notabug.org/peers/forgefed/issues)
- [Wiki](https://notabug.org/peers/forgefed/wiki)
- [Forum](https://talk.feneas.org/c/forgefed)
- [Specification](/forgefed-vocabulary.html)
- [dokk](https://dokk.org/ForgeFed)


[ActivityPub]:    https://www.w3.org/TR/activitypub/
[NotABug]:        https://notabug.org
[Pagure]:         https://pagure.io
[Vervis]:         https://dev.angeley.es/s/fr33domlover/r/vervis
[mcfi]:           https://notabug.org/zPlus/mcfi
[ForgeFed Forum]: https://talk.feneas.org/c/forgefed
