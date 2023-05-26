+++
title = "Vervis Actor Refactoring"
date = 2023-05-25
[extra]
author = "Pere Lev"
+++

For the last 2 months, I've been working on a major refactoring of the Vervis
codebase. I'm switching the architecture and code structure from a traditional
RESTful web API model into a networked *actor model*. I'm very excited about
it, because it's about much much more than just refactoring code: It's about
creating **a new kind of application**. And it's about the creating the **tools
and foundations that enable federated actor-based applications**.

## Vervis

Vervis is my implementation of a federated forge server. It started in 2016,
before the ActivityPub era, when the social Fediverse was based on OStatus.
When ActivityPub gained momentum with Mastodon's adoption of it, and ForgeFed
formed, I implemented ActivityPub-based federation in Vervis, and kept
implementing and experimenting with features, in parallel to developing them in
the ForgeFed specification.

Vervis is a reference implementation of ForgeFed, and is meant to be used for
testing other ForgeFed implementations (such as Forgejo).

While Vervis is on the proof-of-concept level, and not a "production-quality"
forge like Gitea, Forgejo, GitLab, etc., *I do intend to bring it to that level
eventually*. At least to the level that it can serve as the basis for a network
of federated forges where people can get a taste of what it looks and feels
like, to develop software collaborative on a decentralized by-the-people
network.

- Main repo: <https://vervis.peers.community/repos/rjQ3E>
- Mirror on Codeberg: <https://codeberg.org/ForgeFed/Vervis>
- [Federated PR demo from Sep 2022](https://fedi.foundation/2022/09/vervis-federated-merge-requests)

Right now we have the federated forge network project moving in two parallel
paths:

1. The ForgeFed implementation in [Forgejo](https://forgejo.org), along with UI
   changes to support display of federated objects and actors. Once the
   implementation reaches a certain level of readiness,
   [Codeberg](https://codeberg.org) will probably deploy it
2. The Vervis path I'll describe below

While Forgejo is a stable widely deployed forge, and Vervis an experimental
buggy PoC-level piece of software, Vervis also enjoys being **federated at the
core**.

The Vervis path involves:

- Removing all UI code from Vervis, making it a backend API-server only
- Debugging and stabilizing it, having a clear API for federation and for
  client apps with a reliable implementation
- Developing the [Anvil](https://codeberg.org/Anvil/Anvil) frontend app,
  reaching a usable demo release

## The old architecture

Until the refactoring, Vervis was written like a traditional web app server,
with its API being split into a server-to-server federation API (S2S), and a
command API for clients (C2S). All data (except Git and Darcs repos) lived in a
single big PostgreSQL database, including all the data of all the actors:
People, repositories, issue trackers, etc.

This architecture may work for centralized apps and services, but for Vervis,
I was gradually feeling more and more the impact of this structure. The primary
challenges were:

1. Activity handler logic was duplicated: Response to activities of local
   actors was happening in the C2S API handlers, while response to activities
   of remote actors was happening in the S2S API handlers.
2. Since actors are just rows in the DB, an actor that receives an activity
   needs to take care to initiate the whole chain of events needed in response
   to the activity, often involving cooperation between multiple actors, making
   sure to insert activities into inboxes and deliver and forward activities to
   remote actors and collections. This resulted in activity handlers being
   complicated, fragile and bug-prone.

During my work in 2022 it became clear that I need a new architecture: A system
of actors that send and receive messages, and where message handler code is
high-level can implement the logic in one place, without separate paths for
local and remote actors.

It also became clear to me, that ActivityPub actually isn't really suited for
such actor-model based programming. It's a vocabulary for social actors and
notifications, not a full actor-model programming system. Being frustrated with
the complexity of writing Vervis actors, I started looking for alternatives.
The next stage of the Fediverse, perhaps. I found 2 primary tools that seemed
relevant:

- [Spritely](https://spritely.institute)
- [Cap'n Proto](https://capnproto.org)

Spritely is is exactly the kind of tool I was looking for, but still at an
unstable early stage, and works only with Guile and Racket (while Vervis is
written in Haskell). Cap'n Proto is mature and used in "production" systems,
but its Haskell library (and I suspect the other implementations too) is much
more low-level and doesn't provide a batteries-included way to conveniently
write high-level distributed application code.

I decided to start an experiment: A Cap'n Proto based Fediverse demo, that
would demonstrate - to me and to others - what it might look like, if Mastodon
was implemented on top of Cap'n Proto or Spritely or similar, rather than
ActivityPub. It's nicknamed the [Capybara
experiment](https://codeberg.org/fr33domlover/Capybara). "Capybara" because
it's about capability-based programming.

While working with [NLNet](https://nlnet.nl) on the funding plan ([here's my
kanban board](https://todo.towards.vision/share/lecNDaQoibybOInClIvtXhEIFjChkDpgahQaDlmi/auth?view=kanban),
I decided to give a chance to the ActivityPub-based ForgeFed, and to dedicate
my work in 2023 to stabilize ForgeFed as an ActivityPub-based forge federation
protocol that covers the basic features that common forges provide - primarily
code, issues and PRs - and prepare the tools around Vervis to use as a test
suite for other implementations and as a reusable tool that people can study
and built more with. With that in place, I would move on with the Capybara
experiment and create an actor-programming based "ForgeFed 2" (or even give it
a new name).

## Objects, capabilities and actors

The biggest task on my plan for 2023, which I chose as the first task to do
within my NLNet-funded plan, is a refactoring of the Vervis codebase, to be
based on the same kind of actor-programming RPC system that Spritely and Cap'n
Proto have.

It means the structure of the program isn't a set of handlers of HTTP REST web
routes, but instead a set of actor method handlers.

Actors are objects that exist and live in parallel, and asynchronously send
messages to each other. Each type of actor has its own set of methods, and
handlers that implements its reaction to its methods being called by other
actors. Within a method handler, the actor can do just 3 things:

1. Modify/update its own state
2. Launch a finite number of new actors
3. Terminate

So, the program enables a network of actors, running in parallel and exchanging
messages.

Instead of a big shared database, each actor has its own state, that it manages
privately.

This system greatly simplifies writing concurrent code and data queries.

In a networked actor system, these actors can run on different machines, and
communicate via a network. But this communication is completely transparent to
the programmer: Calling a method of a local actor, and calling a method of a
remote actors, look exactly the same. You just write the *logic* of your
program, in terms of actors (think of these as a kind of microservices)
exchanging methods (which are commands, requests and events), and the
networking part is done for you by the actor system. This makes it *very* easy
and convenient to effortlessly write decentralized, federated and distributed
network/web applications!

These objects-actors are also sometimes called capabilities. This refers to
capability-based programming and capability-based security: Instead of using
things like ACLs, RBAC, passwords, and have-it-all ambient authority (e.g.
programs having free access to the filesystem, network, hardware, etc.), your
access to resources is based on *what you have*: If you have a reference to an
actor that representes a certain resource, you can access the resource via the
actor's methods. And if you want to give someone access to a resource, then
instead of giving them a password or adding them to a ACL, you send them a
reference to a relevant actor, so they can call its methods.

One of the principles in such systems is "designation is authorization".
There's no separatation between a reference to a resource (e.g. a link to an
online document) and the authority to access it (e.g. a secret password letting
you edit the document). An object/actor/capability is both the resource and the
authority to access it (possibly just to observe, possibly to also edit). The
resource reference and the authoity are the same thing.

## Material and representational capabilities

So, I'm facing a challenge:

- On one hand, I want to use a networked-capability-actor system in Vervis
- On the other hand, I'm trying to **still use ActivityPub for the network
  layer**, and ActivityPub is quite limiting here:
    - No clear distinction netween commands and events
    - No schema files for easily creating small-scale actors, the focus is on
      domain-level social actors (person, organization, repository, etc.)
    - No real methods with clear typed parameters, instead there are
      mostly-arbitrary and freely-extensible JSON-LD objects called Activities
    - No real capabilities

I'd like to look deeper at the last item, "no real capabilities".

The kind of actor system I described above is *behavior based*. Data,
databases, tables, formats, migrations, linked data etc. etc. aren't a
first-class member in such a system. Obviously, actors would store their state
on disk using some file format. Maybe in a SQL database, maybe in a Git repo,
maybe in some binary-encoded file. But the behavior of the system doesn't
depend on it, you don't access the data directly. The medium of interaction is
*actor methods calls*.

The "pro" you gain in this model: There's a precise and convenient interface
for defining actor behaviors. You define methods, their names and their
parameters, and the types of these parateres. Concurrency and scaling are
built-in, no fiddling with low-level data format details. Atomicity is also
built-in: Actor method calls and all the calls they cause can form a single
transaction, that either failes and rolls, or happens in complete success.

The "con" is that there's no built-in shared data layer. No protocol for
efficient access to specialized kinds of data. If you need these things, you
either build them on top, or use protocols external to the actor system.

The kind of capabilities is what I referred to as "real" capabilities. That's
basically literally and materially, designation is authorization. You literally
gain access to a resource by receiving a pointer to an actor (AKA object AKA
capability). That pointer is literally how you invoke the actor's methods.
Hence I (until I discover a better name) call these capabilities **material**
capabilities.

In contrast, ActivityPub (and [Bluesky](https://atproto.com/) perhaps even
more) heavily leans towards a *data based* approach, rather than a behavior
based one. Instead of methods with precise typed named parameters and return
values, there are "activities", which confusingly double as both commands and
events, and are extensible linked data documents, where even the standard
properties are generic ones like "origin", "context", "instrument", "object"
etc. whose meaning changes based on the type of object or activity.

The "pro" you gain in this approach is that notifications, inboxes and outboxes
containing descriptions of all the activity of actors ar built-in. Linked data
available to stream, mix, match, process, query and display. And the data is
very extensible, easily extensible, both activities and other objects.

The "con" is that having precise clear APIs beyond trivial commands is
difficult, and complex sequences of "method calls" are very cumbersome to
implement. Instead of having the meaning of a command be clearly stated in it,
the command arrives as a more general event description, and the exact meaning
needs to be determined based on the parameters, types and context of previous
activities.

In particular, a consequence of this approach is that when using
capability-based security, you need to choose between:

1. Modeling methods, parameters and return values *on top* of the JSON activity
   based layer, thus using a single "Invoke" activity for all method calls,
   instead of descriptive extensible linked data like "Create", "Follow",
   "Update", "Invite", etc.
2. Using "fake" capabilities where the "pointer" allowing the method call is
   merely attached to the activity description, rather than being the actual
   way of calling the method, i.e. break the "designation is authorization"
   principle by separating resource IDs from the authority to access them

If the "real" capabilities from earlier are *material*, then these "fake"
capabilities I call **representational**. Because they *represent* capabilities
using a JSON-LD linked data vocabulary, but nothing is enforcing that these
capabilities are actually used for authorization. They're like a key or
password that's attached to a command, and the receiving actor is responsible
for using it in the intended way. Such capabilities are *imitating* material
capabilities.

When I started working on bringing capabilities to ForgeFed, this is a choice I
faced: Do we create a whole new paradigm of modeling commands on the Fediverse,
by describing method schemas using JSON-LD and using a single non-descriptive
"Invoke" activity to call them? Or do we maintain the common use of activity
descriptions doubling as both commands and events, but at the cost of
representational, "fake" capabilities, and non-trivial event sequences being
very cumbersome and inconvenient to implement?

It might seem surprising, that I went for the 2nd option. I did so because the
1st option, despite being quite appealing, would cause ForgeFed to diverge from
"regular" ActivityPub to a degree that would almost defeat the point of using
ActivityPub, connecting forges with the wider Fediverse. Forges would seem to
be using some peculiar unusual protocol, that other Fediverse software wouldn't
recognize.

## The new architecture

In the last 2 months or so, I wrote an actor-system library in Haskell, for use
in Vervis (and hopefully elsewhere too). Below are links to some core pieces of
the code.

> Module `Control.Concurrent.Actor`
> [on Vervis](https://vervis.peers.community/repos/rjQ3E/source-by/main/src/Control/Concurrent/Actor.hs),
> [on Codeberg mirror](https://codeberg.org/ForgeFed/Vervis/src/branch/main/src/Control/Concurrent/Actor.hs)

I hooked my ActivityPub code into it, to enable the networking between actors.

> Module `Web.Actor.Deliver`
> [on Vervis](https://vervis.peers.community/repos/rjQ3E/source-by/main/src/Web/Actor/Deliver.hs),
> [on Codeberg mirror](https://codeberg.org/ForgeFed/Vervis/src/branch/main/src/Web/Actor/Deliver.hs)

I even started implementing per-actor storage to gradually replace the
PostgreSQL database.

> Module `Database.Persist.Box`
> [on Vervis](https://vervis.peers.community/repos/rjQ3E/source-by/main/src/Database/Persist/Box/Internal.hs),
> [on Codeberg mirror](https://codeberg.org/ForgeFed/Vervis/src/branch/main/src/Database/Persist/Box/Internal.hs)

And I started porting the `Person` actor to this new system.

> Module `Vervis.Actor.Person`
> [on Vervis](https://vervis.peers.community/repos/rjQ3E/source-by/main/src/Vervis/Actor/Person.hs),
> [on Codeberg mirror](https://codeberg.org/ForgeFed/Vervis/src/branch/main/src/Vervis/Actor/Person.hs)

If you look at that `Vervis.Actor.Person` module, you might notice that the
handlers for locally-sent events and the handlers for remotely-sent events are
separate. Isn't that exactly what I was trying to avoid, aiming to have a
*single* place to implement actor logic? Indeed, that's my intention. But with
ActivityPub as the basis for ForgeFed, it's difficult: Local method calls can
be precise requests, while remote calls are stuck using Activities as method
calls. And each activity is an extensible linked data object that needs to be
parsed, and its internal consistency verified. In addition, activity handlers
in the old architecture were using the shared PostgreSQL database to query the
context of previous activities. That's partially because activities aren't live
objects with live references to other related actors. So I may need a new way
to write safe validating method call handlers.

Ah, the ActivityPub activities double as commands and events, which makes it
impossible to determine the meaning of the activity without looking carefully
at the parameters and previous context, in a way that varies based on the types
of actors and type of activity.

So, to be honest, I'm not sure yet how or whether the local and remote handlers
can be converged into a single thing. Maybe it's not practical as long as I'm
using ActivityPub. Despite that, this architecture still greatly simplifies the
implementation of method handlers.

## What's next

In the new architecture, the actor-system, there's still a lot to do:

- Port all actors to it
- Port the C2S API handlers to it
- Switch to full per-actor storage
- Use thread supervisors for actor threads, instead of plain `forkIO`
- Switch to full capability-based programming of actors, instead of using the
  `IO` monad that allows any actor to perform any side effect

And the actor system can be improved way beyond ActivityPub:

- Implement transactions, where a single sequence of calls either happens to
  completion, or gets rolled back (how does Spritely do that? Perhaps have each
  actor return an STM action that updates its state, and upon completion run
  those STM actions together in a single transaction?)
- Implement CapTP, promise pipelining, etc. etc.
- Implement network layers and OcapN
- Get rid of `TheaterFor` by passing live `ActorRef`s instead of textual IDs

I'm actually considering to do the "Capybara experiment" using this actor
system, instead of Cap'n Proto or Spritely! My funded task plan *does* include
the experiment, but it's only a small part. Perhaps in 2024 when I'm done with
the current tasks, I'll shift my focus to the capability-based system and maybe
even a new phase of ForgeFed that will be based on it.

Anyway, landing back to reality, my next tasks in 2023 with ForgeFed and Vervis
are about:

- Finalizing the (representational) capability system in ForgeFed
- Finishing the specification of projects and teams
- Finishing the implementiion of all of that in Vervis
- Turning Vervis into a test suite for other implementations

## Comments

We have an account for ForgeFed on the Fediverse:
<https://floss.social/@forgefed>

Right after publishing this post, I'll make a toot there to announce the post,
and you can comment there :)
