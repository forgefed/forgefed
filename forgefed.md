---
title: ForgeFed protocol specification
author: ForgeFed Working Group
date: 2020-2022
...


# Satus of this document

This document is still a work in progress. The ForgeFed specification
is still not finalized.


# Introduction

ForgeFed is an upcoming federation protocol for enabling interoperability between
version control services. It’s built as an extension to the ActivityPub protocol,
allowing users of any ForgeFed-compliant service to interact with the repositories
hosted on other instances.

The goal of the project is to support all of the major activities connected with
project management, including bug reports, merge requests, and notifications across
instances.

{ Add more details here }

Because ForgeFed is built upon ActivityPub, the reader should be familiar with the
[ActivityPub specification](https://www.w3.org/TR/activitypub/) before attempting to
read this document (in particular section [*7. Server to Server Interactions*](https://www.w3.org/TR/activitypub/#server-to-server-interactions)).


# Tickets

## Open

A new [Ticket] is opened by sending a [Create] activity to a [TicketTracker] actor.

Example:
```json
{
    "@context" : [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "id": "https://example.org/activities/create/1",
    "type": "Create",
    "actor": "https://example.org/username",
    "object": {
        "type": "Ticket",
        "id": "https://example.org/username/repository/issues/1",
        "context": "https://example.org/username/repository/issues",
        "attributedTo": "https://example.org/username",
        "summary": "Ticket title",
        "content": "Ticket content"
    }
}
```

In response to this request, the [TicketTracker] will either [Accept] or [Reject]
the Create activity. The response MUST contain the `result` property with the `id`
of the newly created Ticket object. The response MUST be sent to all the
followers of the TicketTracker.

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

Tickets can be commented on by users, by creating a [Note] and notifying the
[TicketTracker] about it. Upon receiving the new Note, the TicketTracker MUST
notify its followers by forwarding the activity.

Example:
```json
{
    "@context" : [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "id": "https://example.org/activities/abcdef0123456789",
    "type": "Create",
    "actor": "https://example.org/alice",
    "to": "https://example.org/bob/repository/issues",
    "object": "https://example.org/alice/comments/1",
}
```

## Close

A [Ticket] is closed by sending a [Resolve] activity to a [TicketTracker] actor.
The TicketTracker is responsible for checking that the actor which resolved the
Ticket has the rights to do so.

Example:
```json
{
    "@context" : [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "id": "https://example.org/activities/abcdef0123456789",
    "type": "Resolve",
    "actor": "https://example.org/alice",
    "object": "https://example.org/username/repository/issues/1",
}
```


# Merge requests

## Open

## Comment

## Close


# Vocabulary

ForgeFed extends the core set of ActivityPub objects with new types and properties.
This section describes the ForgeFed vocabulary which is intended to be used in the
context of project management.

The base URI of all ForgeFed terms is `https://forgefed.peers.community/ns#`.
The ForgeFed vocabulary has a JSON-LD context whose URI is
`https://forgefed.peers.community/ns`. Implementations MUST either include the
ActivityPub and ForgeFed contexts in their object definitions, or other
contexts that would result with the ActivityPub and ForgeFed terms being
assigned they correct full URIs. Implementations MAY include additional contexts
and terms as appropriate. A typical `@context` of a ForgeFed object may look like
this:

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

### Resolve

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
    "sshKey": [ ],
    "roles": [ ]
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
    "summary": "",
    "roles": [ ]
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
    "refs": "https://example.org/username/repository.git/refs"
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

### Commit

Represents a commit of a repository.

Example:

```json
{
    "@context": [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "type": "Commit",
    "id": "https://example.org/username/repository/commit/abcdef0123456789",
    "context": "https://example.org/username/repository",
    "attributedTo": "",
    "committedBy": "",
    "hash": "abcdef0123456789",
    "summary": "",
    "description": "",
    "created": "",
    "committed": "2022-01-01 00:00"
}
```

### Roles

Example:

```json
{
    "@context": [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "type": "Role",
    "id": "https://example.org/roles/admin/1",
    "name": "admin",
    "context": "https://example.org/project1"
}
```

### Cryptographic keys

Example:

```json
{
    "@context": ,
    "type": "CryptographicKey",
    "id": ,
    "owner": ,
    "publicKeyPem": ,
    "created": ,
    "expires": ,
    "revoked": ,
    "privateKeyPem": ,
}
```

### SSH keys

Example:

```json
{
    "@context": ,
    "type": "SshKey",
    "id": ,
    "owner": ,
    "sshKeyType": ,
    "content": ,
    "created": ,
    "expires": ,
    "revoked": ,
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
    "mediaType": "text/plain",
    "source": {
        "content": "Ticket content",
        "mediaType": "text/markdown; variant=CommonMark"
    },
    "assignedTo": [ ],
    "isResolved": true,
    "depends": [ "https://example.org/username/repository/issues/2" ],
    "tags": [ "tag 1", "tag 2" ],
    "milestones": [ "milestone 1" ]
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
    "mediaType": "text/plain",
    "content": "Comment text",
    "source": {
        "mediaType": "text/markdown; variant=Commonmark",
        "content": "Comment text"
    },
    "published": "2022-01-01 00:00"
}
```

### MergeRequest

Represents a request to merge a [Branch] into another.

Example:

```json
{
    "@context": [ "https://www.w3.org/ns/activitystreams", "https://w3id.org/security/v1", "https://forgefed.peers.community/ns" ],
    "type": "MergeRequest",
    "id": "https://example.org/alice/mr/1",
    "attributedTo": "https://example.org/alice",
    "summary": "Merge request title",
    "content": "Merge request description",
    "downstream": {
        "repository": "",
        "branch": ""
    },
    "upstream": {
        "repository": "",
        "branch": ""
    },
    "commit_start": "",
    "commit_stop": ""
}
```

### Merge requests comments

Represents a comment submitted to a [MergeRequest].
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
    "mediaType": "text/plain",
    "content": "Comment text",
    "source": {
        "mediaType": "text/markdown; variant=Commonmark",
        "content": "Comment text"
    },
    "published": "2022-01-01 00:00"
}
```


## Properties




[Accept]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-accept
[Application]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-application
[Branch]: #branch
[Create]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-create
[Group]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-group
[MergeRequest]: #mergerequest
[Note]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-note
[Organization]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-organization
[Person]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-person
[Reject]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-reject
[Resolve]: #resolve
[Ticket]: #ticket
[type]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-type
