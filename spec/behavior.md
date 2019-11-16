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
as described in [RFC2119].

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

## Follow Activity

The server receiving a Follow activity in a Repository's inbox SHOULD add the
sender actor to the Repository's followers collection.

# Acknowledgements

