+++
title = "Issue Tracker Migration"
date = 2024-10-31
[extra]
author = "Pere Lev"
+++

## Data Migration

Before we begin: As always, my [task board][kanban] is available.

Data migration, in this context, is my ability as the user, to copy or move my
data from one server to another server on the network. Often in web
applications this service isn't offered, and causes what's often called *vendor
lock-in*: I'm stuck with the server I chose, and whoever is managing and
hosting it.

What if my current server is shutting down? Or what if the terms of use are
changing? It's really a fundamental part of *data freedom*, the ability to
download my data and continue using it in a new place. I don't start over; I
rather *continue*, with the very same data, just on a new server.

Migrating repositories is the easier part: You can always `git clone` a repo,
and `git push` it somewhere else. But how to do the same with the other kinds
of project data?

## Vocabulary, Format, Process

I decided to use the [F3][] format for representing project data. At the time
of writing, it's slightly incomplete, so I added a little extension:

- An `IssueTracker` object
- The `Issue` object has a comments property
- The `Comment` object has a children property
- I picked a content type, `application/f3+json`

This way the entire data of the tracker can be represented as a single JSON
object (another option might be to download each object separately, or provide
a `.tar.gz` containing the directory tree of issues and comments).

Run this command to see some example data:

```sh
curl 'https://grape.fr33domlover.site/decks/OZLdZ' -H 'Accept: application/f3+json'
```

On the ForgeFed side, I picked the AS2 `origin` property, to represent the
source from which migration is or was done. So, when creating a new
project/tracker/etc., specifying the `origin` is the way to request migration.

The process is quite simple:

- (Currently) every tracker servers a F3 version of its data
- The newly created tracker downloads the data and creates local copies, and
  links pointing back to the originals

I added a switch in Vervis settings, to make migrations opt-in, since this
feature could probably be abused easily.

## Other Project Data

So, issue migration is now available in Vervis! But what about the other kinds
of project data:

- Repository
- Pull Request
- Project (i.e. a collection of such components)

With the foundations in place, these will come in the near future :) I suspect
the least trivial one is PRs, which is why I'm adding it to my 2025 roadmap.
Repo and project are easier, and I hope they come in 2025 as well.

## Implementation

Here's a summary of the changes I made in Vervis:

- Added a switch in the settings, as mentioned above
- In the DB, in UI and in the ForgeFed vocabulary: Tracker, issue and comment
  optionally specify their origin object
- When a `Factory` is asked to create a new tracker with an origin, it creates
  the tracker, and then sends it a message requesting it to download the data
  from that origin and create copies
- When a tracker is created, it optionally downloads the origin data and makes
  copies

And here's a list of commits:

- [Comment: Serve a F3 representation (without child comments)](https://codeberg.org/ForgeFed/Vervis/commit/c0636505674a81fc579dd920d317c14661710200)
- [Deck: Ticket: Serve F3 (without the tree of comments)](https://codeberg.org/ForgeFed/Vervis/commit/a38645f7526b531b629e422484db0effa229c59f)
- [DB: Message, Ticket: Specify origin (i.e. source of migration)](https://codeberg.org/ForgeFed/Vervis/commit/19f0b79226342c7a30d89b30b48e21ef27fa902d)
- [DB: Resource: Specify origin actor](https://codeberg.org/ForgeFed/Vervis/commit/99cbc5bd36cbf80d05783a64195bc9475b21bf31)
- [Vocab: Origin property for Deck, Ticket, Message (still set to none)](https://codeberg.org/ForgeFed/Vervis/commit/6e61871914f32aa9ed0ac218c489d95c014b8b3f)
- [Message: When serving AS2/FF object, specify origin](https://codeberg.org/ForgeFed/Vervis/commit/f588e1bbe013ab9720190067017ada9f2abd825c)
- [Deck: Ticket: When serving AS/FF, provide origin](https://codeberg.org/ForgeFed/Vervis/commit/decbb433376e46ee007731ba3a919617232bf096)
- [Deck: When serving AS2/FF, provide origin](https://codeberg.org/ForgeFed/Vervis/commit/0f0dcb2f01e46062666fe98961990a425492ce08)
- [UI: Deck: Display migration origin](https://codeberg.org/ForgeFed/Vervis/commit/dc4d7c309474c7c3f51cdef182afda5c557c741e)
- [UI: Deck: Ticket: Display migration origin](https://codeberg.org/ForgeFed/Vervis/commit/6dbdb4236677300374518ca197224850aa3fe229)
- [UI: Discussion: Display message migration origins](https://codeberg.org/ForgeFed/Vervis/commit/d4ed27fd181faad563f73788ecbae64eaf595bc8)
- [Deck: Serve F3 object, including issues & full comment trees](https://codeberg.org/ForgeFed/Vervis/commit/8913d5ca68d043520792f79b69d127a9fe31c51b)
- [Settings: Option to toggle support for Deck origin](https://codeberg.org/ForgeFed/Vervis/commit/6a7977e80c675b69a6697241e68319355afd2b47)
- [C2S: Allow new actor origin only if settings switch is on](https://codeberg.org/ForgeFed/Vervis/commit/9a3411c6164bc6e83bd908a9e5d6239c1fcf2939)
- [S2S: Deck: Upon creation, copy issues & comments from remote origin](https://codeberg.org/ForgeFed/Vervis/commit/1b08e3d8092ec80ae86e18588950a46695381c67)
- [S2S: Deck: Init: Insert MessageOrigin records by parsing F3 comment index](https://codeberg.org/ForgeFed/Vervis/commit/55992ac2e747abbfd408be281dee41bd26e7a3bb)
- [S2S: Factory: Create{Deck}: If origin specified, ask deck to use it](https://codeberg.org/ForgeFed/Vervis/commit/715f3e0eb8ee646592efa9187e29b3447b92be19)
- [UI: Create Deck: Allow to specify origin URI](https://codeberg.org/ForgeFed/Vervis/commit/35a390b6d64e086864b262949d9cb8f56c0e9694)

## Funding

I really want to thank NLnet for funding this work! The extended grant is
allowing me to continue backend work, and allowing André to work on the
[Anvil][] frontend.

## See It in Action

I recorded a little demo of all this! [Watch it on my PeerTube
instance](https://tube.towards.vision/w/rApKtzfDFiVa4JDbRt4GkN).

If you want to play with things yourself, you can create account(s) on the demo
instances - [fig][], [grape][], [walnut][] - and try the things I've mentioned
and done in the video.

If you encounter any bugs, let me know! Or [open an
issue](https://codeberg.org/ForgeFed/Vervis/issues)

## Comments

Come chat with us on
[Matrix](https://matrix.to/#/#general-forgefed:matrix.batsense.net)!

And we have an account for ForgeFed on the Fediverse:
<https://floss.social/@forgefed>

Right after publishing this post, I'll make a toot there to announce the post,
and you can comment there :)

[kanban]: https://todo.towards.vision/share/lecNDaQoibybOInClIvtXhEIFjChkDpgahQaDlmi/auth?view=kanban
[Vervis]: https://codeberg.org/ForgeFed/Vervis
[Anvil]: https://codeberg.org/Anvil/Anvil
[F3]: https://f3.forgefriends.org
[fig]: https://fig.fr33domlover.site
[grape]: https://grape.fr33domlover.site
[walnut]: https://walnut.fr33domlover.site
