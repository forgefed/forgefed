---
title: ForgeFed
---

**Editors:**

- fr33domlover
- zPlus
- ... add other editors

**Repository:**

- [NotABug](https://notabug.org/peers/forgefed)

**Copyright:**

2019 ...

# Abstract

This document describes the ForgeFed protocol. ForgeFed is an extension of the
[ActivityPub](https://www.w3.org/TR/activitypub/) protocol for delivering
notifications and content for federation of version control systems.
The purpose of this specification is to describe a protocol that can be integrated
into source code management for enabling collaboration across different
platforms.

# Status of This Document

# Overview

ForgeFed is an extension of [ActivityPub](https://www.w3.org/TR/activitypub/)
and follows the same "actors" model, with a client-to-server protocol and a
server-to-server protocol.

# Conformance

The key words MAY, MUST, MUST NOT, SHOULD, and SHOULD NOT are to be interpreted
as described in [RFC2119].

# Objects

Objects are the core concept around which both ActivityPub and ForgeFed are built.
Examples of Objects are Note, Ticket, or Image.
Objects are wrapped in Activities, a subtype of Object that describes some form
of action that may happen, is currently happening, or has already happened.
Examples of Activities are Create, Delete, or Follow.

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
The client MUST send a Follow activity the a Person's outbox. The server
in turn delivers the message to the destination inbox.

## Push Activity

The Push activity is used to notify followers when somebody has pushed changes
to a Repository.
The client MUST send a Push activity the a Repository's outbox. The server
in turn delivers the message to the Repository followers.

# Server to Server Interactions

## Follow Activity

The server receiving a Follow activity in a Repository's inbox SHOULD add the
sender actor to the Repository's followers collection.

# Acknowledgements

