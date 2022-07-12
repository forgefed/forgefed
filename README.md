# ForgeFed - Federation Protocol for Forge Services

<a href="https://codeberg.org/ForgeFed/ForgeFed">
    <img alt="Get it on Codeberg" src="https://codeberg.org/Codeberg/GetItOnCodeberg/media/branch/main/get-it-on-neon-blue.png" height="60">
</a>

---

[ForgeFed][] is a **federation protocol for software forges** and other web
services dealing with version control repositories, project tracking and other
aspects of the software development lifecycle and ecosystem. This includes
repository hosting websites, issue trackers, code review management
applications and more.

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

# How does it work?

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

# So how do I use it?

ForgeFed is a protocol, i.e. instructions for how websites can communicate with each other. For
forge federation to really happen, we need to code it into forge software. This
is still in progress, but there are demos and prototypes you can play with if
you're curious :-) See below for ways to get updates on the latest work on this.

# What's the status? Where do I talk with you and ask questions?

The ForgeFed protocol specification is on the [website][ForgeFed]. The website
is generated from the Markdown sources found in this repository. There are
links there to Matrix and IRC chat, our [forum][], issue tracker, list of
ForgeFed implementations and their status, and more. You can also follow our
progress on the [fediverse][Mastodon].

Come talk with us :-)

# How can I contribute?

There's so much variety of tasks to do! Come talk with us on the chat/forum.

More eyes going over the spec are always welcome! And feel free to open issue
if you notice missing details or unclear text or have improvement suggestions
or requests!

However, to maintain a manageable working environment, we do reserve the issue
tracker for *practical, actionable work items*. If you want to talk first to
achieve more clarity, we prefer you write to us on the [forum][] or chat, and
opening an issue may come later.

If you wish to join the work on the ForgeFed specification, here are some
technical but important details:

- We don't push commits to the master branch, we always open a pull request
- Pull requests making changes to the specification content must have at least
  2 reviews and then they wait for a cooldown period of 2 weeks during which
  more people can provide feedback, raise challenges and conflicts, improve the
  proposed changes etc.
- So if you wish to continuously participate in shaping the specification, it
  would be useful to go over the open PRs once a week or so, to make sure you
  have a chance to communicate your needs, ideas and thoughts before changes
  get merged into the spec

Important files in this repo to know about:

- The file `resources.md` lists which team members have access to which project
  resources, openness and transparency are important to us!
- The actual specification source texts are in the `spec/` directory
- JSON-LD context files are in the `rdf/` directory

# Repo mirrors

This repo is mirrored at:

* [ForgeFed on Notabug][notabug-repo]
* [ForgeFed on Pagure][pagure-repo]
* [ForgeFed on GitHub][github-repo]

# Website build instructions

    ./build.sh

# License

All artifacts produced by the ForgeFed work-group are freely available under
the [CC0 1.0 Universal (CC0 1.0) Public Domain Dedication][cc0]. All
contributions to the wiki must also be offered freely as such.

The ForgeFed logo was created by [iko][].

# Historical resources

ForgeFed started its life on a mailing list, [here's the archive][Mail].

The ForgeFed forum, now at a [new location][forum], used to be at
`talk.feneas.org`, the old forum and posts can be viewed via the Internet
Archive's [wayback machine][old-forum].

[ActivityPub]: https://www.w3.org/TR/activitypub/
[ForgeFed]:    https://forgefed.org
[Forum]:       https://socialhub.activitypub.rocks/c/software/forgefed
[Mail]:        https://framalistes.org/sympa/arc/git-federation
[Mastodon]:    https://floss.social/@forgefed
[Old-forum]:   https://web.archive.org/web/20210306224235/https://talk.feneas.org/c/forgefed/10

[notabug-repo]: https://notabug.org/peers/forgefed/
[pagure-repo]:  https://pagure.io/forge-fed/forge-fed
[github-repo]:  https://github.com/forgefed/forgefed

[cc0]: https://creativecommons.org/publicdomain/zero/1.0/
[iko]: https://iko.im/
