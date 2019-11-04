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
