+++
title = "Stabilizing the Object Capability System"
date = 2023-06-09
[extra]
author = "Pere Lev"
+++

The previous blog post discussed the actor system refactoring work. I've built
into Vervis the foundations for actor programming, and started porting Activity
handlers to this new system.

Then, I moved on to my next task, which is about stabilizing ForgeFed's Object
Capability system.

## ForgeFed Stability

The ForgeFed specification has been evolving for a few years now. Much less
implementation work happened, than I hoped, but the spec still made progress,
and so did the 2 primary implementations: Forgejo and Vervis.

During my work implementing the spec in Vervis, I've more and more noticed the
limitations of ActivityPub (on which ForgeFed in based), and I also had long
periods of time in which I took a pause from development work, due to feeling
the impact of the many-hours-at-the-screen and wanting a more people-focused
and less computer-focused life. These things raised a big question for me:
What's my place in the future of ForgeFed?

Despite the challenges, I still felt (and still feel) that passion in me, to
build the foundations for humanity to develop software in an environment that's
about using and developing technology in ways aimed at serving human needs and
holding the whole. Being in the Free Software Community for such a long time,
and seeing the tragic situation with github centralization and people's need
for a new solution, have given me energy to continue this important work.

A big part of the current work plan is also related to funding: I have funding
from NLNet for a year (which started in March), and the work plan is a
combination of my initial draft and the requests and advice of NLNet.

My goals for the funded work are:

1. Create an initial proof-of-concept that implementes a federated application
   based on actor programming rather than ActivityPub
2. Stabilize the core of the ForgeFed specification, without adding whole new
   features, make the big decisions that haven't been made
3. Finish implementing that core in Vervis and turning it into a tool for
   testing other implementations

As the overall direction, I'll be shifting my focus from ActivityPub to
actor-programming, which I believe is a much better foundation for federated
forges, and for federated applications in general. However, in 2023 I'll still
be putting most of my energy into the ActivityPub-based work, bringing the big
open loops to conclusion.

One of these big open loops is the Object Capability system.

## Why Object Capabilities

ActivityPub doesn't have object capabilities built-in. And it's not obvious
whether and how to add them, in a way that's aligned with ActivityPub's design.
Could we, for simplicity, do without them, and use plain old ACLs and RBAC
instead?

For directly issued access, we sort of could. I'm saying *sort of*, because it
would cause the problem of "ambient authority" - merely being on an ACL is
enough to do some access to protected resources, without having to explicitly
own and provide any authorization token for the specific operation. However, if
we let go of solving that problem in ForgeFed (it's not like the whole web is
based on capabilities anyway), accessing a resource that directly granted you
access to it would be fairly easy.

The challenge comes when dealing not with a single resource, but with a
federated network of related resources that can contain and be contained in
other, possible remote resources. For example:

- Project *MyProject* contains a sub-project *MySubProject*, which contains a
  Pull Request tracker *MyPRs* linked with a Git repo *MyRepo*
- There's a team *CoolTeam* that's managing *MyProject*
- I'm a member of *CoolTeam* wanting to merge a PR that someone submitted to
  *MyMRs*

If I contact *MyPRs*, asking to merge PR #123, how does *MyPRs* know that I'm
authorized? It needs to detect that:

1. *MyPRs* is contained in *MySubProject*, so anyone with access to
   *MySubProject* can also access *MyPRs*
2. *MySubProject* is in turn contained in *MyProject*, so if I had access to
   *MyProject*, I'd be able to access *MyPRs*
3. *CoolTeam* is managing *MyProject*, so if I were either in *CoolTeam* itself
   or in any of its subteams, I could access *MyPRs*

And indeed I'm a member of *CoolTeam*, so I expect *MyPRs* to approve my
request to merge PR #123. But how does *MyPRs* detect that chain of related
resources that links between *MyPRs* and me, given that all of these resources
may live on different servers?

That's where Object Capabilities shine: They a *flexible* tool that easily
supports *distributed* authorization:

- *MyPRs* contacts *MySubProject*, saying: Here's an access token for me. Since
  I'm contained in you, give this token to anyone who has access to you, so
  that they can access me as well.
- *MySubProjet* in turn contacts *MyProject*, passing a token as well
- *MyProject* similarly passes a token to *CoolTeam*
- *CoolTeam* passes a token to me

Now, when I want to merge PR #123, I pass my token to *MyPRs*. And *MyPRs* can
verify the chain of tokens and be sure my access to *MyPRs* is approved at all
the links in the chain.

# Representing Object Capabilities

ActivityPub doesn't have any standard support for object capabilities.
Actually, it doesn't even distinguish between commands and events, and uses
*descriptions* of events to issue commands, rather than referring to
explicitly-declared methods of actors. I'm guessing ActivityPub is primarily
made for publishing personal objects (notes, images, videos, etc.) and personal
events (read, like, eat, etc.), and not for general complex interaction logc
between remote objects. ForgeFed doesn't fit the personal-publishing picture,
since it's about collaborative resources such as issues, PRs, repos and teams.
But given the current situation where ForgeFed is based on ActivityPub, how do
we represent Object Capabilities?

When I first asked myself this question, and read the available material and
ideas about adding OCAPs to the Fediverse, I realized most of it was about C2S
and not S2S, and that mostly just visionary ideas and rough experiments were
available. Anything beyond that was lying in the realm of actor-programming, a
whole new dream for distributed application architecture and development.

So I went for a custom design for OCAPs, using a combination of ActivityPub
activities and new ForgeFed activities:

- Object capabilities are granted using a newly defined `Grant` activity, whose
  `id` is used for invoking the capability
- People can ask to add members to repos/projects/etc. using `Invite` and
  `Join` activities, and if the request is approved, the resource sends a
  `Grant`
- `Grant`s can "delegate" other `Grant`s, i.e. extend the chain by adding a new
  link

This is a design of a kind I called **representational** in the previous blog
post. So it's not ideal. But given the design of ActivityPub and wanting to
design something that doesn't diverge from it, I decided it's reasonable.

Since then, I really hoped someone else, some other projects, would want or
need OCAPs, and a standard OCAP system for the Fediverse would emerge. I also
looked into other Fediverse projects, to see if anyone needed OCAPs. But I
couldn't find anything. It seemed that Fediverse apps are mostly in the field
of personal content publishing and sharing, and ForgeFed is almost alone trying
to use ActivityPub for collaborative resource access and complex distributed
authorization.

But still, in my funded work plan, I put a task: Check out existing OCAP
systems, and see if I can adapt ForgeFed's system to be compatible with them.
It could potentially save a lot of work for implementors, being able to use a
ready OCAP implementation instead of implementing a custom one from scratch.

## Existing Object Capability Systems

I found 2 systems that seem relevant:

- [UCAN](https://ucan.xyz)
- [ZCAP](https://w3c-ccg.github.io/zcap-spec)

Benefits over the custom system:

- Ability to embed delegations instead of just linking to them
- Existing UCAN implementations in both Go (for Forgejo) and Haskell (for
  Vervis)
- Capabilities are cryptoraphically signed, which allows to verify their
  authenticity using the signature rather than relying on `HTTP GET`ing the
  `id` URI

That made UCANs quite appealing! But when I looked deeper, I also felt that
the following factors have an impact.

For ZCAPs:

- ZCAP, while evolving over the years, is still a draft, still changing, and
  still relies on Linked Data signatures, which are a big burden, requiring an
  implementation of complicated JSON-LD algorithms
- ZCAP doesn't an a vocabulary for methods and invocations of them, so I'd
  still have to custom-define that for ForgeFed
- No ready-to-use ZCAP implementations anyway

And for UCANs:

- UCANs have a separate spec for invocation, which would mean diverging from
  ActivityPub-based invocation, making ForgeFed quite incompatible with the
  rest of the Fediverse
- UCANs rely on DIDs, but the Fediverse isn't using decentralized IDs, so we'd
  need to pick and implement a DID method relevant for the Fediverse, such as
  `did:web`
- UCANs can be used without the invocation part, but that decreases the benefit
  of reusing them, especially since we need our own DID
- Fission, the company which seems to be leading the UCAN project, has
  implemented its software in Haskell, but the Haskell implementation of UCANs
  seems minimal and just for what Fission needs, e.g. by supporting only
  `did:key`, and the code hasn't been updated for 10 months

My primary concern is that switching to UCANs, but still needing to add extras
and adaptations, and a whole new JWT-based representation, would significantly
increase the ForgeFed specification's complexity. The custom system, while
being custom, seems simpler to me, and based purely on Activities, which is
very much in line with being an ActivityPub-based protocol.

What now?

## Adapting the Custom System

I decided that instead of using ZCAPs or UCANs, I'll try to *tweak* the custom
system to include the features and benefits that other systems have, and settle
on a stable complete definition that ForgeFed and its implementation can safely
depend on.

Here are some powers and benefits of OCAP systems out there (not just
ZCAP/UCAN):

- OCAPs have a start time and an expiration time
- OCAPs can be cryptographically signed and verified, and therefore embedded
- Revocations can refer to OCAPs by embedding them, because they're signed
- Revocations are done by spreading revocation messages in the network, instead
  of using live URIs
- Promises, i.e. asynchronously sending the return value of a command sent
  earlier
- Immediate return values beyond success-or-failure HTTP status codes
- Promise pipelining, i.e. sending method calls against actors and parameters
  that haven't been created/computed/delivered yet, for network and programming
  efficiency

For the first 4 items, I've proposed updates to the ForgeFed specification:

1. Allow `Grant`s to specify a `startTime` and `endTime`
2. Use JSON-based object signatures to allow signing activities without relying
   on JSON-LD (thanks to silverpill defining a
   [FEP](https://codeberg.org/fediverse/fep/src/branch/main/feps/fep-8b32.md)
   for that)
3. Revocation messages may be a necessity in a fully p2p system, but a big
   complication for systems like the Fediverse which do have live URIs, so I've
   proposed to keep using live URIs for revocation but allow a *time buffer* to
   prevent these URIs from being checked unnecessarily often (e.g. I don't
   think more than once-a-second would be needed in most cases, maybe even
   once-a-minute)

At the time of writing, the PRs are still in review:
[#197](https://codeberg.org/ForgeFed/ForgeFed/pulls/197)
[#198](https://codeberg.org/ForgeFed/ForgeFed/pulls/198),
[#199](https://codeberg.org/ForgeFed/ForgeFed/pulls/199).

In the meantime, I've implemented these changes in Vervis, including progress
porting the OCAP activity handlers to the new actor system:

- [Optional duration buffer for Grant
  revocation](https://codeberg.org/ForgeFed/Vervis/commit/a22aeb85d09b9207f2d1f3ac1ca546fbd319be51)
- [Grant start & end times](https://codeberg.org/ForgeFed/Vervis/commit/ba02d62eb5b4ceb5cd871463f714a4d5b15f86f6)
- Object integrity proof
  [generation](https://codeberg.org/ForgeFed/Vervis/commit/e8e587af26944d3ea8d91f5c47cc3058cf261387)
  and
  [verification](https://codeberg.org/ForgeFed/Vervis/commit/621275e25762a1c1e5860d07a6ff87b147deed4f)
- `Deck` (i.e. issue tracker actor) handlers:
  [Accept-Reject-Follow-Undo](https://codeberg.org/ForgeFed/Vervis/commit/9955a3c0ad7f459b1579e1a2fe61c6cb663a9a7c),
  [Invite](https://codeberg.org/ForgeFed/Vervis/commit/85f77fcac47b1fbedfabe7f87d9383c92a5deef5),
  [Join](https://codeberg.org/ForgeFed/Vervis/commit/59e99f405adc862d253e7da819cadeaf29b380c7)
- (Mostly trivial) `Person` handlers:
  [Invite](https://codeberg.org/ForgeFed/Vervis/commit/4d8e5de8b82ce12d1701d43cce50dd90748d7970),
  [Join](https://codeberg.org/ForgeFed/Vervis/commit/b759b87d0f0c21c920df83033c44fbaae1e8e229),
  [Revoke](https://codeberg.org/ForgeFed/Vervis/commit/d467626049c814b9b90c77e45ba444177e0b61b5)

## Beyond ActivityPub

So, 4 items from the OCAP-features list are taken care of. What remains is:

- Promises
- Return values
- Promise pipelining

It's technically possible to extend ActivityPub to support these things, but
they also represent a significant shift from the (perhaps too) simple activity
model that standard ActivityPub has. And they involve some non-trivial
implementation work, especially promise pipelining. The approach I'm taking is
to implement the ActivityPub-based ForgeFed without those tools, and leaving
them for the more thorough actor-programming systems (such as Spritely and
Cap'n Proto) where such tools are available.

In parallel to the ActivityPub-based work, I'm already evolving an actor
programming system, step by step, and intending to use it for the "Capybara
experiment" AKA actor-system based Fediverse proof-of-concept.

Considering that Spritely is already working on the same thing, and that Cap'n
Proto has a Haskell implementation - am I wasting my time here? Hard (for me)
to say. I just know I'm very excited about actor programming, and that it's
still an evolving technology, and Spritely is only in Scheme right now, so a
Haskell library for actor programming is a valuable addition to the picture.
Cap'n Proto is a lower-level tool, but perhaps my system can wrap Cap'n Proto
or serve as inspiration for a higher-level API to use with Cap'n Proto.

And perhaps I can get a grant to fund my work on actor programming? And perhaps
more people will want to contribute? And perhaps a plugin system can allow
writing actors in different languages into the same application? We'll see :)

Landing back to the current focus: Stabilizing the core of the
ActivityPub-based ForgeFed.

## Comments

We have an account for ForgeFed on the Fediverse:
<https://floss.social/@forgefed>

Right after publishing this post, I'll make a toot there to announce the post,
and you can comment there :)
