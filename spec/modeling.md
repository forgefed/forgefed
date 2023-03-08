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
        "https://forgefed.org/ns"
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
        "https://forgefed.org/ns"
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
* [cloneUri][prop-cloneuri]: The endpoint from which the content of the repository can be
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
* [sendPatchesTo][prop-sendpatchesto]: The actor that tracks patches for this
  repository, this can be the repository itself if it manages its own patches
  and merge requests. For example it may be some external tracker or service,
  or the user or team to whom the repository belongs.
* [context][]: The [Project][type-project](s) to which this repository belongs

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v1",
        "https://forgefed.org/ns"
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
    "attributedTo": "https://example.dev/bob",
    "summary": "<p>Tree growth 3D simulator for my nature exploration game</p>"
}
```

# Project

Properties:

* [type][]: ["Project"][type-project]
* [name][]: The user-given name of the project, e.g. "My cool project"
* [published][]: The time the project was created on the server
* [summary][]: A one-line user provided description of the project, as HTML,
  e.g. "`<p>A command-line tool that does cool things</p>`"
* [ticketsTrackedBy][prop-ticketstrackedby]: The default ticket tracker to use
  when submitting a ticket to this project (this tracker MUST be listed under
  the project's [components][prop-components])
* [subprojects][prop-subprojects]: A [Collection][] of the subprojects of this
  project
* [context][]: The parent [Project][type-project](s) to which this project
  belongs

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://dev.example/projects/wanderer",
    "type": "Project",

    "name": "Wanderer",
    "summary": "3D nature exploration game",
    "components": {
        "type": "Collection",
        "totalItems": 7,
        "items": [
            https://dev.example/repos/opengl-vegetation",
            https://dev.example/repos/opengl-vegetation/patch-tracker",
            https://dev.example/repos/treesim",
            https://dev.example/repos/treesim/patch-tracker",
            https://dev.example/repos/wanderer",
            https://dev.example/repos/wanderer/patch-tracker",
            https://dev.example/issue-trackers/wanderer"
        ]
    },
    "subprojects": {
        "type": "Collection",
        "totalItems": 2,
        "items": [
            "https://dev.example/projects/nature-3d-models",
            "https://dev.example/projects/wanderer-fundraising"
        ]
    },
    "ticketsTrackedBy": "https://dev.example/issue-trackers/wanderer",

    "inbox": "https://dev.example/projects/wanderer/inbox",
    "outbox": "https://dev.example/projects/wanderer/outbox",
    "followers": "https://dev.example/projects/wanderer/followers"
}
```

# Team Membership

Properties:

- [type][]: [Relationship][]
- [subject][]: A [Team][type-team]
- [relationship][]: [hasMember][prop-hasmember]
- [object][]: A [Person][] who is a member of the `Team`
- [tag][]: The role that the member has in the team

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://dev.example/teams/mobilizon-dev-team/members/ThmsicTj",
    "type": "Relationship",
    "subject": "https://dev.example/teams/mobilizon-dev-team",
    "relationship": "hasMember",
    "object": "https://dev.example/people/celine",
    "tag": "https://roles.example/developer"
}
```

# Team

Properties:

* [type][]: ["Team"][type-team]
* [name][]: The user-given name of the team, e.g. "Gitea Development Team"
* [published][]: The time the team was created on the server
* [summary][]: A one-line user provided description of the project, as HTML,
  e.g. `"We are creating a code hosting platform"`
* [members][prop-members]: [Collection][] of the members of this team (see
  details in [Vocabulary specification][prop-members])
* [subteams][prop-subteams]: Subteams of this team, i.e. teams whose members
  (and subteams) inherit the access that this team has been granted (to
  projects, repositories, etc.)
- [context][]: Parent [Team][type-team]s of this team, i.e. teams from which
  this team inherits access to projects, components and resources, e.g.
  repositories, ticket trackers (and passes them to its [members][prop-members]
  and inherits them to its own [subteams][prop-subteams])

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://w3id.org/security/v2",
        "https://forgefed.org/ns"
    ],
    "id": "https://dev.example/teams/mobilizon-dev-team",
    "type": "Team",
    "name": "Mobilizon Development Team",
    "summary": "We're creating a federated tool for organizing events!",
    "members": {
        "type": "Collection",
        "totalItems": 3,
        "items": [
            { "type": "Relationship",
              "subject": "https://dev.example/teams/mobilizon-dev-team",
              "relationship": "hasMember",
              "object": "https://dev.example/people/alice",
              "tag": "https://roles.example/admin"
            },
            { "type": "Relationship",
              "subject": "https://dev.example/teams/mobilizon-dev-team",
              "relationship": "hasMember",
              "object": "https://dev.example/people/bob",
              "tag": "https://roles.example/maintainer"
            },
            { "type": "Relationship",
              "subject": "https://dev.example/teams/mobilizon-dev-team",
              "relationship": "hasMember",
              "object": "https://dev.example/people/celine",
              "tag": "https://roles.example/developer"
            }
        ]
    },
    "subteams": {
        "type": "Collection",
        "totalItems": 2,
        "items": [
            "https://dev.example/teams/mobilizon-backend-team",
            "https://dev.example/teams/mobilizon-frontend-team"
        ]
    },
    "context": "https://dev.example/teams/framasoft-developers",

    "publicKey": {
        "id": "https://dev.example/teams/mobilizon-dev-team#main-key",
        "owner": "https://dev.example/teams/mobilizon-dev-team",
        "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhki....."
    },
    "inbox": "https://dev.example/teams/mobilizon-dev-team/inbox",
    "outbox": "https://dev.example/teams/mobilizon-dev-team/outbox",
    "followers": "https://dev.example/teams/mobilizon-dev-team/followers"
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
        "https://forgefed.org/ns"
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
- [context][]: The [TicketTracker][type-tickettracker] or
  [PatchTracker][type-patchtracker] to which this ticket belongs
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
        "https://forgefed.org/ns"
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

# Access Control

## Giving Access

### Invite

To offer some actor access to a shared resource (such as a repository or a
ticket tracker), use an ActivityPub [Invite][] activity.

Properties:

- [type][]: ["Invite"][Invite]
- [actor][]: The entity (person, bot, etc.) that is offering access
- [instrument][]: A [Role][type-role] specifying which operations on the
  resource are being allowed
- [target][]: The resource, access to which is being given (for example, a
  repository)
- [object][]: The actor who is being gives access to the resource
- [capability][prop-capability]: A previously published `Grant`, giving the
  `actor` permission to invite more actors to access the resource

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://dev.example/aviva/outbox/B47d3",
    "type": "Invite",
    "actor": "https://dev.example/aviva",
    "to": [
        "https://dev.example/aviva/followers",
        "https://coding.community/repos/game-of-life",
        "https://coding.community/repos/game-of-life/followers",
        "https://software.site/bob",
        "https://software.site/bob/followers"
    ],
    "instrument": "https://roles.example/maintainer",
    "target": "https://coding.community/repos/game-of-life",
    "object": "https://software.site/bob",
    "capability": "https://coding.community/repos/game-of-life/outbox/2c53A"
}
```

### Join

To request access to a shared resource, use an ActivityPub [Join][] activity.

Properties:

- [type][]: ["Join"][Join]
- [actor][]: The entity (person, bot, etc.) that is requesting access
- [instrument][]: A [Role][type-role] specifying which operations on the
  resource are being requested
- [object][]: The resource, access to which is being given (for example, a
  repository)
- [capability][prop-capability]: *(optional)* A previously published `Grant`,
  giving the `actor` permission to gain access to the resource without the
  approval of another actor. If `capability` isn't provided, the resource won't
  grant access before someone with adequate access approves the Join request.

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://software.site/bob/outbox/c97E3",
    "type": "Join",
    "actor": "https://software.site/bob",
    "to": [
        "https://coding.community/repos/game-of-life",
        "https://coding.community/repos/game-of-life/followers",
        "https://software.site/bob/followers"
    ],
    "instrument": "https://roles.example/maintainer",
    "object": "https://coding.community/repos/game-of-life",
    "capability": "https://coding.community/repos/game-of-life/outbox/d38Fa"
}
```

### Grant

To give some actor access to a shared resource, use a ForgeFed
[Grant][act-grant] activity.

Properties:

- [type][]: ["Grant"][act-grant]
- [actor][]: The entity (person, bot, etc.) that is giving access
- [object][]: A [Role][type-role] specifying which operations on the
  resource are being allowed
- [context][]: The resource, access to which is being given (for example, a
  repository)
- [target][]: The actor who is being gives access to the resource
- [fulfills][prop-fulfills]: The activity that triggered the sending of the
  `Grant`, such as a related `Invite` (another example: if Alice [Create][]s a
  new repository, the repository may automatically send back a
  [Grant][act-grant] giving Alice admin access, and this Grant's `fulfills`
  refers to the [Create][] that Alice sent)
- [result][]: A URI that can be used later for verifying that the given access
  is still approved, thus allowing the actor granting the access to revoke it
- [allows][prop-allows]: Modes of invocation and/or delegation that this
  `Grant` is meant to be used for
- [delegates][prop-delegates]: If this `Grant` is a delegation, i.e. it is
  passing on some access that it has received, `delegates` specifies the parent
  `Grant` that it has received and now passing on

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://coding.community/repos/game-of-life/outbox/9fA8c",
    "type": "Grant",
    "actor": "https://coding.community/repos/game-of-life",
    "to": [
        "https://dev.example/aviva",
        "https://dev.example/aviva/followers",
        "https://coding.community/repos/game-of-life/followers",
        "https://software.site/bob",
        "https://software.site/bob/followers"
    ],
    "object": "https://roles.example/maintainer",
    "context": "https://coding.community/repos/game-of-life",
    "target": "https://software.site/bob",
    "fulfills": "https://dev.example/aviva/outbox/B47d3",
    "allows": "invoke"
}
```

## Canceling Access

### Remove

To disable an actor's membership in a shared resource, invalidating their
access to it, use an ActivityPub [Remove][] activity.

Properties:

- [type][]: ["Remove"][Remove]
- [actor][]: The actor (person, bot, etc.) that is disabling access
  disabled
- [object][]: The actor whose access to the resource is being taken away
- [origin][]: The resource, access to which is being taken away (for example, a
  repository)
- [capability][prop-capability]: A previously published `Grant`, giving the
  `actor` permission to disable the [object][] actor's access to the resource

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://dev.example/aviva/outbox/F941b",
    "type": "Remove",
    "actor": "https://dev.example/aviva",
    "to": [
        "https://dev.example/aviva/followers",
        "https://coding.community/repos/game-of-life",
        "https://coding.community/repos/game-of-life/followers",
        "https://software.site/bob",
        "https://software.site/bob/followers"
    ],
    "origin": "https://coding.community/repos/game-of-life",
    "object": "https://software.site/bob",
    "capability": "https://coding.community/repos/game-of-life/outbox/2c53A"
}
```

### Leave

To withdraw your consent for membership in a shared resource, invalidating
your access to it, use an ActivityPub [Leave][] activity.

Properties:

- [type][]: ["Leave"][Leave]
- [actor][]: The actor (person, bot, etc.) that is requesting to disable their
  own access
- [object][]: The resource, access to which is being disabled (for example, a
  repository)

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://software.site/bob/outbox/d08F4",
    "type": "Leave",
    "actor": "https://software.site/bob",
    "to": [
        "https://coding.community/repos/game-of-life",
        "https://coding.community/repos/game-of-life/followers",
        "https://software.site/bob/followers"
    ],
    "object": "https://coding.community/repos/game-of-life"
}
```

### Revoke

Another activity that can be used for disabling access is [Revoke][act-revoke].
While [Remove](#remove) and [Leave](#leave) are meant for undoing the effects
of [Invite](#invite) and [Join](#join), `Revoke` is provided as an opposite of
[Grant](#grant). See the Behavior specification for more information about the
usage of these different activity types in revocation of access to shared
resources.

Properties:

- [type][]: ["Revoke"][act-revoke]
- [actor][]: The actor (person, bot, etc.) that is revoking access
- [instrument][]: The [Role][type-role] that the [origin][] actor had with
  respect to accessing the resource, and which is now being taken away
- [context][]: The resource, access to which is being revoked
- [origin][]: The actor whose access to the resource is being revoked
- [fulfills][prop-fulfills]: An activity that triggered the sending of the
  `Grant`, such as a related `Remove` or `Leave`
- [object][]: specific [Grant](#grant) activities being undone, i.e. the access
  that they granted is now disabled and it cannot be used anymore as the
  [capability][prop-capability] of activities

Example:

```json
{
    "@context": [
        "https://www.w3.org/ns/activitystreams",
        "https://forgefed.org/ns"
    ],
    "id": "https://coding.community/repos/game-of-life/outbox/1C0e2",
    "type": "Revoke",
    "actor": "https://coding.community/repos/game-of-life",
    "to": [
        "https://coding.community/repos/game-of-life/followers",
        "https://software.site/bob",
        "https://software.site/bob/followers"
    ],
    "instrument": "https://roles.example/maintainer",
    "context": "https://coding.community/repos/game-of-life",
    "origin": "https://software.site/bob",
    "object": "https://coding.community/repos/game-of-life/outbox/9fA8c"
}
```

### Undo a Grant {#undo-grant}

The Behavior spec describes flows in which the [Revoke](#revoke) activity is
used by resources (more accurately, by the actors managing them) to announce
that they're disabling [Grant](#grant)s that they previously sent. To allow for
a clear distinction, another activity is provided here, for *other* actors to
*request* the revocation of specific [Grant](#grant)s: The ActivityPub [Undo][]
activity.

It's likely that `Grant`s would exist behind-the-scenes in applications, and
human actors would then use activities such as `Remove` and `Leave` for
disabling access. But the ability to disable specific `Grant`s may be required
for ensuring and maintaining system security, therefore `Undo` is provided here
as well.

Properties:

- [type][]: ["Undo"][Undo]
- [actor][]: The actor (person, bot, etc.) that is revoking access
- [object][]: specific [Grant](#grant) activities being undone, i.e. the access
  that they granted is now disabled and it cannot be used anymore as the
  [capability][prop-capability] of activities
- [capability][prop-capability]: A previously published `Grant`, giving the
  `actor` permission to disable the [object][] actor's access to the resource

[xsd:dateTime]:    https://www.w3.org/TR/xmlschema11-2/#dateTime

[act-grant]:  /vocabulary.html#act-grant
[act-push]:   /vocabulary.html#act-push
[act-revoke]: /vocabulary.html#act-revoke

[type-branch]:     /vocabulary.html#type-branch
[type-commit]:     /vocabulary.html#type-commit
[type-patchtracker]: /vocabulary.html#type-patchtracker
[type-project]:    /vocabulary.html#type-project
[type-repository]: /vocabulary.html#type-repository
[type-role]:       /vocabulary.html#type-role
[type-team]:       /vocabulary.html#type-team
[type-ticket]:     /vocabulary.html#type-ticket
[type-tickettracker]: /vocabulary.html#type-tickettracker

[prop-allows]:           /vocabulary.html#prop-allows
[prop-capability]:       /vocabulary.html#prop-capability
[prop-cloneuri]:         /vocabulary.html#prop-cloneuri
[prop-committed]:        /vocabulary.html#prop-committed
[prop-committedby]:      /vocabulary.html#prop-committedby
[prop-components]:       /vocabulary.html#prop-components
[prop-delegates]:        /vocabulary.html#prop-delegates
[prop-description]:      /vocabulary.html#prop-description
[prop-dependants]:       /vocabulary.html#prop-dependants
[prop-dependencies]:     /vocabulary.html#prop-dependencies
[prop-earlyitems]:       /vocabulary.html#prop-earlyitems
[prop-forks]:            /vocabulary.html#prop-forks
[prop-fulfills]:         /vocabulary.html#prop-fulfills
[prop-hash]:             /vocabulary.html#prop-hash
[prop-hasmember]:        /vocabulary.html#prop-hasmember
[prop-hashafter]:        /vocabulary.html#prop-hashafter
[prop-hashbefore]:       /vocabulary.html#prop-hashbefore
[prop-isresolved]:       /vocabulary.html#prop-isresolved
[prop-members]:          /vocabulary.html#prop-members
[prop-ref]:              /vocabulary.html#prop-ref
[prop-resolved]:         /vocabulary.html#prop-resolved
[prop-resolvedby]:       /vocabulary.html#prop-resolvedby
[prop-sendpatchesto]:    /vocabulary.html#prop-sendpatchesto
[prop-subprojects]:      /vocabulary.html#prop-subprojects
[prop-subteams]:         /vocabulary.html#prop-subteams
[prop-team]:             /vocabulary.html#prop-team
[prop-ticketstrackedby]: /vocabulary.html#prop-ticketstrackedby

[prop-created]:     http://purl.org/dc/terms/created

[Collection]:        https://www.w3.org/TR/activitystreams-vocabulary/#dfn-collection
[Create]:            https://www.w3.org/TR/activitystreams-vocabulary/#dfn-create
[Invite]:            https://www.w3.org/TR/activitystreams-vocabulary/#dfn-invite
[Join]:              https://www.w3.org/TR/activitystreams-vocabulary/#dfn-join
[Leave]:             https://www.w3.org/TR/activitystreams-vocabulary/#dfn-leave
[Note]:              https://www.w3.org/TR/activitystreams-vocabulary/#dfn-note
[OrderedCollection]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-orderedcollection
[Object]:            https://www.w3.org/TR/activitystreams-vocabulary/#dfn-object
[Person]:            https://www.w3.org/TR/activitystreams-vocabulary/#dfn-person
[Remove]:            https://www.w3.org/TR/activitystreams-vocabulary/#dfn-remove
[Undo]:              https://www.w3.org/TR/activitystreams-vocabulary/#dfn-undo

[actor]:        https://www.w3.org/TR/activitystreams-vocabulary/#dfn-actor
[attributedTo]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-attributedto
[content]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-content
[context]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-context
[items]:        https://www.w3.org/TR/activitystreams-vocabulary/#dfn-items
[followers]:    https://www.w3.org/TR/activitypub/#followers
[inReplyTo]:    https://www.w3.org/TR/activitystreams-vocabulary/#dfn-inreplyto
[instrument]:   https://www.w3.org/TR/activitystreams-vocabulary/#dfn-instrument
[mediaType]:    https://www.w3.org/TR/activitystreams-vocabulary/#dfn-mediatype
[name]:         https://www.w3.org/TR/activitystreams-vocabulary/#dfn-name
[ordereditems]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-ordereditems
[origin]:       https://www.w3.org/TR/activitystreams-vocabulary/#dfn-origin
[published]:    https://www.w3.org/TR/activitystreams-vocabulary/#dfn-published
[relationship]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-relationship
[replies]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-replies
[result]:       https://www.w3.org/TR/activitystreams-vocabulary/#dfn-result
[source]:       https://www.w3.org/TR/activitypub/#source-property
[subject]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-subject
[summary]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-summary
[tag]:          https://www.w3.org/TR/activitystreams-vocabulary/#dfn-tag
[target]:       https://www.w3.org/TR/activitystreams-vocabulary/#dfn-target
[type]:         https://www.w3.org/TR/activitystreams-vocabulary/#dfn-type
