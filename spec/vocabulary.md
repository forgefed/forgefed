---
title: ForgeFed Vocabulary
---

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

### Push {#act-push}

**URI:** `https://forgefed.peers.community/ns#Push`

**Notes:** Indicates that new content has been pushed to the
[Repository](#type-repository).

**Example:**

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "id": "https://example.dev/aviva/outbox/reBGo",
    "type": "Push",
    "actor": "https://example.dev/aviva",
    "to": [
        "https://example.dev/aviva/followers",
        "https://example.dev/aviva/myproject",
        "https://example.dev/aviva/myproject/team",
        "https://example.dev/aviva/myproject/followers"
    ],
    "summary": "<p>Aviva pushed a commit to myproject</p>",
    "object": {
        "type": "OrderedCollection",
        "totalItems": 1,
        "items": [
            {
                "id": "https://example.dev/aviva/myproject/commits/d96596230322716bd6f87a232a648ca9822a1c20",
                "type": "Commit",
                "attributedTo": "https://example.dev/aviva",
                "context": "https://example.dev/aviva/myproject",
                "hash": "d96596230322716bd6f87a232a648ca9822a1c20",
                "created": "2019-11-03T13:43:59Z",
                "name": "Provide hints in sign-up form fields",
            }
        ]
    },
    "target": "https://example.dev/aviva/myproject/branches/master",
    "context": "https://example.dev/aviva/myproject"
}
```

## Actor Types

### Repository {#type-repository}

**URI:** `https://forgefed.peers.community/ns#Repository`

**Notes:** Represents a version control system repository.

**Example:**

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v1",
        "https://forgefed.peers.community/ns"
    ],
    "id": "https://dev.example/aviva/treesim",
    "type": "Repository",
    "publicKey": {
        "id": "https://dev.example/aviva/treesim#main-key",
        "owner": "https://dev.example/aviva/treesim",
        "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhki....."
    },
    "inbox": "https://dev.example/aviva/treesim/inbox",
    "outbox": "https://dev.example/aviva/treesim/outbox",
    "followers": "https://dev.example/aviva/treesim/followers",
    "team": "https://dev.example/aviva/treesim/team",
    "name": "Tree Growth 3D Simulation",
    "summary": "<p>Tree growth 3D simulator for my nature exploration game</p>"
}
```

## Object Types

### Branch {#type-branch}

**URI:** `https://forgefed.peers.community/ns#Branch`

**Notes:** Represents a named variable reference to a version of the
[Repository](#type-repository), typically used for committing changes in
parallel to other development, and usually eventually merging the changes into
the main history line.

**Example:**

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "id": "https://example.dev/luke/myrepo/branches/master",
    "type": "Branch",
    "name": "master",
    "context": "https://example.dev/luke/myrepo",
    "ref": "refs/heads/master"
}
```

### Commit {#type-commit}

**URI:** `https://forgefed.peers.community/ns#Commit`

**Notes:** Represents a named set of changes in the history of a
[Repository](#type-repository).  This is called "commit" in Git, Mercurial and
Monotone; "patch" in Darcs; sometimes called "change set". Note that `Commit`
is a set of changes that already exists in a repo's history, while a
[Patch](#type-patch) is a separate proposed change set, that *could* be applied
and pushed to a repo, resulting with a `Commit`.

**Example:**

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "id": "https://example.dev/alice/myrepo/commits/109ec9a09c7df7fec775d2ba0b9d466e5643ec8c",
    "type": "Commit",
    "context": "https://example.dev/alice/myrepo",
    "attributedTo": "https://example.dev/bob",
    "committedBy": "https://example.dev/alice",
    "hash": "109ec9a09c7df7fec775d2ba0b9d466e5643ec8c",
    "name": "Add an installation script, fixes issue #89",
    "description": {
        "mediaType": "text/plain",
        "content": "It's about time people can install on their computers!"
    },
    "created": "2019-07-11T12:34:56Z",
    "committed": "2019-07-26T23:45:01Z"
}
```

### TicketDependency {#type-ticketdependency}

**URI:** `https://forgefed.peers.community/ns#TicketDependency`

**Notes:** Represents a relationship between 2 [Ticket](#type-ticket)s, in
which the resolution of one ticket requires the other ticket to be resolved
too. It MUST specify the [subject], [object] and [relationship] properties, and
the `relationship` property MUST be [dependsOn](#prop-dependson).

**Extends:** [Relationship]

**Example:**

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "type": ["Relationship", "TicketDependency"],
    "id": "https://example.dev/ticket-deps/2342593",
    "attributedTo": "https://example.dev/alice",
    "summary": "Alice's ticket depends on Bob's ticket",
    "published": "2019-07-11T12:34:56Z",
    "subject": "https://example.dev/alice/myproj/issues/42",
    "relationship": "dependsOn",
    "object": "https://dev.community/bob/coolproj/issues/85"
}
```

### Ticket {#type-ticket}

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

## assignedTo {#prop-assignedto}

**URI:** `https://forgefed.peers.community/ns#assignedTo`

**Notes:** Identifies the [Person] assigned to work on this
[Ticket](#type-ticket).

**Domain:** [Ticket](#type-ticket)

**Range:** [Person]

**Functional:** Yes

**Inverse of:** (None)

**Example:**

## isResolved {#prop-isresolved}

**URI:** `https://forgefed.peers.community/ns#isResolved`

**Notes:** Specifies whether the [Ticket](#type-ticket) is closed, i.e. the
work on it is done and it doesn't need to attract attention anymore.

**Domain:** [Ticket](#type-ticket)

**Range:** `xsd:boolean`

**Functional:** Yes

**Inverse of:** (None)

**Example:**

## dependsOn {#prop-dependson}

**URI:** `https://forgefed.peers.community/ns#dependsOn`

**Notes:** Identifies one or more tickets on which this [Ticket](#type-ticket)
depends, i.e. it can't be resolved without those tickets being resolved too.

**Domain:** [Ticket](#type-ticket)

**Range:** [Ticket](#type-ticket)

**Functional:** No

**Inverse of:** [dependedBy](#prop-dependedby)

**Example:**

## dependedBy {#prop-dependedby}

**URI:** `https://forgefed.peers.community/ns#dependedBy`

**Notes:** Identifies one or more tickets which depend on this
[Ticket](#type-ticket), i.e. they can't be resolved without this tickets being
resolved too.

**Domain:** [Ticket](#type-ticket)

**Range:** [Ticket](#type-ticket)

**Functional:** No

**Inverse of:** [dependsOn](#prop-dependson)

**Example:**

## dependencies {#prop-dependencies}

**URI:** `https://forgefed.peers.community/ns#dependencies`

**Notes:** Identifies a [Collection] of
[TicketDependency](#type-ticketdependency) which specify tickets that this
[Ticket](#type-ticket) depends on, i.e. this ticket is the [subject] of the
[dependsOn](#prop-dependson) relationship.

**Domain:** [Ticket](#type-ticket)

**Range:** [Collection] of items of type
[TicketDependency](#type-ticketdependency)

**Functional:** Yes

**Inverse of:** (None)

**Example:**

## dependants {#prop-dependants}

**URI:** `https://forgefed.peers.community/ns#dependants`

**Notes:** Identifies a [Collection] of
[TicketDependency](#type-ticketdependency) which specify tickets that depends
on this [Ticket](#type-ticket), i.e. this ticket is the [object] of the
[dependsOn](#prop-dependson) relationship. Often called "reverse dependencies".

**Domain:** [Ticket](#type-ticket)

**Range:** [Collection] of items of type
[TicketDependency](#type-ticketdependency)

**Functional:** Yes

**Inverse of:** (None)

**Example:**

## repository (DEPRECATED) {#prop-repository}

**URI:** `https://forgefed.peers.community/ns#repository`

**Notes:** Identifies the repository to which a commit belongs. DEPRECATED: Use
the standard ActivityPub `context` property instead.

**Domain:** `Commit`

**Range:** `Repository`

**Functional:** Yes

**Inverse of:** (None)

**Example:**

## description {#prop-description}

**URI:** `https://forgefed.peers.community/ns#description`

**Notes:** Specifies the description text of a [Commit](#type-commit), which is an optional
possibly multi-line text provided in addition to the one-line commit title. The
range of the `description` property works the same way the range of the
ActivityPub [source] property works.

**Domain:** [Commit](#type-commit)

**Range:** [Object] that specifies a [content] and a [mediaType]. The
`mediaType` SHOULD be `"text/plain"`.

**Functional:** Yes

**Inverse of:** (None)

**Example:**

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "id": "https://example.dev/alice/myrepo/commits/109ec9a09c7df7fec775d2ba0b9d466e5643ec8c",
    "type": "Commit",
    "context": "https://example.dev/alice/myrepo",
    "attributedTo": "https://example.dev/bob",
    "hash": "109ec9a09c7df7fec775d2ba0b9d466e5643ec8c",
    "created": "2019-07-11T12:34:56Z",
    "name": "Add an installation script, fixes issue #89",

    "description": {
        "mediaType": "text/plain",
        "content": "It's about time people can install on their computers!"
    },
}
```

## committedBy {#prop-committedby}

**URI:** `https://forgefed.peers.community/ns#committedBy`

**Notes:** Identifies the actor (usually a person, but could be something else,
e.g. a bot) that added a set of changes to the version-control
[Repository](#type-repository).  Sometimes the author of the changes and the
committer of those changes aren't the same actor, in which case the
`committedBy` property can be used to specify who added the changes to the
repository. For example, when applying a patch to a repository, e.g. a Git
repository, the author would be the person who made the patch, and the
committer would be the person who applied the patch to their copy of the
repository.

**Domain:** [Commit](#type-commit)

**Range:** [Object]

**Functional:** Yes

**Inverse of:** (None)

**Example:**

## hash {#prop-hash}

**URI:** `https://forgefed.peers.community/ns#hash`

**Notes:** Specifies the hash associated with a [Commit](#type-commit), which
is a unique identifier of the commit within the [Repository](#type-repository),
usually generated as a cryptographic hash function of some (or all) of the
commit's data or metadata.  For example, in Git it would be the SHA1 hash of
the commit; in Darcs it would be the SHA1 hash of the patch info.

**Domain:** [Commit](#type-commit)

**Range:** `xsd:string` of hexadecimal digit ASCII characters

**Functional:** Yes

**Inverse of:** (None)

**Example:**

## committed {#prop-committed}

**URI:** `https://forgefed.peers.community/ns#committed`

**Notes:** Specifies the time that a set of changes was committed into the
[Repository](#type-repository) and became a [Commit](#type-commit) in it. This
can be different from the time the set of changes was produced, e.g. if one
person creates a patch and sends to another, and the other person then applies
the patch to their copy of the repository. We call the former event "created"
and the latter event "committed", and this latter event is specified by the
`committed` property.

**Domain:** [Commit](#type-commit)

**Range:** `xsd:dateTime`

**Functional:** Yes

**Inverse of:** (None)

**Example:**

## filesAdded {#prop-filesadded}

**URI:** `https://forgefed.peers.community/ns#filesAdded`

**Notes:** Specifies a filename, as a relative path, relative to the top of the
tree of files in the [Repository](#type-repository), of a file that got added
in this [Commit](#type-commit), and didn't exist in the previous version of the
tree.

**Domain:** [Commit](#type-commit)

**Range:** `xsd:string`

**Functional:** No

**Inverse of:** (None)

**Example:**

## filesModified {#prop-filesmodified}

**URI:** `https://forgefed.peers.community/ns#filesModified`

**Notes:** Specifies a filename, as a relative path, relative to the top of the
tree of files in the [Repository](#type-repository), of a file that existed in
the previous version of the tree, and its contents got modified in this
[Commit](#type-commit).

**Domain:** [Commit](#type-commit)

**Range:** `xsd:string`

**Functional:** No

**Inverse of:** (None)

**Example:**

## filesRemoved {#prop-filesremoved}

**URI:** `https://forgefed.peers.community/ns#filesRemoved`

**Notes:** Specifies a filename, as a relative path, relative to the top of the
tree of files in the [Repository](#type-repository), of a file that existed in
the previous version of the tree, and got removed from the tree in this
[Commit](#type-commit).

**Domain:** [Commit](#type-commit)

**Range:** `xsd:string`

**Functional:** No

**Inverse of:** (None)

**Example:**

## ref {#prop-ref}

**URI:** `https://forgefed.peers.community/ns#ref`

**Notes:** Specifies an identifier for a [Branch](#type-branch), that is used
in the [Repository](#type-repository) to uniquely refer to it. For example, in
Git, "refs/heads/master" would be the `ref` of the master branch.

**Domain:** [Branch](#type-branch)

**Range:** `xsd:string`

**Functional:** Yes

**Inverse of:** (None)

**Example:**

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "id": "https://example.dev/luke/myrepo/branches/master",
    "type": "Branch",
    "name": "master",
    "context": "https://example.dev/luke/myrepo",

    "ref": "refs/heads/master"
}
```
[Collection]:   https://www.w3.org/TR/activitystreams-vocabulary/#dfn-collection
[Object]:       https://www.w3.org/TR/activitystreams-vocabulary/#dfn-object
[Person]:       https://www.w3.org/TR/activitystreams-vocabulary/#dfn-person

[content]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-content
[mediaType]:    https://www.w3.org/TR/activitystreams-vocabulary/#dfn-mediatype
[relationship]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-relationship
[source]:       https://www.w3.org/TR/activitypub/#source-property
[subject]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-subject