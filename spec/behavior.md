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

### Object capabilities

#### Introduction {#s2s-grant-simple}

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

Providing the `Grant` ID URI like that when requesting to interact with a
resource is called an *invocation* of the `Grant`. There is another operation
possible with a `Grant` though: An actor can *delegate* a `Grant` it has
received, i.e. pass on the access, giving it to more actors. Delegation is
covered in a [later section](#s2s-grant-flow); for now let's assume `Grant`s
are used only for invocation. We therefore get the following simplified
validation process.

When an actor *R* receives from actor *A* a request to access/modify a resource
*r*, where the request is expressed as an activity *a* whose
[capability][prop-capability] field specifies some other activity *g*, then *R*
can validate *a* (i.e. decide whether or not to perform the requested action)
using the following steps:

1. Resource *r* MUST be a resource that *R* manages (it may be *R* itself)
2. *g*'s [type][] MUST be [Grant][act-grant]
3. *g*'s [context][] MUST be *r*
4. *g*'s [target][] MUST be *A*
5. Verify that *g* doesn't specify [delegates][prop-delegates]
6. *g*'s [actor][] MUST be *R*
7. Verify that *R* indeed published *g* and considers it an active grant
   (i.e. *R* hasn't disabled/revoked it)
8. *checkLeaf(g):*
    a. *g*'s [allows][prop-allows] MUST be [invoke][type-usage]
    b. Actor *A* SHOULD be of a [type][] to which *R* allows to perform
       activity *a* on resource *r*, i.e. *A* should probably be a [Person][],
       or some automated service/bot
9. Verify that the action being requested by activity *a* to perform on
   resource *r* is within what *R* permits for role specified by *g*'s
   [object][]

At this point, activity *a* is considered authorized, and the requested action
may be performed.

#### Direct Granting

When an actor *R*, managing some resource *r*, wishes to allow some other actor
*A* to interact with *r*, under the conditions and permissions specified by
role *p*, then actor *R* can send to actor *A* a [Grant][act-grant] activity
with the following properties:

- [actor][]: Specifies actor *R*
- [context][]: Specifies resource *r*
- [target][]: Specifies actor *A*
- [object][]: Specifies role *p*
- [allows][prop-allows]: Specifies [invoke][type-usage]
- [delegates][prop-delegates]: Not used

#### Granting the delegator role {#grant-delegator}

A special case of direct granting is *granting permission to delegate*: If role
*p* is [delegator][type-role], then the `Grant` [actor][] is allowing the
[target][] to delegate `Grant`s to the [actor][], i.e. to send `Grant`s meant
for delegation or `Grants` that are themselves delegations of other `Grant`s
(either start a chain, or extend a chain that some other actor started). More
on delegation in the next sections.

When an actor *A* wishes to allow some other actor *R* to delegate `Grant`s to
actor *A*, then actor *A* can send to actor *R* a [Grant][act-grant] activity
with the following properties:

- [actor][]: Specifies actor *A*
- [context][]: Specifies actor *A*
- [target][]: Specifies actor *R*
- [object][]: Specifies [delegator][type-role]
- [allows][prop-allows]: Specifies [invoke][type-usage]
- [delegates][prop-delegates]: Not used

#### Starting a delegation chain

When an actor *R*, managing some resource *r*, wishes to allow or request some
other actor *A* to delegate some access-to-*r*-under-role-*p* to certain (or
any) other actors that *A* knows, then actor *R* can send to actor *A* a
[Grant][act-grant] activity with the following properties:

- [actor][]: Specifies actor *R*
- [context][]: Specifies resource *r*
- [target][]: Specifies actor *A*
- [object][]: Specifies role *p*
- [allows][prop-allows]: Specifies the conditions under which actor *A* may
  delegate this `Grant` (i.e. conditions under which actor *R* will consider
  the delegation valid when verifying the chain), and what the recipients of
  the delegtaions that *A* will send (which are themselves `Grant` activites)
  are allowed to do with these `Grants` (invoke? further delegate to certain
  other actors?)
- [delegates][prop-delegates]: Not used
- [capability][prop-capability]: *(optional)* Specifies a
  [delegator Grant](#grant-delegator) previously given by *A* to *R*

The following cases are supported in ForgeFed for starting a delegation chain.
The term 'component' used below refers to a forge related service actor. This
may be a service of a [type][] defined in ForgeFed (such as
[Repository][type-repository], [TicketTracker][type-tickettracker],
[PatchTracker][type-patchtracker]), or a service defined in some extension.

1. [actor][] is a component, [target][] is a [Project][type-project]
    - Scenario: A component delegates access-to-a-resource-it-manages (which is
      often simply itself) to a project to which the component belongs
    - [allows][prop-allows] value to use: [gatherAndDistribute][type-usage]
    - Conditions for the target project:
        * It SHOULD delegate the `Grant`, allowing only `gatherAndConvey`, to
          its own parent projects
        * It SHOULD delegate the `Grant`, allowing only `distribute`, to teams
          to which it allows to access it
        * It SHOULD delegate the `Grant`, allowing only `invoke`, to people and
          bots to which it allows to access it
        * It SHOULD NOT make any other delegation of this `Grant`, and SHOULD
          NOT invoke it
2. [actor][] is a [Project][type-project], [target][] is a parent
   [Project][type-project] of it
    - Scenario: A project delegates access-to-a-resource-itself to its parent
      project
    - [allows][prop-allows] value to use: Same as 1
    - Conditions for the target project: Same as 1
3. [actor][] is a component, [target][] is a [Team][type-team]
    - Scenario: A component delegates access-to-a-resource-it-manages to a team
      that has been approved to access the component
    - [allows][prop-allows] value to use: [distribute][type-usage]
    - Conditions for the target team:
        * It SHOULD delegate the `Grant`, allowing `distribute` only, to its
          subteams
        * It SHOULD delegate the `Grant`, allowing `invoke` only, to its
          members
        * It SHOULD NOT make any other delegation of this `Grant`, and SHOULD
          NOT invoke it
4. [actor][] is a [Project][type-project], [target][] is a [Team][type-team]
    - Scenario: A project delegates access-to-itself to a team that has been
      approved to access the project
    - [allows][prop-allows] value to use: Same as 3
    - Conditions for the target project: Same as 3

#### Extending a delegation chain

When an actor *A* receives a [Grant][act-grant] activity *g* where the
[target][] is *A*, and wishes to pass on the granted access to some other actor
*B* (who isn't the [actor][] of that `Grant`), then actor *A* can do so by
sending to actor *B* a new `Grant` activity *h* in which:

- [actor][] is actor *A*
- [context][] (i.e. the resource) is same as *g*'s [context][]
- [target][] is actor *B*
- [object][] (i.e. the granted role) is either *g*'s [object][] or a
  lower-access role than *g*'s [object][], i.e. provides a subset of the
  permissions that *g*'s [object][] provides (the latter case is called
  *attenuation*)
- [allows][prop-allows]: Specifies the conditions under which actor *B* may
  delegate this `Grant` (i.e. conditions under which the delegation will be
  considered valid when verifying the chain), and what the recipients of
  the delegtaions that *B* will send (which are themselves `Grant` activites)
  are allowed to do with these `Grants` (invoke? further delegate to certain
  other actors?)
- [delegates][prop-delegates] is activity *g*
- [capability][prop-capability]: *(optional)* Specifies a
  [delegator Grant](#grant-delegator) previously given by *B* to *A*
- [result][]: a URI that will be used later to verify that *h* is still active
  and hasn't been revoked

The [result][] URI MUST be provided whenever extending a delegation chain. It
MUST be a URI that actor *A* controls, i.e. decides what will be returned by
HTTP requests to that URI. Requirements:

- From the moment that actor *A* publishes activity *h*, as long as actor *A*
  considers *h* an active `Grant` and hasn't revoked it, any HTTP HEAD or HTTP
  GET request the [result][] URI MUST return an HTTP response status 204 or
  200.
- If later activity *h* is revoked, or actor *A* is deleted, then from the
  moment that actor *A* considers *h* deactivated, any HTTP HEAD or HTTP GET
  request to the [result][] URI MUST NOT return an HTTP response status in the
  200-299 range. The response status SHOULD be 410 or 404.

In the following cases, *g* is a *request* for actor *A* to extend the
delegation chain, and actor *A* SHOULD extend the chain by sending `Grant`
activities, as described for each case.

The term 'component' used below refers to a forge related service actor. This
may be a service of a [type][] defined in ForgeFed (such as
[Repository][type-repository], [TicketTracker][type-tickettracker],
[PatchTracker][type-patchtracker]), or a service defined in some extension.

1. Actor *A* is a [Project][type-project], AND *g*'s [actor][] is either a
   [component][prop-components] of *A* or a [subproject][prop-subprojects] of
   *A*, AND *g*'s [allows][prop-allows] is a single value
   [gatherAndConvey][type-usage]
    - Scenario: Project *A* received some access from a component/subproject of
      it, and is requested to pass it on its member people, to its member
      teams, and to its parent projects
    - Requirements for extending the delegation chain:
        a. For each parent project *P* of project *A*, project *A* SHOULD
           publish and deliver to *P* a `Grant` activity in which:
            - [actor][] is project *A*
            - [context][] (i.e. the resource) is same as *g*'s [context][]
            - [target][] is project *P*
            - [object][] (i.e. the granted role) is either *g*'s [object][] or
              a lower-access role than *g*'s [object][]
            - [allows][prop-allows] is a single value
              [gatherAndConvey][type-usage]
            - [delegates][prop-delegates] is activity *g*
            - [capability][prop-capability]: *(optional)* Specifies a
              [delegator Grant](#grant-delegator) previously given by *P* to *A*
            - [result][]: a URI that will be used later to verify that *h* is
              still active and hasn't been revoked

        b. For each team *T* that project *A* considers a member team with role
           *p*, project *A* SHOULD publish and deliver to *T* a `Grant`
           activity in which:
            - [actor][] is project *A*
            - [context][] (i.e. the resource) is same as *g*'s [context][]
            - [target][] is team *T*
            - [object][] (i.e. the granted role) is the lower-access role
              among *g*'s [object][] and *p*
            - [allows][prop-allows] is a single value [distribute][type-usage]
            - [delegates][prop-delegates] is activity *g*
            - [capability][prop-capability]: *(optional)* Specifies a
              [delegator Grant](#grant-delegator) previously given by *T* to *A*
            - [result][]: a URI that will be used later to verify that *h* is
              still active and hasn't been revoked

        c. For each [Person][] or automated service bot *M* (that isn't a team)
           that project *A* considers a member with role *p*, project *A*
           SHOULD publish and deliver to *M* a `Grant` activity in which:
            - [actor][] is project *A*
            - [context][] (i.e. the resource) is same as *g*'s [context][]
            - [target][] is actor *M*
            - [object][] (i.e. the granted role) is the lower-access role
              among *g*'s [object][] and *p*
            - [allows][prop-allows] is a single value [invoke][type-usage]
            - [delegates][prop-delegates] is activity *g*
            - [capability][prop-capability]: *(optional)* Specifies a
              [delegator Grant](#grant-delegator) previously given by *M* to *A*
            - [result][]: a URI that will be used later to verify that *h* is
              still active and hasn't been revoked

        d. Project *A* MUST NOT make any other delegations of *g*, and SHOULD
           NOT try to invoke it

2. Actor *A* is a [Team][type-team], AND *g*'s [actor][] is either a
   component/[Project][type-project] in which *A* is a member or a
   [parent team][prop-subteams] of *A*, AND *g*'s [allows][prop-allows] is a
   single value [distribute][type-usage]
    - Scenario: Team *A* received some access from a component/project that
      considers *A* a member team, or from a parent team of *A*, and *A* is
      requested to pass it on its member people and to its subteams
    - Requirements for extending the delegation chain:
        a. For each team *T* that team *A* considers a
          [subteam][prop-subteams], team *A* SHOULD publish and deliver to *T*
          a `Grant` activity in which:
            - [actor][] is team *A*
            - [context][] (i.e. the resource) is same as *g*'s [context][]
            - [target][] is team *T*
            - [object][] (i.e. the granted role) is the same as
              *g*'s [object][]
            - [allows][prop-allows] is a single value [distribute][type-usage]
            - [delegates][prop-delegates] is activity *g*
            - [capability][prop-capability]: *(optional)* Specifies a
              [delegator Grant](#grant-delegator) previously given by *T* to *A*

        b. For each [Person][] or automated service bot *M* (that isn't a team)
           that team *A* considers a member with role *p*, team *A*
           SHOULD publish and deliver to *M* a `Grant` activity in which:
            - [actor][] is team *A*
            - [context][] (i.e. the resource) is same as *g*'s [context][]
            - [target][] is actor *M*
            - [object][] (i.e. the granted role) is the lower-access role
              among *g*'s [object][] and *p*
            - [allows][prop-allows] is a single value [invoke][type-usage]
            - [delegates][prop-delegates] is activity *g*
            - [capability][prop-capability]: *(optional)* Specifies a
              [delegator Grant](#grant-delegator) previously given by *M* to *A*

        c. Team *A* MUST NOT make any other delegations of *g*, and SHOULD NOT
           try to invoke it

#### Revoking a Grant {#s2s-revoke}

At any point after an actor *A* publishes a [Grant][model-grant] in which it
grants some actor *B* access to a resource that actor *A* manages, actor *A*
MAY cancel that `Grant`, deciding it's no longer a valid OCAP to use via the
[capability][prop-capability] property of activies that actor *B* sends.

If actor *A* cancels such a `Grant`, it SHOULD publish and deliver, at least to
actor *B*, a [Revoke][act-revoke] activity notifying about the canceled
`Grant`. In the `Revoke` activity, actor *A* MUST provide at least one of the
following sets of properties:

1. Describe the `Grant`s being canceled:
    - [object][]: all the `Grant` activities being undone, i.e. the access
      that they granted is now disabled
2. Describe the access being canceled:
    - [origin][]: The actor whose access to the resource is being revoked, i.e.
      actor *B*
    - [instrument][]: The role or permission that the [origin][] actor had with
      respect to accessing the resource, and which is now being taken away
    - [context][]: The resource, access to which is being revoked
    - [allows][prop-allows]: Modes of invocation and/or delegation that the
      canceled access allowed

Actor *A* MAY provide both sets of properties. If it does, then:

- The `Revoke`'s `origin` MUST be identical to the `target` of every `Grant`
  listed as an `object` in the `Revoke`
- The `Revoke`'s `instrument` MUST be identical to the `object` of every
  `Grant` listed as an `object` in the `Revoke`
- The `Revoke`'s `context` MUST be identical to the `context` of every `Grant`
  listed as an `object` in the `Revoke`
- The `Revoke`'s `allows` MUST be identical to the `allows` of every `Grant`
  listed as an `object` in the `Revoke`

Additional requirements:

- If the canceled access includes `Grant`s that are delegations (i.e. specify
  the [delegates][prop-delegates] property), then the `Revoke` activity MUST
  provide the [object][] property, and have it list *all* canceled `Grant`s,
  not just the ones that are delegations
- Implementations displaying a `Revoke` activity or an interpretation of it in
  a human interface MUST examine the `Revoke`'s [object][] property if it is
  present, check if any of the `Grant`s listed are delegations, and communicate
  that detail in the human interface

Once actor *A* publishes the `Revoke`, it MUST from now on refuse to execute
requests from actor *B* to access resources that actor *A* manages, coming as
activities that specify any of the canceled `Grant`s in the `capability`
property. If actor *A* receives such an activity from actor *B*, it SHOULD
publish and send back a [Reject][] activity, whose [object][] specifies the
activity that actor *B* sent.

If the `Grant` that actor *A* is revoking specifies a [result][], then from now
on any HTTP HEAD request to the URI specified by [result][] MUST NOT return an
HTTP response status in the 200-299 range. The returned status SHOULD be 410
or 404. See [Extending a delegation chain](#extending-a-delegation-chain) for
more information.

#### Verifying an invocation {#s2s-grant-flow}

A [previous section](#s2s-grant-simple) described *direct* usage of
[Grant][act-grant]s, where the *resource actor* gives some access to a *target
actor*, and the *target actor* then uses it to interact with the resource.
Another way to give authorization is via delegation chains:

- The *resource actor* passes access to a *target actor*, allowing (or
  requesting) the *target actor* to pass this access (or reduced access) on to
  more actors
- If authorized by the delegation, those actors may further pass on the access
  (possibly reduced)
- Eventually, an actor that received such a delegation may use it to access the
  resource

Access is delegated using [Grant][act-grant] activities as well, using the
[delegates][prop-delegates] property to point from each `Grant` in the chain to
the previous one. The "direct" `Grant` discussed earlier is simply a delegation
chain of length 1.

When an actor *R* receives from actor *A* a request to access/modify a resource
*r*, where the request is expressed as an activity *a* whose
[capability][prop-capability] field specifies some other activity *g*, then *R*
can validate *a* (i.e. decide whether or not to perform the requested action)
using the following steps.

*R* begins by verifying that resource *r* is indeed a resource that *R* manages
(it may be *R* itself). Otherwise, verification has failed.

*R* proceeds by collecting the delegation chain in a list, by traversing the
chain backwards from the leaf all the way to the beginning of the chain. The
traversal starts with the list *L* being empty, and *R* examines activity *g*:

1. *g*'s [type][] MUST be [Grant][act-grant]
2. *g*'s [context][] MUST be *r*
3. *g*'s [target][] MUST be *A*
4. *g* MUST NOT already be listed in *L*
5. Look at *g*'s [delegates][prop-delegates]:
    - If *g* doesn't specify [delegates][prop-delegates]:
        a. *g*'s [actor][] MUST be *R*
        b. Verify that *R* indeed published *g* and considers it an active
           grant (i.e. *R* hasn't disabled/revoked it)
        c. Prepend *g* to the beginning of *L*, resulting with new list *M*
        d. We're done with the traversal step, the output is *M*
    - If *g*'s [delegates][prop-delegates] is some activity *h*:
        a. *g*'s [actor][] MUST NOT be *R*
        b. *g* MUST specify exactly one [result][] URI
        c. Verify the [result][] URI:
            i. Send an HTTP HEAD request to that URI
            ii. The HTTP response status MUST be 200 or 204
        d. Prepend *g* to the beginning of *L*, resulting with new list *M*
        e. Continue traversal by going back to step 1, but with *M* being the
           list, and with *g*'s [actor][] instead of *A*, and now examining
           activity *h*

*R* proceeds by traversing the resulting list *L* from the beginning forward,
all the way to the leaf, validating and tracking attenuation in each step. *R*
starts this by examining the first item in *L*, let's call this item *g*:

1. Let *p* be *g*'s [object][]
2. Examine *g*'s position in *L*:
    - If *g* is the last item in *L*:
        a. Perform *checkLeaf* on *g* (see below)
        b. Verify that the action being requested by activity *a* to perform on
           resource *r* is within what *R* permits for role *p*.
        c. We're done with the traversal!
    - Otherwise:
        a. Let *h* be the next item after *g* in *L*
        b. Let *q* be *h*'s [object][]
        c. The permissions that role *q* allows on resource *r* MUST be
           identical to or a subset of the permissios that role *p* allows on
           *r*
        d. Perform *checkItem* on *(g, h)* (see below)
        e. Continue traversal by going back to step 2, but with *h* instead of
           *g* and *q* instead of *p*

The steps *checkLeaf* and *checkItem* mentioned above MAY be extended by
implementations, by using custom values in the [allows][prop-allows] property.
But here are the standard definitions, using the values defined in ForgeFed:

*checkLeaf (g):*

1. *g*'s [allows][prop-allows] MUST be [invoke][type-usage]
2. *g*'s [target][] (which is actor *A*, the sender of activity *a*) SHOULD be
   an actor of a [type][] to which *R* allows to perform activity *a* on
   resource *r*, i.e. *A* should probably be a [Person][], or some automated
   service/bot

*checkItem (g, h):*

1. *g* MUST specify exactly one value for [allows][prop-allows]
2. That value MUST be either [gatherAndConvey][type-usage] or
   [distribute][type-usage]
    - If it's [gatherAndConvey][type-usage]:
        a. *g*'s [target][] MUST be a [Project][type-project]
    - If it's [distribute][type-usage]:
        a. *g*'s [target][] MUST be a [Team][type-team]
        b. *h*'s [allows][prop-allows] MUST be either [distribute][type-usage]
           or [invoke][type-usage]

At this point, activity *a* is considered authorized, and the requested action
may be performed.

#### Identifying resources and their managing actors {#manager}

Some shared resources are themselves actors. Some shared resources aren't
actors, but they are child objects of actors. When some actor *A* wishes to
access a resource *R* and perform a certain operation, it needs to determine
which actor to contact in order to request that operation. Actor *A* then looks
at resource *R*, and the following MUST hold:

- Either the resource *R* isn't an actor (i.e. doesn't have an [inbox][]) but
  does specify which actor manages it via the [managedBy][prop-managedby]
  property;
- Or the resource *R* is an actor, i.e. it has an [inbox][] (it doesn't have to
  specify [managedBy][prop-managedby], but if it does, then it MUST refer to
  itself)

Therefore any object that wishes to be specified as the [context][] of a
[Grant][act-grant] MUST either be an actor or be [managedBy][prop-managedby] an
actor.

#### Invoking a Grant

Invoking a [Grant][act-grant] means using the `Grant` to authorize a request to
access or modify some resource. If some actor *A* wishes to access or modify a
resource *r*, using a `Grant` activity *g* for authorization, preconditions
for a successful invocation include:

- *g*'s [target][] is actor *A*
- *g*'s [context][] is either the resource *r*, or a resource in which *r* is
  contained, or the actor that [manages][prop-managedby] *r*
- *g*'s [object][] is a [Role][type-role] that permits the kind of operation
  that actor *A* is requesting to do on resource *r*
- *g*'s [allows][prop-allows] is [invoke][type-usage]

When actor *A* sends the activity *a* that requests to access or modify
resource *r*, it can use *g* for authorization by specifying its [id][] URI in
the [capability][prop-capability] property of activity *a*.

To have a chance to access resource *r*, actor *A* needs to deliver activity
*a* to the actor that manages *r*. [See above](#manager) instructions for
determining who that actor is.

### Granting access

#### Initial Grant upon resource creation

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

#### Offering access using Invite activities

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
       [Verifying an invocation](#s2s-grant-flow)
    b. Verifies that the `Accept`'s [object][] specifies the `Invite` and the
       `Accept`'s [actor][] is the `Invite`'s [object][]
    c. Publishes and delivers a [Grant][act-grant] activity (see
       [Modeling specification][model-grant] for more details on the
       properties) where:
        - [object][] is the `Invite`'s [instrument][]
        - [context][] is the `Invite`'s [target][], which is resource *R*
        - [target][] is the `Invite`'s [object][], which is actor *B*
        - [fulfills][prop-fulfills] is the `Invite`
        - [allows][prop-allows] is [invoke][type-usage]
        - [delegates][prop-delegates] isn't specified

Actor *B* can now use the URI of that new `Grant` as the
[capability][prop-capability] when it sends activities that access or
manipulate resource *R*.

#### Requesting access using Join activities

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
       [Verifying an invocation](#s2s-grant-flow)
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
   least to the *resource actor* of *R*) an [Accept][] activity where:
      - [object][] specifies the `Join` sent by actor *A*
      - [capability][prop-capability] is the `Grant` mentioned above,
        authorizing to approve or deny Joins
3. The *resource actor* of *R* receives the `Join` and the `Accept` and:
    a. Verifies the `Accept` is authorized, as described above in
       [Verifying an invocation](#s2s-grant-flow)
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

In step 2, actor *B* may choose to deny the request of actor *A*, by sending a
[Reject][] activity (at least to the *resource actor* of *R*) where:

- [object][] specifies the `Join` that actor *A* sent
- [capability][prop-capability] is the `Grant` mentioned in step 2, authorizing
  actor *B* to approve or deny Joins

If the *resource actor* of *R* receives the `Reject`:

a. It MUST verify the `Reject` is authorized, as described above in
   [Verifying an invocation](#s2s-grant-flow)
b. it MUST verify that the `Reject`'s [object][] specifies the `Join`
c. Consider this `Join` request canceled: If actor *B*, or some other actor
   *C*, tries again to `Accept` the `Join`, then:
      i. The *resource actor* MUST NOT send a `Grant` to actor *A*, even if the
         `Accept` is authorized
      ii. The *resource actor* MAY publish and deliver a `Reject` activity, at
          least to the actor that sent the `Accept`, where [object][] specifies
          the `Accept`
d. It SHOULD publish and deliver a `Reject` activity, at least to actor *A*,
   where [object][] specifies the `Join` that actor *A* sent

So, once a `Join` is rejected (using an authorized `Reject`), it cannot be
accepted. But actor *A* MAY send a new `Join`, which could then possibly get
accepted.

### Revoking access

#### Taking away access using Remove activities

When an actor *A* wishes to cancel the membership of another actor *B* (who
isn't *A*) in a shared resource *R*, invalidating any active
[Grant][model-grant]s that the *resource actor* of *R* has granted to actor
*B*, then actor *A* SHOULD use a [Remove][] activity, and the following steps:

1. Actor *A* publishes and delivers a [Remove][], at least to actor
   *B* and to the *resource actor* of *R*, with a relevant
   [capability][prop-capability] (see [Modeling specification][model-remove]
   for details on the properties to use)
2. The *resource actor* of *R* receives the `Remove` and:
    a. Verifies the `Remove` is authorized, as described above in
       [Verifying an invocation](#s2s-grant-flow)
    b. Verifies that actor *B* indeed has active `Grant`s for accessing
       resource *R*
    c. Marks those Grants as disabled in its internal state
    d. Publishes and delivers a [Revoke][model-revoke] activity, as described
       above in [Revoking a Grant](#s2s-revoke), where
       [fulfills][prop-fulfills] specifies the `Remove`

Actor *B* SHOULD no longer use the URI of any `Grant` that has been disabled as
the [capability][prop-capability] when it sends activities that access or
manipulate resource *R*.

#### Waiving access using Leave activities

When an actor *A* wishes to cancel their membership in a shared resource *R*
(where the *resource actor* who manages *R* isn't *A*), invalidating any active
[Grant][model-grant]s that the *resource actor* of *R* has granted to actor
*A*, then actor *A* SHOULD use a [Leave][] activity, and the following steps:

1. Actor *A* publishes and delivers a [Leave][], at least to the
   *resource actor* of *R* (see [Modeling specification][model-leave] for
   details on the properties to use)
2. The *resource actor* of *R* receives the `Leave` and:
    a. Verifies that actor *A* indeed has active `Grant`s for accessing
       resource *R*
    b. Marks those Grants as disabled in its internal state
    c. Publishes and delivers a [Revoke][model-revoke] activity, as described
       above in [Revoking a Grant](#s2s-revoke), where
       [fulfills][prop-fulfills] specifies the `Leave`

Actor *A* SHOULD no longer use the URI of any `Grant` that has been disabled as
the [capability][prop-capability] when it sends activities that access or
manipulate resource *R*.

#### Requesting to disable specific Grants using Undo

When an actor *A* wishes to deactivate a specific [Grant][model-grant] activity
(or multiple `Grant`s), providing access to view or manipulate some resource
*R* (where the *resource actor* of *R* isn't *A*), then actor *A* SHOULD use an
[Undo][] activity, and the following steps. The actor *B* to whom
access-to-resource-*R* was given by the `Grant` may be actor *A* itself, or
some other actor, as long as actor *A* is authorized by the *resource actor* of
*R* to deactivate that `Grant`.

NOTE: Upon a successful `Undo`, if actor *B* doesn't have any active `Grants`
left, that allow access to resource *R*, then the *resource actor* of *R* MAY
remove actor *B*'s membership in *R*, or it MAY consider actor *B* a member
without access.

1. Actor *A* publishes and delivers an [Undo][], at least to the
   *resource actor* of *R* (see [Modeling specification][model-undo-grant] for
   details on the properties to use)
2. The *resource actor* of *R* receives the `Undo` and:
    a. Verifies the `Undo` is authorized, as described above in
       [Verifying an invocation](#s2s-grant-flow)
    b. Verifies that actor *B* indeed has all the active `Grant`s for accessing
       resource *R*, that are listed as [object][]s of the `Undo` (if more than
       one `Grant` is listed, the [target][] of all the `Grant`s MUST be
       identical)
    c. Marks all of those Grants as disabled in its internal state
    d. Publishes and delivers a [Revoke][model-revoke] activity, at least to
       actors *A* and *B*, as described above in
       [Revoking a Grant](#s2s-revoke), where:
          - [object][] MUST specify all the deactivated `Grant`s
          - [fulfills][prop-fulfills] MUST specify the `Undo`

Actor *B* SHOULD no longer use the URI of any `Grant` that has been disabled as
the [capability][prop-capability] when it sends activities that access or
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
    "fulfills": "https://forge.community/users/aviva/outbox/oU6QGAqr-create-treesim",
    "allows": "invoke"
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
    "fulfills": "https://forge.community/users/aviva/outbox/qfrEGqnC-invite-luke",
    "allows": "invoke"
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
    "fulfills": "https://dev.online/@celine/sent/v5Qvd6bB-celine-join",
    "allows": "invoke"
}
```

Celine can now use this `Grant` to access the *treesim* repo.

# Acknowledgements

[act-grant]:  /vocabulary.html#act-grant
[act-push]:   /vocabulary.html#act-push
[act-revoke]: /vocabulary.html#act-revoke

[type-patchtracker]: /vocabulary.html#type-patchtracker
[type-project]:    /vocabulary.html#type-project
[type-repository]: /vocabulary.html#type-repository
[type-role]:       /vocabulary.html#type-role
[type-team]:       /vocabulary.html#type-team
[type-ticket]:     /vocabulary.html#type-ticket
[type-tickettracker]: /vocabulary.html#type-tickettracker
[type-usage]:      /vocabulary.html#type-usage

[prop-allows]:           /vocabulary.html#prop-allows
[prop-capability]:       /vocabulary.html#prop-capability
[prop-components]:       /vocabulary.html#prop-components
[prop-delegates]:        /vocabulary.html#prop-delegates
[prop-fulfills]:         /vocabulary.html#prop-fulfills
[prop-managedby]:        /vocabulary.html#prop-managedby
[prop-subprojects]:      /vocabulary.html#prop-subprojects
[prop-subteams]:         /vocabulary.html#prop-subteams
[prop-team]:             /vocabulary.html#prop-team
[prop-ticketstrackedby]: /vocabulary.html#prop-ticketstrackedby
[prop-tracksticketsfor]: /vocabulary.html#prop-tracksticketsfor

[model-comment]: /modeling.html#comment
[model-grant]:   /modeling.html#grant
[model-invite]:  /modeling.html#invite
[model-join]:    /modeling.html#join
[model-leave]:   /modeling.html#leave
[model-push]:    /modeling.html#push
[model-remove]:  /modeling.html#remove
[model-revoke]:  /modeling.html#revoke
[model-ticket]:  /modeling.html#ticket
[model-undo-grant]: /modeling.html#undo-grant

[Accept]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-accept
[Create]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-create
[Invite]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-invite
[Join]:   https://www.w3.org/TR/activitystreams-vocabulary/#dfn-join
[Leave]:  https://www.w3.org/TR/activitystreams-vocabulary/#dfn-leave
[Offer]:  https://www.w3.org/TR/activitystreams-vocabulary/#dfn-offer
[Reject]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-reject
[Remove]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-remove
[Undo]:   https://www.w3.org/TR/activitystreams-vocabulary/#dfn-undo

[Image]:  https://www.w3.org/TR/activitystreams-vocabulary/#dfn-image
[Note]:   https://www.w3.org/TR/activitystreams-vocabulary/#dfn-note
[Object]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-object
[Person]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-person

[actor]:        https://www.w3.org/TR/activitystreams-vocabulary/#dfn-actor
[attributedTo]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-attributedto
[content]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-content
[context]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-context
[followers]:    https://www.w3.org/TR/activitypub/#followers
[id]:           https://www.w3.org/TR/activitystreams-vocabulary/#dfn-id
[inbox]:        https://www.w3.org/TR/activitystreams-vocabulary/#dfn-inbox
[instrument]:   https://www.w3.org/TR/activitystreams-vocabulary/#dfn-instrument
[origin]:       https://www.w3.org/TR/activitystreams-vocabulary/#dfn-origin
[result]:       https://www.w3.org/TR/activitystreams-vocabulary/#dfn-result
[summary]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-summary
[target]:       https://www.w3.org/TR/activitystreams-vocabulary/#dfn-target
[to]:           https://www.w3.org/TR/activitystreams-vocabulary/#dfn-to
[type]:         https://www.w3.org/TR/activitystreams-vocabulary/#dfn-type

[RFC2119]: https://tools.ietf.org/html/rfc2119
