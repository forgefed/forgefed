# Project Hosting Federation Vocabulary

## Intro

This is a draft of a linked data / semantic web vocabulary for expressing
information about version control repos and related technology such as issues
and merge requests. It's meant to be used for decentralization of project
hosting by making repo hosting platforms federate using ActivityPub.

The vocabulary here is going to be an extension to the ActivityStreams 2
vocabulary (to which ActivityPub is an existing core extension).

I suggest we start by keeping 2 lists: A list of classes (kinds of things, e.g.
"repo" and "merge request" and "issue" etc.) and a list of properties (e.g.
"name", "description", "main-branch", "creation-time").

For a class, specify:

- Name
- Description
- Superclasses (e.g. Person is a subclass of LivingBeing)

For a property:

- Name
- Description
- Superproperties (e.g. 'loves' is a subproperty of 'knows')
- Domain (e.g. in "A loves B", A probably has to be a person, or at least some
  living being)
- Range (e.g. in "A lives at B", B has to be a Location/Place)
