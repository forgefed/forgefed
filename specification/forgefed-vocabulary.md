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
ActivityPub context and the ForgeFed contexts in their object definitions, or
other contexts that would result with the ActivityPub and ForgeFed terms being
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

## Actor Types

### Repository

**URI:** `https://forgefed.peers.community/ns#Repository`

**Notes:** Represents a single repository.

**Example:**

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

## Object Types

### Commit

**URI:** `https://forgefed.peers.community/ns#Commit`

**Notes:** Represents a single Commit in a Repository.

**Example:**

    {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://forgefed.peers.community/ns"
        ],
        "type": "Commit",
        "id": "https://localhost/alice/repo2/commit/2c7323781aec1f7",
        "author": "Alice"
        "message": "Fix #89"
    }

### Ticket

**URI:** `https://forgefed.peers.community/ns#Ticket`

**Notes:** Represents a single ticket (aka "issue") for a Repository. Tickets
are used to track ideas, enhancements, tasks, or bugs.

**Example:**

    {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://forgefed.peers.community/ns"
        ],
        "type": "Ticket",
        "id": "https://localhost/alice/repo2/issues/42",
        "attributedTo": "",
        "author": "",
        "title": "Nothing works!",
        "content": "Please fix. Everything is broken!",
        "context": ""
    }

# Properties


