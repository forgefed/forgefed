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

## Granting access to shared resources

An actor that wishes to give other specific actors access to view or modify it
(or a child object of it), SHOULD do so according to the following
instructions.

### Object capabilities using Grant activities {#s2s-grant-flow}

An Object Capability (or in short OCap or OCAP) is a token providing access to
certain operations on a certain resource. An actor wishing to act on a resource
provides the token to the resource, alongside the Activity they wish to
perform. The resource verifies the token, and if and only if it finds the token
valid, and access to the requested Activity is allowed by the token, *then* the
resource allows the Activity to be performed.

The token provided by the actor to the resource, i.e. the OCAP, is the ID URI
of a previously published [Grant][act-grant] activity.

The fundamental steps for accessing shared resources using OCAPs are:

1. The actor managing the resource (which may be the resource itself) sends a
   `Grant` activity to the actor to whom it wishes to grant access
2. When the actor who received the access wishes to operate on the resource, it
   sends the activity to the actor managing the resource, along with the ID URI
   of the `Grant` sent in step 1
3. The actor managing the resource verifies the access provided by the `Grant`
   whose ID URI is provided, and allows the activity to be performed only if
   the verification passes

Requirements for the `Grant` activity, i.e. step 1:

- The `Grant`'s [context][], i.e. the resource for which access is being given,
  MUST be the `Grant's` sender (i.e. its [actor][]) or a child object of it
- The `Grant`'s [object][] MUST be provided and specify a *role* determining
  which operations the recipient actor may perform on the resource; however
  this specification doesn't (yet) specify how to define or find such roles
- The `Grant`'s [target][] MUST be provided, and specify exactly one actor to
  whom access is being given

Requirements for the activity (referred below as *activity A*) sent in step 3:

- The OCAP, i.e. a URI of a `Grant`, is provided in *activity A*'s
  [capability][prop-capability] property
- If the actor managing the resource (from now on *the resource actor*)
  requires an OCAP for the action being requested by *activity A*, it MUST deny
  the activity unless all of the following holds:
    - The activity referred by the OCAP is a `Grant` activity
    - The `Grant` activity's [actor][] is indeed the *resource actor*, and the
      *resource actor* can verify that it indeed published a `Grant` with the
      given URI
    - The `Grant`'s [context][] is the resource that *activity A* is requesting
      to access (to view and/or to modify)
    - The `Grant`'s [target][] is the sender (and [actor][]) of *activity A*
    - The action being requested by *activity A* to perform on the resource is
      within what the *resource actor* permits for the role specified by the
      `Grant`'s [object][]

### Identifying resources and their managing actors

Some shared resources are themselves actors, and some shared resources aren't
actors, but they are child objects of actors. When some actor *A* wishes to
access a resource *R* and perform a certain operation, it needs to determine
which actor to contact in order to request that operation. Actor *A* then looks
at resource *R*, and the following MUST hold:

- Either the resource *R* isn't an actor (i.e. doesn't have an [inbox][]) but
  does specify which actor manages it via the [managedBy][prop-managedby]
  property ;
- Or the resource *R* is an actor, i.e. it has an [inbox][] (it doesn't have to
  specify [managedBy][prop-managedby], but if it does, then it MUST refer to
  itself)

Therefore any object that wishes to be specified as the [context][] of a
[Grant][act-grant] MUST either be an actor or be [managedBy][prop-managedby] an
actor.

### Initial Grant upon resource creation

When an actor *A* requests to create a new shared resource *R*, and the
*resource actor* approves and creates it, then the *resource actor* SHOULD send
a `Grant` to actor *A*, which provides actor *A* with access to resource *R*.

Typically, this `Grant` would provide actor *A* with what the *resource actor*
considers full/admin access to resource *R*, which would typically include the
ability to gives access to resource *R* to more actors (using an [Invite][]
activity, see below).

If such a `Grant` is sent by the *resource actor* upon the creation of resource
*R*, then the `Grant`'s [fulfills][prop-fulfills] property MUST be provided and
specify the ID URI of the activity (published by actor *A*) that requested to
create resource *R* (typically this would be an [Offer][] activity, see
[Object Publishing and Hosting](#publishing)).

### Offering access using Invite activities

When an actor *A* wishes to offer actor *B* access to resource *R* (where the
*resource actor* who manages *R* is neither *A* nor *B*), then actor *A* SHOULD
use an [Invite][] activity, and the following steps:

1. Actor *A* publishes and delivers an [Invite][], at least to actor
   *B* and to the *resource actor* of *R*, with a relevant
   [capability][prop-capability] (see [Modeling specification][model-invite]
   for details on the properties to use)
2. If actor *B* wishes to have the offered access, it publishes and delivers
   (at least to the *resource actor* of *R*) an [Accept][] activity whose
   [object][] specifies the `Invite` sent by actor *A*
3. The *resource actor* of *R* receives the `Invite` and the `Accept` and:
    a. Verifies the `Invite` is authorized, as described above in
       [Object capabilities using Grant activities](#s2s-grant-flow)
    b. Verifies that the `Accept`'s [object][] specifies the `Invite` and the
       `Accept`'s [actor][] is the `Invite`'s [object][]
    c. Publishes and delivers a [Grant][act-grant] activity (see
       [Modeling specification][model-grant] for more details on the
       properties) where:
        - [object][] is the `Invite`'s [instrument][]
        - [context][] is the `Invite`'s [target][], which is resource *R*
        - [target][] is the `Invite`'s [object][], which is actor *B*
        - [fulfills][prop-fulfills] is the `Invite`

Actor *B* can now use the URI of that new `Grant` as the
[capability][prop-capability] when it sends activities that access or
manipulate resource *R*.

### Requesting access using Join activities

When an actor *A* wishes to request access to resource *R* (where the *resource
actor* who manages *R* isn't *A*), then actor *A* SHOULD use a
[Join][] activity, and the following steps. There are two options detailed
below, depending on whether actor *A* has been previously given a
[Grant][act-grant] authorizing it to gain access to resource *R* without
needing someone else to approve. For example, perhaps actor *A* already has
some access to a resource collection to which *R* belongs, and that access
allows *A* to freely `Join` *R* without needing to wait for human approval.

**Option 1: Actor *A* already has a `Grant` allowing it to gain access to *R*
without external approval:**

1. Actor *A* publishes and delivers a [Join][], at least to the
   *resource actor* of *R*, with the relevant [capability][prop-capability] it
   has (see [Modeling specification][model-join] for details on the properties
   to use)
2. The *resource actor* of *R* receives the `Join` and:
    a. Verifies the `Join` is authorized, as described above in
       [Object capabilities using Grant activities](#s2s-grant-flow)
    b. Publishes and delivers a [Grant][act-grant] activity (see
       [Modeling specification][model-grant] for more details on the
       properties) where:
        - [object][] is the `Join`'s [instrument][]
        - [context][] is the `Join`'s [object][], which is resource *R*
        - [target][] is the `Join`'s [actor][], which is actor *A*
        - [fulfills][prop-fulfills] is the `Join`

Actor *A* can now use the URI of that new `Grant` as the
[capability][prop-capability] when it sends activities that access or
manipulate resource *R*.

**Option 2: Actor *A* doesn't have (or chooses not to use) a `Grant` allowing
it to gain access to *R* without external approval:**

1. Actor *A* publishes and delivers a [Join][], at least to the
   *resource actor* of *R* (see [Modeling specification][model-join] for
   details on the properties to use)
2. If some actor *B*, that has previously received a `Grant` from the *resource
   actor* of *R* authorizing it to approve joins, sees the `Join` sent by actor
   *A* and decides to approve it, then actor *B* publishes and delivers (at
   least to the *resource actor* of *R*) an [Accept][] activity whose
   [object][] specifies the `Join` sent by actor *A*
3. The *resource actor* of *R* receives the `Join` and the `Accept` and:
    a. Verifies the `Accept` is authorized, as described above in
       [Object capabilities using Grant activities](#s2s-grant-flow)
    b. Verifies that the `Accept`'s [object][] specifies the `Join`
    c. Publishes and delivers a [Grant][act-grant] activity (see
       [Modeling specification][model-grant] for more details on the
       properties) where:
        - [object][] is the `Join`'s [instrument][]
        - [context][] is the `Join`'s [object][], which is resource *R*
        - [target][] is the `Join`'s [actor][], which is actor *A*
        - [fulfills][prop-fulfills] is the `Join`

Actor *A* can now use the URI of that new `Grant` as the
[capability][prop-capability] when it sends activities that access or
manipulate resource *R*.

### Example

Aviva creates a new [Repository][type-repository] for her 3D Tree Growth
Simulation software:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://forge.community/users/aviva/outbox/oU6QGAqr-create-treesim",
    "type": "Create",
    "actor": "https://forge.community/users/aviva",
    "to": [
        "https://forge.community/users/aviva/followers"
    ],
    "object": {
        "id": "https://forge.community/repos/treesim",
        "type": "Repository",
        "name": "Tree Growth 3D Simulation",
        "summary": "A graphical simulation of trees growing"
    }
}
```

The newly created *treesim* `Repository` automatically sends back a `Grant` to
Aviva, allowing her full access to the repo:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://forge.community/repos/treesim/outbox/2NwyPWMX-grant-admin-to-aviva",
    "type": "Grant",
    "actor": "https://forge.community/repos/treesim",
    "to": [
        "https://forge.community/aviva",
        "https://forge.community/aviva/followers"
    ],
    "object": "https://roles.example/admin",
    "context": "https://forge.community/repos/treesim",
    "target": "https://forge.community/aviva",
    "fulfills": "https://forge.community/users/aviva/outbox/oU6QGAqr-create-treesim"
}
```

Aviva can now use this `Grant`, e.g. to update the repo's description text:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://forge.community/users/aviva/outbox/RmTygyuj",
    "type": "Update",
    "actor": "https://forge.community/users/aviva",
    "to": [
        "https://forge.community/users/aviva/followers",
        "https://forge.community/repos/treesim",
        "https://forge.community/repos/treesim/followers"
    ],
    "object": {
        "id": "https://forge.community/repos/treesim",
        "type": "Repository",
        "name": "Tree Growth 3D Simulation",
        "summary": "Tree growth 3D simulator for my nature exploration game"
    },
    "capability": "https://forge.community/repos/treesim/outbox/2NwyPWMX-grant-admin-to-aviva"
}
```

Aviva wants to keep track of events related to the *treesim* repo:

```json
{
    "@context": "https://www.w3.org/ns/activitystreams",
    "id": "https://forge.community/users/aviva/outbox/gqtpAhm2",
    "type": "Follow",
    "actor": "https://forge.community/users/aviva",
    "to": "https://forge.community/repos/treesim",
    "object": "https://forge.community/repos/treesim",
}
```

Aviva can invite Luke to have access to the *treesim* repo:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://forge.community/users/aviva/outbox/qfrEGqnC-invite-luke",
    "type": "Invite",
    "actor": "https://forge.community/users/aviva",
    "to": [
        "https://forge.community/aviva/followers",
        "https://forge.community/repos/treesim",
        "https://forge.community/repos/treesim/followers",
        "https://software.site/people/luke",
        "https://software.site/people/luke/followers"
    ],
    "instrument": "https://roles.example/maintainer",
    "target": "https://forge.community/repos/treesim",
    "object": "https://software.site/people/luke",
    "capability": "https://forge.community/repos/treesim/outbox/2NwyPWMX-grant-admin-to-aviva"
}
```

And it appears that Luke accepts the invitation:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://software.site/people/luke/activities/mEYYmt8u",
    "type": "Accept",
    "actor": "https://software.site/people/luke",
    "to": [
        "https://forge.community/aviva",
        "https://forge.community/aviva/followers",
        "https://forge.community/repos/treesim",
        "https://forge.community/repos/treesim/followers",
        "https://software.site/people/luke/followers"
    ],
    "object": "https://forge.community/users/aviva/outbox/qfrEGqnC-invite-luke"
}
```

Seeing the `Invite` and the `Accept`, the *treesim* repo sends Luke a `Grant`
giving him the access that Aviva offered, and which he accepted:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://forge.community/repos/treesim/outbox/D5uod3pz-grant-maintainer-to-luke",
    "type": "Grant",
    "actor": "https://forge.community/repos/treesim",
    "to": [
        "https://forge.community/aviva",
        "https://forge.community/aviva/followers",
        "https://forge.community/repos/treesim/followers",
        "https://software.site/people/luke",
        "https://software.site/people/luke/followers"
    ],
    "object": "https://roles.example/maintainer",
    "context": "https://forge.community/repos/treesim",
    "target": "https://software.site/people/luke",
    "fulfills": "https://forge.community/users/aviva/outbox/qfrEGqnC-invite-luke"
}
```

Luke can now use this `Grant`, e.g. to delete some old obsolete branch of the
*treesim* repo:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://software.site/people/luke/activities/vShj2aIe",
    "type": "Delete",
    "actor": "https://software.site/people/luke",
    "to": [
        "https://forge.community/repos/treesim",
        "https://forge.community/repos/treesim/followers",
        "https://software.site/people/luke/followers"
    ],
    "object": "https://forge.community/repos/treesim/branches/fixes-for-release-0.1.3",
    "origin": "https://forge.community/repos/treesim",
    "capability": "https://forge.community/repos/treesim/outbox/D5uod3pz-grant-maintainer-to-luke"
}
```

Celine requests to have developer access to the *treesim* repo:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://dev.online/@celine/sent/v5Qvd6bB-celine-join",
    "type": "Join",
    "actor": ""https://dev.online/@celine",
    "to": [
        "https://forge.community/repos/treesim",
        "https://forge.community/repos/treesim/followers",
        "https://dev.online/@celine/followers"
    ],
    "object": ""https://forge.community/repos/treesim",
    "instrument": "https://roles.example/developer"
}
```

Aviva sees the `Join` request, talks with Celine and decides to approve her
request:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://forge.community/users/aviva/outbox/PzRtDydu",
    "type": "Accept",
    "actor": "https://forge.community/users/aviva",
    "to": [
        "https://forge.community/repos/treesim",
        "https://forge.community/repos/treesim/followers",
        "https://dev.online/@celine",
        "https://dev.online/@celine/followers"
    ],
    "object": "https://dev.online/@celine/sent/v5Qvd6bB-celine-join",
    "capability": "https://forge.community/repos/treesim/outbox/2NwyPWMX-grant-admin-to-aviva"
}
```

Seeing the `Join` and the `Accept`, the *treesim* repo sends Celine a `Grant`
giving her the access that she requested, and which Aviva approved:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://forge.community/repos/treesim/outbox/D5uod3pz-grant-developer-to-celine",
    "type": "Grant",
    "actor": "https://forge.community/repos/treesim",
    "to": [
        "https://forge.community/aviva",
        "https://forge.community/repos/treesim/followers",
        "https://dev.online/@celine",
        "https://dev.online/@celine/followers"
    ],
    "object": "https://roles.example/developer",
    "context": "https://forge.community/repos/treesim",
    "target": "https://dev.online/@celine",
    "fulfills": "https://dev.online/@celine/sent/v5Qvd6bB-celine-join"
}
```

Celine can now use this `Grant` to access the *treesim* repo.

# Acknowledgements

[act-grant]:  /vocabulary.html#act-grant
[act-push]:   /vocabulary.html#act-push

[type-repository]: /vocabulary.html#type-repository
[type-ticket]:     /vocabulary.html#type-ticket

[prop-capability]:       /vocabulary.html#prop-capability
[prop-fulfills]:         /vocabulary.html#prop-fulfills
[prop-managedby]:        /vocabulary.html#prop-managedby
[prop-team]:             /vocabulary.html#prop-team
[prop-ticketstrackedby]: /vocabulary.html#prop-ticketstrackedby
[prop-tracksticketsfor]: /vocabulary.html#prop-tracksticketsfor

[model-comment]: /modeling.html#comment
[model-grant]:   /modeling.html#grant
[model-invite]:  /modeling.html#invite
[model-join]:    /modeling.html#join
[model-push]:    /modeling.html#push
[model-ticket]:  /modeling.html#ticket

[Accept]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-accept
[Create]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-create
[Invite]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-invite
[Join]:   https://www.w3.org/TR/activitystreams-vocabulary/#dfn-join
[Offer]:  https://www.w3.org/TR/activitystreams-vocabulary/#dfn-offer
[Reject]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-reject

[Image]:  https://www.w3.org/TR/activitystreams-vocabulary/#dfn-image
[Note]:   https://www.w3.org/TR/activitystreams-vocabulary/#dfn-note
[Object]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-object

[actor]:        https://www.w3.org/TR/activitystreams-vocabulary/#dfn-actor
[attributedTo]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-attributedto
[content]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-content
[context]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-context
[followers]:    https://www.w3.org/TR/activitypub/#followers
[id]:           https://www.w3.org/TR/activitystreams-vocabulary/#dfn-id
[inbox]:        https://www.w3.org/TR/activitystreams-vocabulary/#dfn-inbox
[instrument]:   https://www.w3.org/TR/activitystreams-vocabulary/#dfn-instrument
[result]:       https://www.w3.org/TR/activitystreams-vocabulary/#dfn-result
[summary]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-summary
[target]:       https://www.w3.org/TR/activitystreams-vocabulary/#dfn-target
[to]:           https://www.w3.org/TR/activitystreams-vocabulary/#dfn-to
[type]:         https://www.w3.org/TR/activitystreams-vocabulary/#dfn-type

[RFC2119]: https://tools.ietf.org/html/rfc2119
