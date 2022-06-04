---
title: ForgeFed Modeling
---

# Abstract

This document describes the rules and guidelines for representing version
control and project management related objects as linked data, using the
ForgeFed vocabulary, ActivityStreams 2, and other related vocabularies.

# Introduction

**The ForgeFed modeling specification** is a set of rules and guidelines which
describe version control repository and project management related objects and
properties, and specify how to represent them as JSON-LD objects (and linked
data in general) using the ForgeFed vocabulary and related vocabularies and
ontologies. Using these modeling rules consistently across implementations and
instances allows to have a common language spoken across networks of software
forges, project management apps and more.

The ForgeFed vocabulary specification defines a dedicated vocabulary of
forge-related terms, and the **modeling specification** uses these terms, along
with terms that already exist in ActivityPub or elsewhere and can be reused for
forge federation.

The ForgeFed behavior specification provides instructions for using Activities,
and which Activities and properties to use, to represent forge events, and
describes the side-effects these Activities should have. The objects used as
inputs and outputs of behavior descriptions there are defined here in the
**modeling specification**.

# Commit

To represent a named set of changes committed into a repository's history, use
the ForgeFed [Commit][type-commit] type. Such a committed change set is called
e.g. a *commit* in Git, and a *patch* in Darcs.

Properties:

* [type][]: ["Commit"][type-commit]
* [context][]: The [Repository][type-repository] that this commit belongs to
* [attributedTo][]: The commit author; if their actor URI is unknown, it MAY be
  their email address as a `mailto` URI
* [created][prop-created]: A value of type [xsd:dateTime][] (i.e. an ISO 8601
  datetime value) specifying the time at which the commit was written by its
  author
* [committedBy][prop-committedby]: The entity that committed the commit's
  changes into their local copy of the repo, before the commit was pushed; if
  their actor URI is unknown, it MAY be their email address as a `mailto` URI
* [committed][prop-committed]: The time the commit was committed by its
  committer
* [hash][prop-hash]: The hash identifying the commit, e.g. the commit SHA1 hash
  in Git; the patch info SHA1 hash in Darcs
* [summary][]: The commit's one-line title as HTML-escaped plain text; if the
  commit title and description are a single commit message string, then the
  title is the 1st line of the commit message
* [description][prop-description]: A JSON object with a [mediaType][] field and
  a [content][] field, where `mediaType` SHOULD be "text/plain" and `content`
  is the commit's possibly-multi-line description; if the commit title and
  description are a single commit message string, then the description is
  everything after the 1st line of the commit message (possibly with leading
  whitespace stripped)

Example:

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
    "created": "2019-07-11T12:34:56Z",
    "committedBy": "https://example.dev/alice",
    "committed": "2019-07-26T23:45:01Z",
    "hash": "109ec9a09c7df7fec775d2ba0b9d466e5643ec8c",
    "summary": "Add an installation script, fixes issue #89",
    "description": {
        "mediaType": "text/plain",
        "content": "It's about time people can install it on their computers!"
    }
}
```

# Branch

To represent a repository branch, use the ForgeFed [Branch][type-branch] type.
It can be a real built-in version control system branch (such as a Git branch)
or a copy of the repo used as a branch (e.g. in Darcs, which doesn't implement
branches, and the way to have branches is to keep multiple versions of the
repo).

Properties:

* [type][]: ["Branch"][type-branch]
* [context][]: The [Repository][type-repository] that this branch belongs to
* [name][]: The user given name of the branch, e.g. "master"
* [ref][prop-ref]: The unique identifier of the branch within the repo, e.g.
  "refs/heads/master"
* [team][prop-team]: If the branch has its own access/authority/visibility
  settings, this can be a [Collection][] of the actors who have push/edit
  access to the branch

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "id": "https://example.dev/luke/myrepo/branches/master",
    "type": "Branch",
    "context": "https://example.dev/luke/myrepo",
    "name": "master",
    "ref": "refs/heads/master"
}
```

# Repository

To represent a version control repository, use the ForgeFed
[Repository][type-repository] type.

Properties:

* [type][]: ["Repository"][type-repository]
* [name][]: The user given name of the repository, e.g. "My cool repo"
* [cloneUri][]: The endpoint from which the content of the repository can be
  obtained via the native protocol (Git, Hg, etc.)
* [attributedTo][]: The actor(s) in charge of the repository, e.g. a person or
  an organization; if their actor URI is unknown, it MAY be
  their email address as a `mailto` URI
* [published][]: The time the repository was created on the server
* [summary][]: A one-line user provided description of the repository, as HTML,
  e.g. "`<p>A command-line tool that does cool things</p>`"
* [team][prop-team]: [Collection][] of actors who have management/push access
  to the repository, or the subset of them who is available and wants to be
  contacted/notified/responsible on repo access related activities/requests
* [forks][prop-forks]: [OrderedCollection][] of repositories that are forks of
  this repository
* [ticketsTrackedBy][prop-ticketstrackedby]: The ticket tracker that tracks
  tickets for this repository, this can be the repository itself if it manages
  its own tickets
* [sendPatchesTo][prop-sendpatchesto]: The actor that tracks tickets for this
  repository, this can be the repository itself if it manages its own patches
  and merge requests. For example it may be some external tracker or service,
  or the user or team to whom the repository belongs.

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v1",
        "https://forgefed.peers.community/ns"
    ],
    "id": "https://dev.example/aviva/treesim",
    "cloneUri": "https://dev.example/aviva/treesim.git",
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
    "ticketsTrackedBy": "https://dev.example/aviva/treesim",
    "sendPatchesTo": "https://dev.example/aviva/treesim",
    "name": "Tree Growth 3D Simulation",
    "summary": "<p>Tree growth 3D simulator for my nature exploration game</p>"
}
```

# Push

To represent an event of [Commit][type-commit]s being pushed to a
[Repository][type-repository], use a ForgeFed [Push][act-push] activity.

Properties:

- [type][]: ["Push"][act-push]
- [actor][]: The entity (person, bot, etc.) that pushed the commits
- [context][]: The [Repository][type-repository] to which the push was made
- [target][]: The specific repo history tip onto which the commits were added,
  this is either a [Branch][type-branch] (for VCSs that have branches) or a
  [Repository][type-repository] (for VCSs that don't have branches, only a
  single history line). If it's a branch, it MUST be a branch belonging to the
  repository specified by [context][]. And if it's a repository, it MUST be
  identical to the one specified by [context][].
- [hashBefore][prop-hashbefore]: Repo/branch/tip hash before adding the new
  commits
- [hashAfter][prop-hashafter]: Repo/branch/tip hash after adding the new
  commits
- [object][]: An [OrderedCollection][] of the [Commit][type-commit]s being
  pushed, in **reverse chronological order**. The [items][] (or
  [orderedItems][]) property of the collection MUST contain either the whole
  list of commits being pushed, or a prefix i.e. continuous subset from the
  beginning of the list (therefore the **latest** commits).
  [earlyItems][prop-earlyitems] MAY be used for listing a suffix i.e.
  continuous subset from the end (therefore the **earliest** commits).

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "id": "https://dev.example/aviva/outbox/E26bE",
    "type": "Push",
    "actor": "https://dev.example/aviva",
    "to": [
        "https://dev.example/aviva/followers",
        "https://dev.example/aviva/game-of-life",
        "https://dev.example/aviva/game-of-life/team",
        "https://dev.example/aviva/game-of-life/followers"
    ],
    "context": "https://dev.example/aviva/game-of-life",
    "target": "https://dev.example/aviva/game-of-life/branches/master",
    "hashBefore": "017cbb00bc20d1cae85f46d638684898d095f0ae",
    "hashAfter": "be9f48a341c4bb5cd79ae7ab85fbf0c05d2837bb",
    "object": {
        "totalItems": 2,
        "type": "OrderedCollection",
        "orderedItems": [
            {
                "id": "https://dev.example/aviva/game-of-life/commits/be9f48a341c4bb5cd79ae7ab85fbf0c05d2837bb",
                "type": "Commit",
                "attributedTo": "https://dev.example/aviva",
                "context": "https://dev.example/aviva/game-of-life",
                "hash": "be9f48a341c4bb5cd79ae7ab85fbf0c05d2837bb",
                "created": "2019-12-02T16:07:32Z",
                "summary": "Add widget to alter simulation speed"
            },
            {
                "id": "https://dev.example/aviva/game-of-life/commits/fa37fe100a8b1e69933889c5bf3caf95cd3ae1e6",
                "type": "Commit",
                "attributedTo": "https://dev.example/aviva",
                "context": "https://dev.example/aviva/game-of-life",
                "hash": "fa37fe100a8b1e69933889c5bf3caf95cd3ae1e6",
                "created": "2019-12-02T15:51:52Z",
                "summary": "Set window title correctly, fixes issue #7"
            }
        ]
    }
}
```

# Ticket

To represent a work item in a project, use the ForgeFed [Ticket][type-ticket]
type.

TODO decide on ticket categories/subtypes and update below

TODO decide on property for titles, update below

TODO properly document `history` or remove it from example

Properties:

- [type][]: ["Ticket"][type-ticket]
- [context][]: The project to which this ticket belongs (a repository, an issue
  tracker, etc.)
- [attributedTo][]: The actor (person, bot, etc.) who submitted the ticket
- [summary][]: The ticket's one-line title, as HTML-escaped plain text
- [content][], [mediaType][]: The ticket's (possibly multi-line) detailed
  description text, in rendered form
- [source][]: Source form of the ticket's description
- [published][]: The time the ticket submission was accepted (which may not be
  the same as the time the ticket was submitted)
- [followers][]: Collection of the followers of the ticket, actors who want to
  be notified on activity related to the ticket
- [team][prop-team]: Collection of project team members who have responsibility
  for work on this ticket and want to be notified on activities related to it
- [replies][]: Collection of direct comments made on the ticket (but not
  comments made *on other* comments on the ticket)
- [dependants][prop-dependants]: Collection of [Ticket][type-ticket]s which
  depend on this ticket
- [dependencies][prop-dependencies]: Collection of [Ticket][type-ticket]s on
  which this ticket depends
- [isResolved][prop-isresolved]: Whether the work on this ticket is done
- [resolvedBy][prop-resolvedby]: If the work on this ticket is done, who marked
  the ticket as resolved, or which activity did so
- [resolved][prop-resolved]: When the ticket has been marked as resolved

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.peers.community/ns"
    ],
    "id": "https://dev.example/aviva/game-of-life/issues/107",
    "type": "Ticket",
    "context": "https://dev.example/aviva/game-of-life",
    "attributedTo": "https://forge.example/luke",
    "summary": "Window title is empty",
    "content": "<p>When I start the simulation, window title disappears suddenly</p>",
    "mediaType": "text/html",
    "source": {
        "mediaType": "text/markdown; variant=Commonmark",
        "content": "When I start the simulation, window title disappears suddenly",
    },
    "published": "2019-11-04T07:00:04.465807Z",
    "followers": "https://dev.example/aviva/game-of-life/issues/107/followers",
    "team": "https://dev.example/aviva/game-of-life/issues/107/team",
    "replies": "https://dev.example/aviva/game-of-life/issues/107/discussion",
    "history": "https://dev.example/aviva/game-of-life/issues/107/activity",
    "dependants": "https://dev.example/aviva/game-of-life/issues/107/rdeps",
    "dependencies": "https://dev.example/aviva/game-of-life/issues/107/deps",
    "isResolved": true,
    "resolvedBy": "https://code.example/martin",
    "resolved": "2020-02-07T06:45:03.281314Z"
}
```

# Comment

To represent a comment, e.g. a comment on a ticket or a merge request, use the
ActivityPub [Note][] type.

Properties:

- [type][]: ["Note"][Note]
- [attributedTo][]: The author of the comment
- [context][]: The topic of the discussion, e.g. a ticket or a merge request.
  It MUST be provided.
- [inReplyTo][]: The entity on which this comment replies. MUST be provided. If
  the comment is made directly on the discussion topic, then [inReplyTo][] MUST
  be identical to [context][]. Otherwise, set [inReplyTo][] to the comment to
  which this comment replies. In that case both comments MUST have an identical
  [context][].
- [content][], [mediaType][], [source][]: The comment text, in rendered form
  and in source form

Example:

```json
{
    "@context": "https://www.w3.org/ns/activitystreams",
    "id": "https://forge.example/luke/comments/rD05r",
    "type": "Note",
    "attributedTo": "https://forge.example/luke",
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
```

[xsd:dateTime]:    https://www.w3.org/TR/xmlschema11-2/#dateTime

[act-push]: /vocabulary.html#act-push

[type-branch]:     /vocabulary.html#type-branch
[type-commit]:     /vocabulary.html#type-commit
[type-repository]: /vocabulary.html#type-repository
[type-ticket]:     /vocabulary.html#type-ticket

[prop-committed]:        /vocabulary.html#prop-committed
[prop-committedby]:      /vocabulary.html#prop-committedby
[prop-description]:      /vocabulary.html#prop-description
[prop-dependants]:       /vocabulary.html#prop-dependants
[prop-dependencies]:     /vocabulary.html#prop-dependencies
[prop-earlyitems]:       /vocabulary.html#prop-earlyitems
[prop-forks]:            /vocabulary.html#prop-forks
[prop-hash]:             /vocabulary.html#prop-hash
[prop-hashafter]:        /vocabulary.html#prop-hashafter
[prop-hashbefore]:       /vocabulary.html#prop-hashbefore
[prop-isresolved]:       /vocabulary.html#prop-isresolved
[prop-ref]:              /vocabulary.html#prop-ref
[prop-resolved]:         /vocabulary.html#prop-resolved
[prop-resolvedby]:       /vocabulary.html#prop-resolvedby
[prop-sendpatchesto]:    /vocabulary.html#prop-sendpatchesto
[prop-team]:             /vocabulary.html#prop-team
[prop-ticketstrackedby]: /vocabulary.html#prop-ticketstrackedby

[prop-created]:     http://purl.org/dc/terms/created

[Collection]:        https://www.w3.org/TR/activitystreams-vocabulary/#dfn-collection
[Note]:              https://www.w3.org/TR/activitystreams-vocabulary/#dfn-note
[OrderedCollection]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-orderedcollection
[Object]:            https://www.w3.org/TR/activitystreams-vocabulary/#dfn-object

[actor]:        https://www.w3.org/TR/activitystreams-vocabulary/#dfn-actor
[attributedTo]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-attributedto
[content]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-content
[context]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-context
[items]:        https://www.w3.org/TR/activitystreams-vocabulary/#dfn-items
[followers]:    https://www.w3.org/TR/activitypub/#followers
[inReplyTo]:    https://www.w3.org/TR/activitystreams-vocabulary/#dfn-inreplyto
[mediaType]:    https://www.w3.org/TR/activitystreams-vocabulary/#dfn-mediatype
[name]:         https://www.w3.org/TR/activitystreams-vocabulary/#dfn-name
[ordereditems]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-ordereditems
[published]:    https://www.w3.org/TR/activitystreams-vocabulary/#dfn-published
[replies]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-replies
[source]:       https://www.w3.org/TR/activitypub/#source-property
[summary]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-summary
[target]:       https://www.w3.org/TR/activitystreams-vocabulary/#dfn-target
[type]:         https://www.w3.org/TR/activitystreams-vocabulary/#dfn-type
