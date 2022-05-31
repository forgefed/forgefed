---
title: ForgeFed protocol specification
author: ForgeFed Working Group
date: 2020-2022
...


# Status of this document

This document is still a work in progress. The ForgeFed specification
is still not finalized.


# Introduction

ForgeFed is a protocol for federation of project-management activities through ActivityPub.
The objective of the project is to establish a standard for ActivityPub federation,
capable of supporting the activities of project management such as bug reports,
patches, and notifications across ActivityPub instances. ForgeFed compliant servers
will allow projects to become part of the broader ActivityPub federation.

The ForgeFed working group was established for reaching consensus about the protocol
among the interested parties. This document is the result of the workgroup discussion.

This revision of the specification establishes the basic mechanisms for ActivityPub
federation, while deferring more advanced features for future revisions or extensions.
Because ForgeFed is built upon ActivityPub, the reader is expected to be already familiar
with the [ActivityPub specification](https://www.w3.org/TR/activitypub/) before reading
this document, and in particular with section [*7. Server to Server Interactions*](https://www.w3.org/TR/activitypub/#server-to-server-interactions).


# Tickets

The workgroup discussion has highlighted two contrasting views for managing tickets
in the federation. One view is that tickets should be owned by the actor that created
the ticket; the other view is that tickets should be owned by the [TicketTracker]
receiving the ticket. This revision of the specification only takes into consideration
the latter case, thus recognizing [TicketTracker] as the entity in complete control of
the ticket lifecycle.

## Open

A new [Ticket] is opened by sending a [Create] activity to a [TicketTracker] actor.

Example:
```json
{
    "@context" : [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "id": "https://example.org/activities/create/1",
    "type": "Create",
    "actor": "https://example.org/alice",
    "object": {
        "type": "Ticket",
        "context": "https://example.org/bob/repository/issues",
        "attributedTo": "https://example.org/alice",
        "summary": "Ticket title",
        "content": "Ticket content",
    }
}
```

In response to this request, the [TicketTracker] MUST [Accept] or [Reject] the
Create activity. If the ticket is accepted, the response MUST contain the `result`
property with the `id` of the newly created Ticket object. If the ticket is submitted
with a value in the `id` property, servers MUST ignore this and generate a new one.
The response MUST be sent to all the followers of the TicketTracker.

Example:
```json
{
    "@context" : [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "id": "https://example.org/activities/abcdef0123456789",
    "type": "Accept",
    "actor": "https://example.org/username/repository/issues",
    "object": "https://example.org/activities/create/1",
    "result": "https://example.org/username/repository/issues/1"
}
```

## Comment

Tickets can be commented on by creating a new [Note]. The [Create] activity MUST
be delivered to the [TicketTracker] responsible for the ticket. The Note MUST have
the `context` property, with the ticket `id` as value.
Upon receiving the new Note, the TicketTracker MUST notify its followers by forwarding
the activity.

Example:
```json
{
    "@context" : [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "id": "https://example.org/activities/abcdef0123456789",
    "type": "Create",
    "actor": "https://example.org/alice",
    "to": "https://example.org/bob/repository/issues",
    "object": {
        "id": "https://example.org/alice/comments/1",
        "type": "Note",
        "context": "https://example.org/bob/repository/issues/1",
        "attributedTo": "https://example.org/alice",
        "content": "Comment text",
        "published": "2022-01-01 00:00"
    }
}
```

## Close

A [Ticket] is closed by sending a [Resolve] activity to the [TicketTracker] managing
the Ticket. The TicketTracker is responsible for checking that the actor which
resolved the Ticket has the rights to do so. If the actor has permission to modify
the ticket, the TicketTracker MUST update the `isResolved` property of the ticket
accordingly, and finally notify its followers by forwarding the activity.

Example:
```json
{
    "@context" : [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "id": "https://example.org/activities/abcdef0123456789",
    "type": "Resolve",
    "actor": "https://example.org/alice",
    "object": "https://example.org/bob/repository/issues/1",
}
```


# Patches

There are two popular ways for submitting changes when using distributed version
control systems. "Merge requests", which have been popularized by web-based
hosting services, consist in comparing the branches of two repositories. "Patches"
instead consist in preparing patch files with all the changes to be submitted.
A considerable side effect of merge-requests is that the receiving server has to
download the remote repositories in order to fetch the changes and create a diff
file. This behaviour is undesirable because of the excessive burden on the receiving
server, and is not included in this revision of the specification. Patch files
do not carry the same side effect since they already include the list of changes.

## Submit

[Patch] are submitted by sending a [Create] activity to a [Repository] actor. The
[Repository] MUST forward the activity to all its followers.

Example:

```json
{
    "@context" : [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "id": "https://example.org/activities/create/1",
    "type": "Create",
    "actor": "https://example.org/alice",
    "to": "https://example.org/bob/repository.git",
    "object": {
        "id": "https://example.org/alice/patch/1",
        "type": "Patch",
        "attributedTo": "https://example.org/alice",
        "summary": "Patch title",
        "content": "Content of the patch",
        "downstream": {
            "repository": "",
            "branch": ""
        },
        "upstream": {
            "repository": "",
            "branch": ""
        },
    }
}
```

## Comment

Patches can be commented on by users, by creating a [Note].

Patches can be commented on by creating a new [Note]. The [Create] activity MUST
be delivered to the target [Repository]. The Note MUST have
the `context` property, with the patch `id` as value.
Upon receiving the new Note, the Repository MUST notify its followers by forwarding
the activity.

Example:

```json
{
    "@context" : [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "id": "https://example.org/activities/abcdef0123456789",
    "type": "Create",
    "actor": "https://example.org/alice",
    "to": "https://example.org/bob/repository.git",
    "object": {
        "id": "https://example.org/alice/comments/1",
        "type": "Note",
        "context": "https://example.org/bob/repository.git",
        "attributedTo": "https://example.org/alice",
        "content": "Comment text",
        "published": "2022-01-01 00:00"
    }
}
```

## Apply

Once a [Patch] has been applied, the [Repository] SHOULD notify its followers by
sending an [Apply] activity.

Example:
```json
{
    "@context" : [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "id": "https://example.org/activities/abcdef0123456789",
    "type": "Apply",
    "actor": "https://example.org/bob",
    "object": "https://example.org/alice/patch/1"
}
```


# Vocabulary

ForgeFed extends the core set of ActivityPub objects with new types and properties.
This section describes the ForgeFed vocabulary.

The base URI of all ForgeFed terms is `https://forgefed.peers.community/ns#`.
The ForgeFed vocabulary has a JSON-LD context whose URI is
`https://forgefed.peers.community/ns`. Implementations MUST include the ActivityPub
and ForgeFed contexts in their object definitions, or other contexts that would result
in the ActivityPub and ForgeFed terms being assigned they correct URIs. Implementations
MAY include additional contexts and terms as appropriate. A typical `@context` of a
ForgeFed object looks like this:

```json
{
    "@context" : [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v1",
        "https://forgefed.peers.community/ns"
    ]
}
```

## Activity types

### Apply

Indicates that a [Patch] has been applied to a repository.

Example:

```json
{
    "@context": [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "type": "Apply",
    "id": "https://example.org/activities/1",
    "actor": "https://example.org/bob",
    "object": "https://example.org/alice/patch/1"
}
```

### Resolve

Indicates that an actor has resolved a ticket.

Example:

```json
{
    "@context" : [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "id": "https://example.org/activities/abcdef0123456789",
    "type": "Resolve",
    "actor": "https://example.org/alice",
    "object": "https://example.org/bob/repository/issues/1",
}
```

## Actor types

### Users

ForgeFed does not introduce new actor types for users, relying instead on
ActivityPub. Common types of users are [Person] for real people, and [Application]
for bots.

Example:

```json
{
    "@context": [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "type": "Person",
    "id": "https://example.org/username",
    "inbox": "https://example.org/username/inbox",
    "outbox": "https://example.org/username/outbox",
    "followers": "https://example.org/username/followers",
    "following": "https://example.org/username/following",
    "publicKey": "https://example.org/username/key.pub",
    "name": "User Name",
    "preferredUsername": "username",
}
```

### Groups

ForgeFed does not introduce new actor types for groups, relying instead on
ActivityPub. Common types of groups are [Group] and [Organization].

Example:

```json
{
    "@context": [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "type": "Group",
    "id": "https://example.org/groupname",
    "name": "Group Name",
    "preferredUsername": "groupname",
}
```

### Repository

Represents a version control system repository.

Example:

```json
{
    "@context": [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "type": "Repository",
    "id": "https://example.org/username/repository.git",
    "inbox": "https://example.org/username/repository.git/inbox",
    "outbox": "https://example.org/username/repository.git/outbox",
    "followers": "https://example.org/username/repository.git/followers",
    "following": "https://example.org/username/repository.git/following",
    "publicKey": "https://example.org/username/repository.git/key.pub",
    "name": "Repository full name",
    "preferredUsername": "repository",
    "project": "https://example.org/project",
}
```

### TicketTracker

Represents a ticket tracker, also known as issue tracker or bug tracker.
Tracks the status of [Ticket]s.

Example:

```json
{
    "@context": [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "type": "TicketTracker",
    "id": "https://example.org/username/repository/issues",
    "inbox": "https://example.org/username/repository/issues/inbox",
    "outbox": "https://example.org/username/repository/issues/outbox",
    "followers": "https://example.org/username/repository/issues/followers",
    "following": "https://example.org/username/repository/issues/following",
    "publicKey": "https://example.org/username/repository/issues/key.pub",
    "name": "Tracker full name",
    "preferredUsername": "tracker_name",
    "project": "https://example.org/project"
}
```

## Object types

### Project

Represents the set of repositories and ticket trackers that logically belong to
the same project.

Example:

```json
{
    "@context": [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "type": "Project",
    "id": "https://example.org/project",
    "name": "Project full name",
    "repository": [ ],
    "tickettracker": [ ]
}
```

### Branch

Represents a branch of a repository.

Example:

```json
{
    "@context": [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "type": "Branch",
    "id": "https://example.org/tree/branch_name",
    "name": "branch_name",
    "context": "https://example.org/username/repository"
}
```

### Ticket

Represents a ticket in a ticket tracker.

Example:

```json
{
    "@context": [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "type": "Ticket",
    "id": "https://example.org/username/repository/issues/1",
    "context": "https://example.org/username/repository/issues",
    "attributedTo": "https://example.org/username",
    "summary": "Ticket title",
    "content": "Ticket content",
    "isResolved": true,
}
```

### Ticket comments

Represents a comment submitted to a [Ticket].
ForgeFed does not introduce a new type for comments, relying instead on the
ActivityPub's [Note] type. ForgeFed does introduce however new properties for
this type.

Example:

```json
{
    "@context": [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "id": "https://example.org/alice/comments/1",
    "type": "Note",
    "context": "https://example.org/bob/repository/issues/1",
    "attributedTo": "https://example.org/alice",
    "inReplyTo": null,
    "content": "Comment text",
    "published": "2022-01-01 00:00"
}
```

### Patch

Represents a patch file.

Example:

```json
{
    "@context": [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "type": "Patch",
    "id": "https://example.org/alice/patch/1",
    "attributedTo": "https://example.org/alice",
    "summary": "Patch title",
    "content": "Content of the patch",
    "downstream": {
        "repository": "",
        "branch": ""
    },
    "upstream": {
        "repository": "",
        "branch": ""
    },
}
```

### Patch comments

Represents a comment submitted to a [Patch].
ForgeFed does not introduce a new type for comments, relying instead on the
ActivityPub's [Note] type. ForgeFed does introduce however new properties for
this type.

Example:

```json
{
    "@context": [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "id": "https://example.org/alice/comments/1",
    "type": "Note",
    "context": "https://example.org/alice/mr/1",
    "attributedTo": "https://example.org/bob",
    "inReplyTo": null,
    "content": "Comment text",
    "published": "2022-01-01 00:00"
}
```


## Properties

TODO add list of properties here



[Accept]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-accept
[Application]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-application
[Branch]: #branch
[Create]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-create
[Group]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-group
[MergeRequest]: #mergerequest
[Note]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-note
[Organization]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-organization
[Patch]: #patch
[Person]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-person
[Reject]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-reject
[Resolve]: #resolve
[Ticket]: #ticket
[type]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-type
