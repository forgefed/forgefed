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

The file `VOCABULARY.md` contains these 2 lists. Other files such as `ISSUE.md`
have plans and ideas and info, based on which the vocabulary is gradually
written.

The intention is to reuse properties and classes in the RDFiverse and
ActivityPub! Some things in VOCABULARY.md may be removed in favor of existing
entities defined in such places. As a result, though, we need to provide
guidelines for the stuff that should be included in JSON-LD data sent between
servers! For example, if we reuse `dc:author` from the Dublin Core ontology,
eventually `ISSUE.md` should have an example for a JSON-LD issue object, to
show the use of `dc:author` there.

We may need a base URI for the ActivityPub extension. I suggest we add the
following mapping to the JSON-LD context:

`"forge": "https://forgefed.org/ns#"`

And we can put in this namespace everything that doesn't come from other
places. Later that mapping could be changed into a remote context URL, but,
let's leave that cosmetic detail for later (also I must say, I don't like this
pretentious cramming of everything into 1 remote context like AP does; I like
the general RDF way where you just freely add namespace prefixes and use
whatever you like from the RDFiverse).
