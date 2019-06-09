# ForgeFed Vocabulary - DRAFT

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

This document describes the ForgeFed vocabulary. It's intended to be an extension
of the [ActivityPub Vocabulary](https://www.w3.org/TR/activitystreams-vocabulary/)
and provides additional vocabulary for federation of project management and
version control system hosting and collaboration platforms.

## Table of Contents
1. [Introduction](#Introduction)
2. [Types](#Types)
3. [Properties](#Properties)

## Introduction

The ForgeFed Vocabulary describes a set of types and properties to be used by
platforms that support the ForgeFed protocol.

## Types

Base URI: `https://forgefed.peers.community/ns`

### Activity Types

#### Follow

**URI:** `https://www.w3.org/ns/activitystreams#Follow`

**Notes:** used by a user who wants to follow a repository.
This activity doesn't define a new type (the `Follow` Activity is defined in
ActivityPub) but it's here for reference.

**Example:**

    {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://forgefed.peers.community/ns"
        ],
        "summary": "Alice followed Bob",
        "type": "Follow",
        "actor": "https://localhost/alice",
        "object": "https://remotehost/bob/repository"
    }

#### Push

**URI:** `https://forgefed.peers.community/ns#Push`

**Notes:** Indicates that new content has been pushed to the repository. The
Activity's object MUST contain a list of Commits.

**Example:**

    {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://forgefed.peers.community/ns"
        ],
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

### Actor Types

#### Repository

**URI:** `https://forgefed.peers.community/ns#Repository`

**Notes:** Represents a single repository.

**Example:**

    {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://forgefed.peers.community/ns"
        ],
        "type": "Repository",
        "name": "Homeworks-2019"
    }

### Object Types

#### Commit

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
        "author": ""
        "message": "Fix #89"
    }

#### Ticket

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

## Properties


