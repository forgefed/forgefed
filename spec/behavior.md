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

## Kinds of Objects

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

## Object Publishing and Hosting {#publishing}

In ForgeFed, actors host their child objects locally, i.e. the actor and the
child object are hosted on the same instance. Actors may create remote objects
by *offering* them to the relevant actor, which then may create the object on
their side and assign it a URI.

The process begins with an [Offer][] activity, in which:

- [object][] MUST be the object being offered for publishing, and that object
  MUST NOT have an [id][]
- [target][] MUST indicate under which list/collection/context the sender would
  like the object to be published (it may also be the URI of the target actor
  itself)

Among the recipients listed in the [Offer][]'s recipient fields, exactly one
recipient is the actor who's responsible for inspecting and possibly publishing
the newly object, and possibly sending back an [Accept][] or a [Reject][].
We'll refer to this actor as the *target actor*. Specific object types
described throughout this specification have a specific meaning for the *target
actor*, which processing and inspection it is expected to do, and where it is
expected to list the URI of the object once it publishes it.

The sender is essentially asking that the target actor hosts the object as a
child object and assigns is a URI, allowing to observe and interact with the
object. The target actor will be responsible for hosting and controlling the
object, and the sender will just be mentioned as the author.

When an actor *A* receives the [Offer][] activity, they can determine whether
they're the *target actor* as follows: If the [target][] is *A* or a child
object of *A*, then *A* is the *target actor*. Otherwise, *A* isn't the target
actor.

In the following example, Luke wants to open a ticket under Aviva's Game Of
Life simulation app:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
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
        "summary": "Test test test",
        "content": "<p>Just testing</p>",
        "mediaType": "text/html",
        "source": {
            "mediaType": "text/markdown; variant=Commonmark",
            "content": "Just testing"
        }
    },
    "target": "https://dev.example/aviva/game-of-life"
}
```

The *target actor* SHOULD send an [Accept][] or a [Reject][] activity to the
Offer's author in response. If the *target actor* sends an Accept, it MUST
host its own copy, assigning an [id][] to the newly published object and adding
it to the expected list specified by the [Offer][]'s [target][].

If the *target actor* sends a [Reject][], it MUST NOT add the object's [id][]
to that list. However if the *target actor* doesn't make any use of the
object, it MAY choose not to send a Reject, e.g. to protect user privacy. The
`Accept` or `Reject` may also be delayed, e.g. until review by a human user;
that is implementation dependent, and implementations should not rely on an
instant response.

In the [Accept][] activity:

- [object][] MUST be the Offer activity or its [id][]
- [result][] MUST be specified and be the [id][] of the new child object now
  hosted by the *target actor*, which is extracted from the [Offer][]'s
  [object][]

In the following example, Luke's ticket is opened automatically and Aviva's
Game Of Life repository, which is an actor, automatically sends Luke an Accept
activity:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://dev.example/aviva/game-of-life/outbox/096al",
    "type": "Accept",
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
properties as described [in the modeling specification][model-push]. If the
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

The first step for opening a ticket is to determine to which actor to send the
ticket. We'll refer to this actor as the *ticket tracker*. Given an object
*obj* against which you'd like to open a ticket (e.g. some application's source
code repository), look at the [ticketsTrackedBy][prop-ticketstrackedby]
property of *obj*.

- If `ticketsTrackedBy` isn't specified, then *obj* does't declare a way to
  open tickets via ForgeFed.
- If `ticketsTrackedBy` is specified and is set to the [id][] of *obj* itself,
  that means *obj* manages its own tickets, i.e. it is the *ticket tracker* to
  which you'll send the ticket.
- If `ticketsTrackedBy` is specified and is set to some other object, look at
  the [tracksTicketsFor][prop-tracksticketsfor] property of that other object.
  If the [id][] of *obj* is listed there under `tracksTicketsFor`, then that
  other object is the *ticket tracker* to which you'll send the ticket.
  Implementations SHOULD verify this bidirectional reference between the object
  and the tracker, and SHOULD NOT send a ticket if the bidirectional reference
  isn't found.

Now that we've determined the *ticket tracker*, i.e. the actor to whom we'll
send the [Ticket][type-ticket], the ticket may be opened using an [Offer][]
activity in which:

- [object][] is the ticket to be opened, it's a [Ticket][type-ticket] object
  with fields as described [in the modeling specification][model-ticket]. It
  MUST specify at least [attributedTo][], [summary][] and [content][], and MUST
  NOT specify [id][]. If it specifies a [context][], then it MUST be identical
  the Offer's [target][] described below.
- [target][] is the ticket tracker to which the actor is offering the Ticket
  (e.g. a repository or project etc. under which the ticket will be opened if
  accepted). It MUST be either an actor or a child object. If it's a child
  object, the actor to whom the child object belongs MUST be listed as a
  recipient in the Offer's [to][] field. If it's an actor, then that actor MUST
  be listed in the `to` field.

The *target actor* MAY then send back an Accept or Reject. The action that has
been taken by the *target actor* is indicated to the ticket author as follows:

- If a [Reject][] was sent, it means the ticket hasn't been assigned an [id][]
  URI by the tracker and isn't being tracked by the tracker
- If an [Accept][] was sent, it means the ticket is now tracked and hosted on
  the target's side

In the following example, Luke wants to open a ticket under Aviva's Game Of
Life simulation app:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
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
        "summary": "Test test test",
        "content": "<p>Just testing</p>",
        "mediaType": "text/html",
        "source": {
            "mediaType": "text/markdown; variant=Commonmark",
            "content": "Just testing"
        }
    },
    "target": "https://dev.example/aviva/game-of-life"
}
```

Luke's ticket is opened automatically and Aviva's Game Of Life repository,
which is an actor, automatically sends Luke an Accept activity:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://dev.example/aviva/game-of-life/outbox/096al",
    "type": "Accept",
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

## Commenting

A comment on a ForgeFed resource object (such as tickets, merge requests) MUST
be published as a [Create][] activity, in which [object][] is a [Note][] with
fields as described [in the modeling specification][model-comment].

In the following example, Luke replies to Aviva's comment under a merge request
he submitted earlier against her Game Of Life simulation app repository:

```json
{
    "@context": "https://www.w3.org/ns/activitystreams",
    "id": "https://forge.example/luke/outbox/rLaYo",
    "type": "Create",
    "actor": "https://forge.example/luke",
    "to": [
        "https://forge.example/luke/followers",
        "https://dev.example/aviva/game-of-life",
        "https://dev.example/aviva/game-of-life/followers",
        "https://dev.example/aviva/game-of-life/team",
        "https://dev.example/aviva/game-of-life/merge-requests/19/followers",
        "https://dev.example/aviva/game-of-life/merge-requests/19/team"
    ],
    "object": {
        "id": "https://forge.example/luke/comments/rD05r",
        "type": "Note",
        "attributedTo": "https://forge.example/luke",
        "to": [
            "https://forge.example/luke/followers",
            "https://dev.example/aviva/game-of-life",
            "https://dev.example/aviva/game-of-life/followers",
            "https://dev.example/aviva/game-of-life/team",
            "https://dev.example/aviva/game-of-life/merge-requests/19/followers",
            "https://dev.example/aviva/game-of-life/merge-requests/19/team"
        ],
        "context": "https://dev.example/aviva/game-of-life/merge-requests/19",
        "inReplyTo": "https://dev.example/aviva/comments/E9AGE",
        "mediaType": "text/html",
        "content": "<p>Thank you for the review! I'll submit a correction ASAP</p>",
        "source": {
            "mediaType": "text/markdown; variant=Commonmark",
            "content": "Thank you for the review! I'll submit a correction ASAP"
        },
        "published": "2019-11-06T20:49:05.604488Z"
    }
}
```

# Acknowledgements

[act-push]: /vocabulary.html#act-push

[type-repository]: /vocabulary.html#type-repository
[type-ticket]:     /vocabulary.html#type-ticket

[prop-team]:             /vocabulary.html#prop-team
[prop-ticketstrackedby]: /vocabulary.html#prop-ticketstrackedby
[prop-tracksticketsfor]: /vocabulary.html#prop-tracksticketsfor

[model-comment]: /modeling.html#comment
[model-push]:    /modeling.html#push
[model-ticket]:  /modeling.html#ticket

[Accept]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-accept
[Create]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-create
[Image]:  https://www.w3.org/TR/activitystreams-vocabulary/#dfn-image
[Note]:   https://www.w3.org/TR/activitystreams-vocabulary/#dfn-note
[Object]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-object
[Offer]:  https://www.w3.org/TR/activitystreams-vocabulary/#dfn-offer
[Reject]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-reject

[actor]:        https://www.w3.org/TR/activitystreams-vocabulary/#dfn-actor
[attributedTo]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-attributedto
[content]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-content
[context]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-context
[followers]:    https://www.w3.org/TR/activitypub/#followers
[id]:           https://www.w3.org/TR/activitystreams-vocabulary/#dfn-id
[result]:       https://www.w3.org/TR/activitystreams-vocabulary/#dfn-result
[summary]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-summary
[target]:       https://www.w3.org/TR/activitystreams-vocabulary/#dfn-target
[to]:           https://www.w3.org/TR/activitystreams-vocabulary/#dfn-to
[type]:         https://www.w3.org/TR/activitystreams-vocabulary/#dfn-type

[RFC2119]: https://tools.ietf.org/html/rfc2119
