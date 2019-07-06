---
title: ForgeFed Vocabulary
---

**Editors:**

- deesix
- fr33domlover
- zPlus
- ... add other editors

**Repository:**

- [NotABug](https://notabug.org/peers/forgefed)

**Copyright:**

2019 ...

# Abstract

This document describes the ForgeFed vocabulary. It's intended to be an extension
of the [ActivityPub Vocabulary](https://www.w3.org/TR/activitystreams-vocabulary/)
and provides additional vocabulary for federation of project management and
version control system hosting and collaboration platforms.

# Introduction

The ForgeFed Vocabulary describes a set of types and properties to be used by
platforms that support the ForgeFed protocol. This specification describes only
the new vocabulary called ForgeFed. The ForgeFed behavior specification
describes how to use this vocabulary, along with standard ActivityPub
vocabulary, to support the ForgeFed protocol.

# Types

The base URI of all ForgeFed terms is `https://forgefed.peers.community/ns#`.
The ForgeFed vocabulary has a JSON-LD context whose URI is
`https://forgefed.peers.community/ns`. Implementers MUST either include the
ActivityPub and ForgeFed contexts in their object definitions, or other
contexts that would result with the ActivityPub and ForgeFed terms being
assigned they correct full URIs. Implementers MAY include additional contexts
and terms as appropriate.

A typical `@context` of a ForgeFed object may look like this:

```json
"@context": [
    "https://www.w3.org/ns/activitystreams",
    "https://forgefed.peers.community/ns"
]
```

## Activity Types

### Push

**URI:** `https://forgefed.peers.community/ns#Push`

**Notes:** Indicates that new content has been pushed to the repository. The
Activity's object MUST contain a list of Commits.
A Repository actor can use this Activity to notify followers of new changes.

**Example:**

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "summary": "Alice pushed 2 new commits to Repo2."
    "type": "Push",
    "actor": "https://localhost/alice/repo2",
    "object": [
        {
            "type": "Commit",
        },
        {
            "type": "Commit",
        }
    ]
}
```

## Actor Types

### Repository

**URI:** `https://forgefed.peers.community/ns#Repository`

**Notes:** Represents a version control system repository.

**Example:**

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "id": "https://localhost/alice/forgefed",
    "type": "Repository",
    "name": "ForgeFed",
    "summary": "ForgeFed development",
    "inbox": "",
    "outbox": "",
    "followers": "",
    "following": ""
}
```

## Object Types

### Commit

**URI:** `https://forgefed.peers.community/ns#Commit`

**Notes:** Represents a named set of changes to a repository. This is called
"commit" in Git, Mercurial and Monotone; "patch" in Darcs; sometimes called
"change set".

**Example:**

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "type": "Commit",
    "id": "https://example.dev/alice/myrepo/commit/2c7323781aec1f7",
    "attributedTo": "https://example.dev/alice",
    "name": "Add an installation script, fixes issue #89"
}
```

### Ticket

**URI:** `https://forgefed.peers.community/ns#Ticket`

**Notes:** Represents an item that requires work or attention. Tickets exist in
the context of a project (which may or may not be a version-control
repository), and are used to track ideas, proposals, tasks, bugs and more.

**Example:**

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "type": "Ticket",
    "id": "https://example.dev/alice/myrepo/issues/42",
    "context": "https://example.dev/alice/myrepo",
    "attributedTo": "https://dev.community/bob",
    "summary": "Nothing works!",
    "content": "<p>Please fix. <i>Everything</i> is broken!</p>",
    "mediaType": "text/html",
    "source": {
        "content": "Please fix. *Everything* is broken!",
        "mediaType": "text/markdown; variant=CommonMark"
    },
    "assignedTo": "https://example.dev/alice",
    "isResolved": false
}
```

# Properties

## assignedTo

**URI:** `https://forgefed.peers.community/ns#assignedTo`

**Notes:** Identifies the person assigned to work on this ticket.

**Domain:** `Ticket`

**Range:** `Person`

**Functional:** Yes

**Inverse of:** (None)

**Example:**

## isResolved

**URI:** `https://forgefed.peers.community/ns#isResolved`

**Notes:** Specifies whether the ticket is closed, i.e. the work on it is done
and it doesn't need to attract attention anymore.

**Domain:** `Ticket`

**Range:** `xsd:boolean`

**Functional:** Yes

**Inverse of:** (None)

**Example:**

## dependsOn

**URI:** `https://forgefed.peers.community/ns#dependsOn`

**Notes:** Identifies one or more tickets on which this ticket depends, i.e. it
can't be resolved without those tickets being resolved too.

**Domain:** `Ticket`

**Range:** `Ticket`

**Functional:** No

**Inverse of:** [dependedBy](#dependedby)

**Example:**

## dependedBy

**URI:** `https://forgefed.peers.community/ns#dependedBy`

**Notes:** Identifies one or more tickets which depends on this ticket, i.e.
they can't be resolved without this tickets being resolved too.

**Domain:** `Ticket`

**Range:** `Ticket`

**Functional:** No

**Inverse of:** [dependsOn](#dependson)

**Example:**
