+++
title = "Forks"
date = 2024-11-29
[extra]
author = "Pere Lev"
+++

## Concept

Before we begin: As always, my [task board][kanban] is available. It seems some
disk space problem is taking apart my VPS, including the SSL certs, so you
might get a warning about them being expired. I'm starting to wonder if it's a
good idea for me to find an arrangement where someone else manages the services
that I use. Like, I still want Nextcloud etc. etc. all the self-hosted appps I
use, I just don't want to be a sysadmin, and I'm ok with financially supporting
someone else who, unlike me, enjoys that work and is happy to be doing it.
Anyone has ideas?

The last post talked about issue tracker migration. This post is going to talk
about something quite similar - repository forks! Vervis never had them in the
UI until just now.

Here's a brief summary of how issue tracker migration works:

1. Each tracker publishes its data to make it available for copying
2. When you create a tracker, you can choose to fill it with a copy of another
   tracker's data

I added another piece on top:

- When the request for the new tracker (or repository or any other resource) is
  sent, and when it's fulfilled and the tracker gets created, the old tracker
  is notified on these events
- Therefore the tracker/resource tracks and lists its "children" i.e. resources
  created as copies of it - for repos, we call these children **forks**

And for repos specifically,

- Each repo publishes its F3 object, and of course its Git content for cloning
- When creating repo B as a fork of repo A, repo B `git fetch`es from repo A
- While tracker migration works only between remote trackers, repo forking can
  be done both local and remote

NOTE: The Git repo implementation in Vervis is still buggy - I intend to fix
the bugs in the 2025 roadmap - for this task I implemented and fixed just
enough pieces for repo creation and forking to work.

## Purpose

I often see people complain about the limitations of the fork-and-PR based
workflow. With forks being implemented into Vervis and ForgeFed, I imagine you
may be asking "Why are you imitating the limited GitHub workflow?"

Here's the answer: ForgeFed is a specification, not an application. It really
tries to be flexible. ForgeFed supports sending PRs via forks, branches and
simple patch files, which means the classic patch-sending flows are perfectly
possible as well. Forks in ForgeFed and Vervis aren't about imitating the GH
workflow - they're just a way to support easy migration, and track copies and
derivatives of content. The actual workflows are up to the specific forge.

For example, imagine that personal-forks-just-for-PRs had their own namespace.
Or that forking is allowed for easy copying and migration but isn't used for
PRs. It's really up to the actual forge software. As long as it implements the
ForgeFed event sequences, it can communicate with any other forge, even if
their UIs offer diffrent workflows.

## How to Use

Just like with issue tracker migration: When creating a repo, you can
optionally specify an existing repo URI - local or remote - and the new repo
will be created as a fork of the existing one.

Note that I tested this only for Git repos - expect (more) bugs for Darcs.

[This repository on the Fig instance](https://fig.fr33domlover.site/repos/W058b)
has been created as a fork of repo from the Grape instance. If you click it,
and then go to its *Forks* tab (which currently serves only a JSON object), you
can see the URI of the Fig repo listed as a known fork.

## Implementation

- [Repo: UI, Client and S2S preparations for Forking](https://codeberg.org/ForgeFed/Vervis/commit/9d6ca7e4a40091c004464044303b147d256eb0b6)
- [UI: Remote Actor: If it's a repo, display a Fork link](https://codeberg.org/ForgeFed/Vervis/commit/d4a9d847ec1b96fb5427f51284de7f87520aec73)
- [Vocab: Repo: Specify origin property](https://codeberg.org/ForgeFed/Vervis/commit/c6be86f8530dcbb3af82ed915067ade76238b111)
- [Repo: Serve F3 representation](https://codeberg.org/ForgeFed/Vervis/commit/86f01f93567e24f56f768677f8f9abc8cc9eeb62)
- [UI: Repo: Display fork origin repo](https://codeberg.org/ForgeFed/Vervis/commit/20a2ca87e569d4471903e603ac4355f3a232df18)
- [DB, UI, Vocab: Repo: Serve forks collection](https://codeberg.org/ForgeFed/Vervis/commit/f1adf3e3f23986bf6076f8ae4b8dd2456c94ae1f)
- [Factory-based Repo creation, with local and remote fork support](https://codeberg.org/ForgeFed/Vervis/commit/b5a59d6704160a59004e7fe74882f7a0c7212409)
- [S2S: Repo: Create: Record the fork attempt](https://codeberg.org/ForgeFed/Vervis/commit/b2e52eb466ed323912cc5769bd8c00606b4562ed)
- [S2S: Component: Accept: If it's a Factory accepting a Create, record the fork](https://codeberg.org/ForgeFed/Vervis/commit/8190b7ae9c289c7267daac8def1621c9ab6fa651)
- [UI: Factory: Allow to toggle repo support](https://codeberg.org/ForgeFed/Vervis/commit/6233863caf2f6533d0571215d74e1edb63621e67)

## Funding

I really want to thank NLnet for funding this work!

Our current grant is about to end, but we're also working on the roadmap of the
new grant, so exciting stuff is expected for 2025, more news soon :)

## See It in Action

This time I didn't record a video demo. If you want to play with things
yourself, you can create account(s) on the demo instances - [fig][], [grape][],
[walnut][] - and try creating repos and forks.

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
