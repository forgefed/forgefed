# ForgeFed - DRAFT

**Editors:**

- deesix
- fr33domlover
- zPlus
- ... add other editors

**Repository:**

- [NotABug](https://notabug.org/peers/forgefed)

**Copyright:**

2019 ...

## Abstract

This document describes the ForgeFed protocol. ForgeFed is an extension of the
[ActivityPub](https://www.w3.org/TR/activitypub/) protocol for delivering
notifications and content for federation of version control systems.
The purpose of this specification is to describe a protocol that can be integrated
into source code management for enabling collaboration across different
platforms.

## Table of Contents
1. [Overview](#Overview)
2. [Conformance](#Conformance)
3. [Objects](#Objects)
4. [Actors](#Actors)
5. [Client to Server Interactions](#Client to Server Interactions)
6. [Server to Server Interactions](#Server to Server Interactions)
7. [Acknowledgements](#Acknowledgements)

## Overview

ForgeFed is an extension of [ActivityPub](https://www.w3.org/TR/activitypub/)
and follows the same "actors" model, with a client-to-server protocol and a
server-to-server protocol.

## Conformance

The key words MAY, MUST, MUST NOT, SHOULD, and SHOULD NOT are to be interpreted
as described in [RFC2119].

## Objects

Objects are the core concept around which both ActivityPub and ForgeFed are built.
Examples of Objects are Note, Ticket, or Image.
Objects are wrapped in Activities, a subtype of Object that describes some form
of action that may happen, is currently happening, or has already happened.
Examples of Activities are Create, Delete, or Follow.

## Actors

A ForgeFed implementation MUST provide an Actor of type `Repository` for every
repository that should support federation.

A ForgeFed implementation SHOULD provide an Actor of type `Person` for every user
of the platform.

## Client to Server Interactions

    TODO: how are these different than AP?

## Server to Server Interactions

    TODO: how are these different than AP?

## Acknowledgements




--- PUT THESE IN THE CORRECT PLACE

### Follow Activity

The `Follow` activity is used to subscribe to the activities of a repository.

### Push Activity

The `Push` activity is used to notify followers of new code that has been
pushed to a repository.
