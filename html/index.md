---
title: ForgeFed
---

ForgeFed is a **federation protocol for software forges** and code collaboration
tools for the software development lifecycle and ecosystem. This includes
repository hosting websites, issue trackers, code review applications, and more.
ForgeFed provides a common substrate for people to create interoperable code
collaboration websites and applications.

**Federation** means that these websites can interact, allowing the humans
using them to interact too, despite being registered on different websites. For
example, imagine you could host your Git repos anywhere you want, perhaps even
your own personal website, but still be able to open issues and submit pull
requests against other people's repos hosted elsewhere, without having to
create accounts on those other websites!

Without federation, we end up having to choose between:

- Centralizing into huge profit-oriented websites, where we're powerless
- Hosting our code on a small website where we're in control and freedom but
  isolated from the community

With federation, all the websites now communicate with each other to form
**a network and community of collaboration** in which we're all both free and
connected. It puts the power back into our hands to create tools and
collaborate in ways that are aligned with human needs, powerful and safe ways
that allow us to include everyone and that don't depend on some big company's
policies or some website suddenly shutting down. Let's create the future
together!

## How does it work?

ForgeFed is an [ActivityPub][] extension. ActivityPub is an actor-model based
protocol for federation of web services and applications.

It's a bit like e-mail, except the data sent is JSON objects (i.e. structured
computer-readable data), and not only humans have inboxes where they can be
contacted, but also repositories and issue trackers have inboxes through which
they can be remotely and safely interacted with.

On top of ActivityPub's vocabulary (common language for websites to use for
communicating) and protocol, ForgeFed defines new vocabulary terms related to
repositories, commits, patches, issues, etc. and the protocol for creating and
interacting with such objects across servers.

You can find more technical details in our [repository][Codeberg].

## Project status

The best way to keep track of our progress is to follow us on the [Fediverse][].
You can also join our chat using [Matrix][] or Libera.Chat at #forgefed.

## Implementations

- [Vervis][] is the reference implementation of ForgeFed. It serves as a demo
platform for testing the protocol and new features.
- [Forgejo][] is implementing federation.
- Pagure has an unmaintained [ForgeFed plugin][Pagure].

[ActivityPub]: https://www.w3.org/TR/activitypub/
[Codeberg]:    https://codeberg.org/ForgeFed/ForgeFed
[Fediverse]:   https://floss.social/@forgefed
[Matrix]:      https://matrix.to/#/#forgefed:libera.chat
[Vervis]:      https://vervis.peers.community/
[Forgejo]:     https://forgejo.org
[Pagure]:      https://pagure.io/forge-fed/forge-fed
