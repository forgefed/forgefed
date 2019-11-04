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
* [name][]: The commit's one-line title as plain text; if the commit title and
  description are a single commit message string, then the title is the 1st
  line of the commit message
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
    "name": "Add an installation script, fixes issue #89",
    "description": {
        "mediaType": "text/plain",
        "content": "It's about time people can install it on their computers!"
    }
}
```

# Branch

TODO

# Repository

TODO

# Pushing Commits into a Repository

TODO

# Ticket

TODO

[xsd:dateTime]:    https://www.w3.org/TR/xmlschema11-2/#dateTime

[type-commit]:     /vocabulary.html#type-commit
[type-repository]: /vocabulary.html#type-repository

[prop-committed]:   /vocabulary.html#prop-committed
[prop-committedby]: /vocabulary.html#prop-committedby
[prop-description]: /vocabulary.html#prop-description
[prop-hash]:        /vocabulary.html#prop-hash

[prop-created]:     http://purl.org/dc/terms/created

[attributedTo]: https://www.w3.org/TR/activitystreams-vocabulary/#dfn-attributedto
[content]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-content
[context]:      https://www.w3.org/TR/activitystreams-vocabulary/#dfn-context
[mediaType]:    https://www.w3.org/TR/activitystreams-vocabulary/#dfn-mediatype
[name]:         https://www.w3.org/TR/activitystreams-vocabulary/#dfn-name
[type]:         https://www.w3.org/TR/activitystreams-vocabulary/#dfn-type
