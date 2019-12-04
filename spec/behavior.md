---
title: ForgeFed Behavior
---

# Abstract

This document provides instructions for using ActivityPub activities and
properties to represent forge events, and describes the side-effects these
activities should have. 

# Introduction

**The ForgeFed behavior specification** is a set of instructions for
representing version control system and project management related transactions
using ActivityPub activity objects, and it describes the side effects and
expected results of sending and receiving these activities. The vocabulary for
these activities includes standard ActivityPub terms, new terms defined by
ForgeFed, and terms borrowed from other external vocabularies.

The ForgeFed vocabulary specification defines a dedicated vocabulary of
forge-related terms, and the **behavior specification** uses these terms, along
with terms that already exist in ActivityPub or elsewhere and can be reused for
forge federation.

The ForgeFed modeling specification defines rules for representing forge
related objects as ActivityPub JSON-LD objects, and these objects are used in
the **behavior specification**, included in activities or mentioned in
activities or modified due to activity side-effects.

# Conformance

The key words MAY, MUST, MUST NOT, SHOULD, and SHOULD NOT are to be interpreted
as described in [RFC2119][].

# Objects

Objects are the core concept around which both ActivityPub and ForgeFed are
built. Examples of Objects are [Note], [Ticket][type-ticket], [Image],
[Create], [Push][act-push]. Some objects are resources, which are objects that
contain or represent information and user made or program made content, and
some objects are helpers that exist as implementation detail aren't necessarily
exposed to humans or are useful to humans. But everything is an [Object],
represented as compacted JSON-LD.

ForgeFed is an ActivityPub extension, and communication between ForgeFed
implementations occurs using activity objects sent to actor inboxes and
outboxes.

There are 4 kinds of objects in ForgeFed:

1. Activities: These are objects that describe actions (actions that happened,
   or actions that are happening, or a request to perform an action), and their
   primary use is for S2S interaction between actors, by being sent to an
   actor's inbox, and C2S interaction between a person or a program and actor
   they control, by being sent to the actor's outbox. Activities can also
   appear or be linked inside other objects and activities and be listed in
   Collections.
2. Actors: These are static persistent objects that have an [inbox] and can be
   directly interacted with by POSTing activities to it. Their primary use is
   to contain or represent information and output of user actions or program
   actions, and to manage access this information and to modification of it.
3. Child objects: These are persistent objects which, like actors, contain or
   represent information and output of user actions or program actions, but
   they don't have their own [inbox] and aren't directly interacted with. A
   managed static object always has a parent object, which is an actor, and
   that actor's inbox is the way to interact with the child object. The parent
   actor manages access and modification of the child object.
4. Global helper objects: These are objects that don't belong to any actor and
   don't need any interaction through activities. As such, they don't exactly
   fit into the actor model, but may be involved in implementation details and
   practical considerations.

Actors, children and globals are referred in ForgeFed as the *static* objects,
while activities are the *dynamic* objects (the terms *constant* and *variable*
are used for stating whether an object changes during its lifetime or not).

*Static* objects, in addition to being an actor or child or global, also have a
resource/helper distinction:

- Resource: Contains or represents information and user made or program made
  content, usually belongs to the domain model of version control systems and
  project management.
- Helper: Used for running things behind the scenes, not exposed directly as
  user content, may be transient or auto generated, usually related to
  implementation detail and not to concepts of version control and project
  management.

This specification doesn't mandate which types and objects should be actors,
but it does provide guidelines that implementations SHOULD follow:

- Resource objects that have self-contained stand-alone meaning should be
  actors
- Objects that handle access control for updates of themselves should be actors
- Objects that need to be able to send activities should be actors
- Objects whose meaning is inherently tied to a parent object, or whose access
  control is managed by a parent object, can have all their interactions done
  via the parent object, and not be actors themselves
- If an object doesn't need to send or receive activities, even if it's self
  contained, there's probably no need to make it an actor, because it
  practically doesn't participate in actor-model communication

Here are some examples and their rationale:

- A ticket/issue/bug is created with respect to some project, repo, software,
  system, the ticket is inherently a part of that parent object, so tickets
  would generally not be actors
- A project or repository are generally self-contained entities, and even if
  some forge has users as top-level namespace and repos are created under
  users, the user managing/owning/sharing a repo is just a matter of access
  control and authority, *it isn't a part of the meaning of the repo itself*,
  and the repo could easily change hands and change maintainers while remaining
  the same repo, same software, same content, same meaning. So, repos and
  projects would generally be actors.
- A group/organization/team is a self-contained object, a set of users along
  with access control and roles and so on, and it needs to be able to receive
  update activities that update the team members list, structure and access and
  so on, even though a team isn't a user and probably doesn't publish
  activities. So, teams would generally be actors.

The proposal here is that the following types typically be actors:

- Person
- Project
- Repository
- Group/Organization/Team

And other types such as these typically not be actors:

- Commit
- Ticket
- Merge request
- Patch
- Diff
- Discussion thread

# Actors

A ForgeFed implementation MUST provide an Actor of type `Repository` for every
repository that should support federation.

A ForgeFed implementation SHOULD provide an Actor of type `Person` for every user
of the platform.

# Client to Server Interactions

ForgeFed uses Activities for client to server interactions, as described by
ActivityPub. A client will send objects (eg. a Ticket) wrapped in a Activity
(eg. Create) to an actor's outbox, and in turn the server will take care of
delivery.

## Follow Activity

The Follow activity is used to subscribe to the activities of a Repository.
The client MUST send a Follow activity to the Person's outbox. The server
in turn delivers the message to the destination inbox.

## Push Activity

The Push activity is used to notify followers when somebody has pushed changes
to a Repository.
The client MUST send a Push activity to the Repository's outbox. The server
in turn delivers the message to the Repository followers.

# Server to Server Interactions

## Reporting Pushed Commits

The ForgeFed [Push][act-push] activity can be used for representing an action
of pushing commits into a [Repository][type-repository]. Two actors are
involved in the process, the *pusher* (usually a person) and the *repository*,
and they may be hosted on different instances. We therefore refer to 2 kinds of
pushes:

1. *Local Push*: The pusher and the repository are hosted on the same instance
   (that's the only case in centralized non-federated forges)
2. *Federated Push*: The pusher and the repository are hosted on different
   instances (that's unique to federated forges)

At this time, the representation of *Federated Push* isn't provided yet. Below
we discuss *Local Push*.

Upon a successful push, a ForgeFed implementation that publishes a Push
activity MUST provide the [type][], [actor][], [context][] and [target][]
properties as described in the [modeling specification][model-push]. If the
Push activity's recipient fields list collections that belong to the
repository, such as its [followers][] and [team][prop-team], the repository
MUST verify the authenticity and correctness of the Push activity's fields
before it performs inbox forwarding (i.e. delivery to the members of those
collections), and MUST NOT perform inbox delivery if the correctness check
doesn't pass.

In a *Local Push*, if the Push activity is generated on the server, that
obviates the need to perform correctness checking. Implementations MAY forbid
clients from publishing Push activities (via the ActivityPub C2S API or any
other mechanism), in order to guarantee the authenticity of Push activities.

See [example in the modeling specification][model-push].

## Opening a Ticket

A request to open a [Ticket][type-ticket] sent from one actor to another MUST
be represented as an [Offer][] activity in which:

- [object][] is the ticket to be opened, it's either the whole
  [Ticket][type-ticket] object or just the [id][] of a Ticket that's already
  published and the recipient of the Offer can fetch.
- [target][] is the ticket tracker to which the actor is offering the Ticket
  (e.g. a repository or project etc. under which the ticket will be opened if
  accepted). It MUST be either an actor or a child object. If it's a child
  object, the actor to whom the child object belongs MUST be listed as a
  recipient in the Offer's [to][] field. If it's an actor, then that actor MUST
  be listed in the `to` field.

Among the recipients listed in the Offer's recipient fields, exactly one
recipient is the actor who's responsible for processing the offer and possibly
sending back an [Accept][] or a [Reject][]. We'll refer to this actor as the
*target actor*.

When an actor *A* receives the Offer activity, they can determine whether
they're the *target actor* as follows: If the Offer's [target][] is *A* or a
child object of *A*, then *A* is the *target actor*. Otherwise, *A* isn't the
target actor.

In the following example, Luke wants to open a ticket under Aviva's Game Of
Life simulation app:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "id": "https://forge.example/luke/outbox/02Ljp",
    "type": "Offer",
    "actor": "https://forge.example/luke",
    "to": [
        "https://dev.example/aviva/game-of-life",
        "https://dev.example/aviva/game-of-life/team",
        "https://dev.example/aviva/game-of-life/followers"
    ],
    "object": {
        "type": "Ticket",
        "attributedTo": "https://forge.example/luke",
        "name": "Test test test",
        "content": "<p>Just testing</p>",
        "mediaType": "text/html",
        "source": {
            "mediaType": "text/markdown; variant=Commonmark",
            "content": "Just testing"
        },
    },
    "target": "https://dev.example/aviva/game-of-life"
}
```

If the [Ticket][type-ticket] isn't opened, the *target actor* MAY send a
[Reject][] activity to the [actor][] of the Offer. If the ticket is opened, the
*target actor* MUST deliver an [Accept][] activity to the actor of the Offer.
In the Accept activity:

- [object][] MUST be the Offer activity or its [id][]
- [result][] MUST be the newly created ticket or its [id][]

In the following example, Luke's ticket is opened automatically and Aviva's
Game Of Life repository, which is an actor, automatically sends Luke an Accept
activity:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "id": "https://dev.example/aviva/game-of-life/outbox/096al",
    "type": "Accept"
    "actor": "https://dev.example/aviva/game-of-life",
    "to": [
        "https://forge.example/luke",
        "https://dev.example/aviva/game-of-life/team",
        "https://dev.example/aviva/game-of-life/followers"
    ],
    "object": "https://forge.example/luke/outbox/02Ljp",
    "result": "https://dev.example/aviva/game-of-life/issues/113"
}
```

# Acknowledgements

[act-push]: /vocabulary.html#act-push

[type-repository]: /vocabulary.html#type-repository
[type-ticket]:     /vocabulary.html#type-ticket

[prop-team]: /vocabulary.html#prop-team

[model-push]: /modeling.html#push

[Accept]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-accept
[Create]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-create
[Image]:  https://www.w3.org/TR/activitystreams-vocabulary/#dfn-image
[Note]:   https://www.w3.org/TR/activitystreams-vocabulary/#dfn-note
[Object]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-object
[Offer]:  https://www.w3.org/TR/activitystreams-vocabulary/#dfn-offer
[Reject]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-reject

[actor]:     https://www.w3.org/TR/activitystreams-vocabulary/#dfn-id
[context]:   https://www.w3.org/TR/activitystreams-vocabulary/#dfn-context
[followers]: https://www.w3.org/TR/activitypub/#followers
[id]:        https://www.w3.org/TR/activitystreams-vocabulary/#dfn-id
[result]:    https://www.w3.org/TR/activitystreams-vocabulary/#dfn-result
[target]:    https://www.w3.org/TR/activitystreams-vocabulary/#dfn-target
[to]:        https://www.w3.org/TR/activitystreams-vocabulary/#dfn-to
[type]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-type

[RFC2119]: https://tools.ietf.org/html/rfc2119
