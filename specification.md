# ForgeFed Specification - DRAFT

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
and provides additional vocabulary for federation of version control services.

## Table of Contents
1. [Introduction](#Introduction)
2. [Types](#Types)
3. [Properties](#Properties)
4. [Client to Server Interactions](#Client to Server Interactions)

## Introduction

## Types

Base URI: `https://peers.community/ns/repo-fed-vocab#`

### Activity Types

#### Follow

**URI:** `https://www.w3.org/ns/activitystreams#Follow`

**Notes:** used by a user who wants to follow a repository

**Example:**

    {
        "@context": "https://www.w3.org/ns/activitystreams",
        "summary": "Alice followed Bob",
        "type": "Follow",
        "actor": "https://localhost/alice",
        "object": "https://remotehost/bob"
    }

#### Push

**URI:** `https://peers.community/ns/repo-fed-vocab#Push`

**Notes:**

**Example:**

    {
        "@context": "https://www.w3.org/ns/activitystreams",
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

### Object Types

#### Commit

**URI:** `https://peers.community/ns/repo-fed-vocab#Commit`

**Notes:** 

**Example:**

    {
        "@context": "https://peers.community/ns/repo-fed-vocab#",
        "type": "Commit",
        "id": "https://localhost/alice/repo2/commit/2c7323781aec1f7",
        "author": ""
        "message": "Fix #89"
    }

#### Ticket

**URI:** `https://peers.community/ns/repo-fed-vocab#Ticket`

**Notes:** 

**Example:**

    {
        "@context": "https://peers.community/ns/repo-fed-vocab#",
        "type": "Ticket",
        "id": "https://localhost/alice/repo2/issues/42",
        "attributedTo": "",
        "author": "",
        "title": "Nothing works!",
        "content": "Please fix. Everything is broken!",
        "context": ""
    }

## Properties

## Client to Server Interactions

### Follow Activity

The `Follow` activity is used to subscribe to the activities of a repository.

### Push Activity

The `Push` activity is used to notify followers of new code that has been
pushed to a repository.
