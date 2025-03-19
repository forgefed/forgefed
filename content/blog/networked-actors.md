+++
title = "Networked Actors"
date = 2025-01-28
[extra]
author = "Pere Lev"
+++

## New Year, New Work

So, what's new for ForgeFed in 2025?

- The previous NLnet grant is about to close (we had an extension but I'm happy
  to say we've used all the funding we received)
- We're about to sign the new grant, which is going to have a slightly
  different focus than before:
    * User research, gather the needs of forge federation developers
    * Figure out a path to get some federated collaboration in the real world,
      e.g. by getting Forgejo instances to federate issues (but more likely:
      Implement a (possibly simplified version of) ForgeFed OCAPs first)
    * Organize the spec and add human friendly documentation and API specs
    * Anvil frontend work
    * And yes, some Vervis development will continue
    * And yes, some Playwright actor system research will continue as well

This post is about the Playwright actor programming system, which now features
networking!

As always, my [task board][kanban] is available.

## The Previous Step - Relics

I've been giving nicknames to the layers of the actor system. In the previous
tasks I created 2 primary layers:

- Fly: General-purpose actor threads that receive messages
- Relic: A persistence layer on top of Fly

So, what we've had is a transparently disk-backed actor system! Since each
actor has its own thread, this system is actually meant for *Vats* rather than
individual actors. The actual actor part will come on top.

The next step on my plan was to add networking.

## The New Layer - Goose

*Goose* actors are a layer on top of *Relic*, which adds transparent networking
support. It currently uses plain TCP, without authentication. Each node on the
network has a host+port pair, and a TCP server that receives call requests and
inserts them into the local actor queues.

Goose actors use 2 types of Relics:

1. Each Goose type *g* is implemented using a Relic *GooseWrap g*
2. There's a specific new Relic type called *Remote*, used for calling methods
   of remote actors

Actor networking introduces 2 new pieces of the system:

1. Needing to maintain a map of local actors, so that the TCP server can look
   them up and insert calls to their queues
2. Tracking the *Remote* actors as well, so that actor mentions that appear in
   method arguments can be converted into live references

For this I added a `RelicMap` feature to the `Relic` module, for tracking local
actors. And in `Goose` there's a `RemoteTreasureMap` that tracks `Remote`
actors.

It's also possible for Goose actors to convert references between the data form
and the live actor form, which allows to copy and paste actors references and
connect actors on different machines!

There's no actual network protocol yet - I hope to use OCapN for that. At this
point, simple Haskell types are being used, along with their textual
serialization - one for method invocation and the other for reporting the
result. That's it.

But all of this may seem like hand waving. So I implemented a chat demo, to
show you the system in action :)

Here's the actual work:

- The Goose layer is in the
  [Control.Concurrent.Goose](https://codeberg.org/Playwright/playwright/src/branch/main/src/Control/Concurrent/Goose.hs)
  module
- The `Relic` module got some updates too, primarily this commit:
  [Relic, Goose: Introduce calling into the actor map](https://codeberg.org/Playwright/playwright/commit/6dc70895da22cef3d38f5a3abe8cf02d32a764cf)
- [goose-chat demo](https://codeberg.org/Playwright/playwright/src/branch/main/demos/goose-chat.hs)

In the code and in the demo, there are mentions of "Sturdy" - a *SturdyRef* is
a persistent identifier referring to a live actor. In the future these
identifiers will be serialized as URIs, but for now the default Haskell type
display is being used.

## See It in Action

To run the chat demo,

1. Clone [Playwright][] into 2 separate directories, and run `stack build` in
   each directory (don't worry, the builds will share all the dependency
   libraries)
2. In each directory execute: `stack run goose-chat`
3. Use localhost as the host for both, and pick some 2 available ports, e.g.
   6111 and 6222
4. The program will ask whether to update the peer's address - answer with *Y*
   and paste the "GooseSturdy" line from each program into the other
5. Now you can type chat lines into each program, and they will appear on the
   other! We've established a chat channel.

The "GooseSturdy" line is each peer's *Chat* actor identifier, and it looks
like this:

`GooseSturdy {gsAddr = GooseAddr {gaHost = "localhost", gaPort = 6111}, gsRelic = 2}`

A URI form could probably look like this:

`goose://localhost:6111/2`

Which means "actor ID 2 on server localhost:6111".

As you might notice, there's no mention of the actor type. I could add it, but
IIRC OCapN doesn't use it, and Spritely Goblins being written in Scheme leans
towards self-describing representations rather than relying on type schemas
(e.g. like Cap'n'Proto). So although on the Haskell level the type schemas are
present, the network serialization will try to mimic what Spritely does.

If you try the demo, let me know how it went!

## Funding

I really want to thank NLnet for funding this work! The extended grant is
allowing me to continue backend work, and allowing André to work on the
[Anvil][] frontend.

And I'm excited to see what happens during 2025! Implementing federation isn't
a trivial task, but I hope we can get more of it into actual usable live
forges.

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
[Spritely]: https://spritely.institute
[CapnProto]: https://capnproto.org
[Playwright]: https://codeberg.org/Playwright/playwright
