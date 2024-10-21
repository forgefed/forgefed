+++
title = "Hello Actor Programming"
date = 2024-10-13
[extra]
author = "Pere Lev"
+++

## Stressful Times

Wow, two months passed since my last post. Two exhausting, but also exciting,
months of working on something entirely new and different: An actor programming
library. It took much more time than I hoped, and of course it's just the
beginning, but I'm so relieved now that I have some results to show.

I'll be honest with you: I depend financially on the funding from NLnet,
funding for which I'm deeply grateful. But it also sometimes means a lot of
stress, when a task becomes complicated and long, which delays the payment. I
can already imagine the advice coming my way: Create a variety of income
sources, it's more sustainable. And you're right! And I'm working on it. But in
the field of software, just FYI, I never actually worked in a company. It's
deeply special and important and dear to me, that my work's purpose continues
to be the loyal service of humankind and perhaps even the whole ecosystem that
is our planet, and I therefore work in a post-capitalism mode, releasing all my
work as Free Software, and there's no investors or expectations of profit. I
just need enough money for my house and food etc. etc., that's it.

But being a student has made my expenses much much higher and my schedule much
more busy. That's probably what has made these months stressful.

Thank you for being witnesses of my journey! Let's dive into the content.

As always, my [task board][kanban] is available.

## ActivityPub and OCAPs

ForgeFed is built on top of the federation protocol called ActivityPub. And
ActivityPub is designed around the publishing of personal user content: You
publish posts, images, videos, etc. and people can comment on them, and comment
on other people's comments. And over the years, the Fediverse is getting new
applications that implement services that match that pattern:

- Funkwhale, for publishing audio
- Peertube, for publishing videos
- PixelFed, for publishing images
- Mastodon, for microblogging
- Lemmy, for link aggregation
- And much more...

The collaboration patterns for these applications *can* be complicated, but
they're mostly simple:

- Anyone can publish content
- Anyone can comment on anyone else's content
- There are features to handle spam protection, user blocking, etc.

I know, I know, implementing all of that isn't trivial. My point is that the
main scenario is the publishing of personal content: You make a video, you
upload it, done.

ForgeFed is unusual compared to this Fediverse landscape: The focus of forges
is on *collaboration* on shared resources. Of course you can just publish your
own personal Git repos and work alone, but the power of issues, PRs, etc.
shines when people can work together. So the collaboration patterns here are
more complex. Unlike a video, that you just upload once, a Git repo is an
editable resource that ongoingly receives changes.

Collaboration on editable resources on a decentralized network requires a
powerful authorization mechanism: A way to reliably determine who can do which
actions on which resources. But federated authorization is one of the things
ActivityPub doesn't define, and leaves it to us to figure out.

In the past 2 years or so, I've worked hard to build an Object Capability
system into ForgeFed - a vocabulary for granting and revoking permissions. It
goes a long way, and still, something just feels wrong: Trying to build rich
collaboration on top of a system very clearly suited for personal publishing.

That's why in the work plan for 2023-2024, I added items for exploring
something else: A forge based on *actor programming* instead of ActivityPub.

## Actor Programming

While ActivityPub mostly a combination or email-like publishing and a
vocabulary for describing personal objects, *actor programming*, or
*capability-based programming*, focuses on behavior: You write your
application's source code in such a way that a piece of the software has access
only to what it needs, and the permissions are essentially combined with the
operations: If you have a reference to an operation, you're allowed to execute
it.

*Networked* actor programming becomes possible by creating tokens that
represent operations, and passing these tokens to other actors possibly on
different machines over the network. However, instead of a custom JSON-based
vocabulary like ActivityPub, that represents domain objects (images, videos,
etc.), the data format is now behind the scenes, and encodes references to
*functions* (and actors and their methods), so that any piece of code you write
can become a capability you pass on the network and allow other actors to
execute it.

This is a vastly more powerful foundation that what the ActivityPub-based
ForgeFed has, and I've been playing with it for the past year, exploring,
reading a lot of material, asking questions.

I've mostly been observing how [Spritely][] and [CapnProto][] work, and aiming
to create something similar, even compatible.

Much of the work happened inside Vervis: I implemented an actor system right
inside it, and it's been powering Vervis for a while now. But at some point,
the HTTP-based API and the capability-based system had to depart and take
different directions.

## A Big Experiment

Spritely, which I mentioned above, already has the foundations for networked
actor programming, and a possible route would have been to try implementing a
little forge on top. This is a great direction! Anyone feels like trying it? I
picked a different route: While Spritely focuses on the Scheme language, I
started work, inspired by the CanProto Haskell implementation, to implement an
actor-programming system in Haskell.

Haskell and its ecosystem do have facilities for actor programming, and the
powerful type system could also allow generating client code for other
programming languages, but most (if not all) actor related packages are meant
for concurrent and cloud computation, not for capability-based programming of
federated-network applications.

I knew diving into this would be a risk for me: It's an experiment, with very
little clarity about the chances for success, or how much time it would take.
So through the year I kept working on Vervis tasks, and waiting with the actor
programming experiment as I read and explore and gather more and more clarity
on how to implement it when the time comes.

The risk is financial: I'm not an academic researcher paid for my work hours.
If I start a huge task, I don't receive funds until it's done. So I need to
gather some savings, allowing me some buffer to work without needing immediate
income.

Despite the financially stressful times, I somehow did it. In August 2024, the
time came.

## Basic Concepts

So, I basically started implementing something in the spirit of Spritely
Goblins, in Haskell. Some parts, such as networking and petnames, are left for
my next tasks. I started with focusing just on the basics (which are quite
complex by themselves):

- Actors have methods
- Methods can call other methods of other actors
- Networking is transparent: Calling a method or a local and remote actors
  looks the same, you don't care about it when you implement domain logic
- Actors are grouped in groups called *Vats* - actors in the same Vat can call
  each other's methods synchronously, like regular function calls
- Actors in different vats can only do an *asynchronous* call - send out the
  method parameters and the result of the method call will arrive later
- The whole system can be serialized to disk, and restored to continue running
- Actors can have state, which may include references to other actors
- The sequence of method calls within each Vat is *atomic* - either it succeeds
  and the Vat's state is updated, or any state changes are reverted

I'm about to descibe the steps I've taken on the path to implement these
features. If you want to explore the bottom-line code, look at these:

- <https://codeberg.org/Playwright/playwright>
- In particular
  [Control.Concurrent.Relic](https://codeberg.org/Playwright/playwright/src/branch/main/src/Control/Concurrent/Relic.hs)
- And that module's
  [test](https://codeberg.org/Playwright/playwright/src/branch/main/test/Relic.hs)

Most tests do a little Fibonacci computation using actors, thus serving as a
simple usage example.

## Utilities

I needed some helper modules to support the actor programming system, such as:

- Since actor state (as well as method parameters etc.) can contain live
  references to actors (which are essentially threads), I needed a way to
  switch between the live state and the serializable form which can be read and
  written to disk. For that I wrote the
  [mold](https://codeberg.org/Playwright/mold) library, which allows to replace
  live references with their serialized form and vice versa.
- To generate unique actor IDs, I implemented a simple type-safe
  [NameGenerator](https://codeberg.org/Playwright/playwright/src/branch/main/src/Data/NameGenerator),
  which basically immitates the auto-increasing IDs that SQL DBs often use
- Some actors need the ability to shut themselves down, while others run
  forever / until garbage collected. The latter kind allows for static
  references: If you hold a reference, you have a guarantee the actor is alive.
  To encode that in the type system I wrote the
  [Control.Concurrent.Lifespan](https://codeberg.org/Playwright/playwright/src/branch/main/src/Control/Concurrent/Lifespan.hs)
  module.
- Finally, for the actor thread part, the
  [Control.Concurrent.Exchange](https://codeberg.org/Playwright/playwright/src/branch/main/src/Control/Concurrent/Exchange.hs)
  module is full of building blocks for data exchange and method calls between
  threads

## High-Level API Based On Vervis

My starting point was the Vervis
[Control.Concurrent.Actor](https://codeberg.org/ForgeFed/Vervis/src/branch/main/src/Control/Concurrent/Actor.hs)
API, which does a lot of what I needed, but is limited by Vervis needing the
actors to be ForgeFed actors which communicate by publishing Activities. I
played with it created the
[BeeZero](https://codeberg.org/Playwright/playwright/src/branch/main/src/Control/Concurrent/BeeZero.hs)
interface, which refers to actors as "Bees". I knew I'd need to build the
actor programming system in layers, and tried to give a name to each layer :)

The BeeZero module supports both near actors (i.e. synchronous calls to actors
in the same Vat) and far actors (async calls to other Vats), and is only a
live system, without disk persistence.

- The module itself:
  [src/Control/Concurrent/BeeZero.hs](https://codeberg.org/Playwright/playwright/src/branch/main/src/Control/Concurrent/BeeZero.hs)
- Test:
  [test/Bee.hs](https://codeberg.org/Playwright/playwright/src/branch/main/test/Bee.hs)

## A Step Back To Low-Level

Persistence requires to have unique tokens representing actor references, as
well as any other live object that needs to be serialized and loaded back,
restoring the system to exactly the same state it was before. Since `BeeZero`
just uses live references without attaching serializable IDs, I didn't build
persistence on top. No IDs also means Promises (future values waiting to be
returned from method calls) can't be persisted either, which led me to decide I
need to take a step back and start from a lower-level point.

Since state atomicity is on the Vat level, and since each Vat is a single
thread with a single event loop, I decided to implement an actor system layer
for Vats, and later add the near-actor feature on top, instead of the other way
around.

I call these *Fly* actors, in the `Control.Concurrent.Fly` module. Fly actors
run in their own threads, their methods have exactly one parameter, and no
return value. To return a value, the parameter needs to provide a way to send
back the result. A low-level foundation.

The idea is that Vats would be Fly actors, and the next layers would add near
actors inside Vats, essentially adapting the `BeeZero` code to work on top of
`Fly`.

- The module itself:
  [src/Control/Concurrent/Fly.hs](https://codeberg.org/Playwright/playwright/src/branch/main/src/Control/Concurrent/Fly.hs)
- Test:
  [test/Fly.hs](https://codeberg.org/Playwright/playwright/src/branch/main/test/Fly.hs)

## Vat Persistence

On top of Fly actors, I went on to implement a persistence layer. Each Fly
actor has a read-only piece and a read-write piece in its state, and both can
be serialized to and from disk. There's a foundation for adding multiple
serialization methods, but right now the implementation is coded to use a
simple file-based database format. A future improvement could be switching to
SQLite.

Migration is supported too, by allowing actors to provide a series of mappings
between the previous versions of their state.

I named these actors *Relic* actors. So, a Relic actor *implements* the Fly
interface, making sure to atomically store its state on each iteration of the
event loop.

Since serialization involves conversions between live objects and their
serializable IDs, loading the actor system happens in steps:

1. Load all actor data including actor IDs
2. Perform migrations on actor state
3. For each actor ID, create the live objects in memory
4. In each actor's loaded state, now attach to each actor reference (that is
   right now just an ID) the matching live object
5. Now that we have the live state for each actor, finally launch the actor
   threads

Since Relic actors just implement the Fly interface, they too have methods with
a single parameter and no return value. Of course, multiple parameters can
trivially be passed by passing a tuple as the single parameter. But to support
Promises and Promise Pipelining (calling methods using future values and
references), we'll need another layer on top of Relic.

- The module itself:
  [src/Control/Concurrent/Relic.hs](https://codeberg.org/Playwright/playwright/src/branch/main/src/Control/Concurrent/Relic.hs)
- Test:
  [test/Relic.hs](https://codeberg.org/Playwright/playwright/src/branch/main/test/Relic.hs)

The test demonstrates persistence: Each time it runs, the test computes the
next 5 Fibonacci numbers, and displays them. On the filesystem, `test/ng` file
is the state of the ID-generator, and the `test/root` directory keeps the state
of each actor type.

## What's Next

That's all so far! So what we have in place is *Persistent single-actor Vats
(Relic actors)*. Near calls can be represented by generating token IDs in Relic
state, but a higher-level layer will properly implement near calls by adapting
the BeeZero code to Relic.

What to expect for this actor programming library project in 2025:

- Full documentation (the `Exchange` module I mentioned above has a detailed
  tutorial, the other modules not yet because they're still rapidly changing)
- Promises and promise pipelining
- Support for event sources
    - Mouse and keyboard
    - Textual UI
    - Graphic/Web UI
    - Networking (TCP, HTTP)
- Petnames
- An initial forge demo

Of course 2024 isn't over yet! I'll continue with this work, as well as some
Vervis tasks and bug fixes.

## Funding

I really want to thank NLnet for funding this work! The extended grant is
allowing me to continue backend work, and allowing André to work on the
[Anvil][] frontend.

## See It in Action

So, the main artifact of this work is the [Playwright][] library. There's no UI
to show, so no video demo yet. But you can already start a Haskell project and
import the Playwright library and play with Relic actors. The test is a good
starting point.

If you encounter any bugs, let me know! Or [open an
issue](https://codeberg.org/Playwright/playwright/issues).

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
