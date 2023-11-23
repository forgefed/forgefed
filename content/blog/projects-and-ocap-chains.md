+++
title = "Projects & Grant Chains"
date = 2023-11-13
[extra]
author = "Pere Lev"
+++

It's been 5 months since the previous blog post! Much longer than I hoped. The
features I've been working on proved to be much more complex to implement, than
I anticipated. With the frustration and exhaustion building up, I kept working
in small chunks, and the result is finally here.

After all the many words below there's a demo as well.

Take a look at my [task board][kanban] for more context while reading.

## Vervis and OCAPs

A bit of background just in case you missed it. I've been working in 2
channels:

- Make updates and additions to the [ForgeFed specification](/spec)
- Implementing them in [Vervis][], a proof-of-concept reference-implementation
  ForgeFed server written in Haskell

One of my primary topics has been Object Capabilities (or OCAPs), which are
decentralized authorization tokens. They're a core piece of how federated
authorization works in ForgeFed. For more info about OCAPs, see the previous
blog posts.

I'll just say this: Giving permission to access some resource is done in
ForgeFed by sending a Grant activity. That activity can then be used as
authorization when accessing the resource, by specifying the `Grant`'s `id`
URI.

## Beyond Direct Grants

Until now, Vervis allowed working with projects only in the most direct way:

- You couldn't create a whole project in one click
- You could create just a stand-alone **component**, such as a Git repository
  or an issue tracker
- After creation, the component sends you a `Grant` activity, giving you full
  admin access to the component
- You can now specify that Grant's `id` URI in the `capability` field of
  activities that request access/modification of the componet (e.g. change
  settings; close an issue; merge a PR; etc.)

That sort of Grant is what I call a **direct** Grant. It goes straight from the
resource to the person who's being given access.

This might work nicely on a very small scale, but if we want to be serious
and effective about our work, we'd probably eventually face at least
some of these 3 challenges:

1. How do we meaningfully group components into projects? Much like on GitHub,
   GitLab, Gitea, Forgejo etc. a "repository" is actually a multi-component
   unit that contains code, issues, PRs, releases, kanban, wiki, CI, etc. etc.
2. How do we create a flexible way to arrange projects according to the
   organizational structure of our team/company/organization, to make access
   management simple?
3. How do we use OCAPs/Grants effectively to send out all the necessary
   authorizations, especially with the complexity of a federated situation?

Today we're visiting especially 1 and 3. A future blog post (along with the
implementation of course) will touch point 2.

## The Project Actor

Software development components can be collected under **projects**. I've
implemented project creation, viewing and browsing, which is task **V5** on my
task list, in the following commits:

- [Vocabulary](https://codeberg.org/ForgeFed/Vervis/commit/050e8d09bcb939826d0e4a7092a2feaac8db5fbb)
  and
  [DB schema](https://codeberg.org/ForgeFed/Vervis/commit/3db602e3bd08dea1ab70b8b70f00698c0c86a7eb)
- [View handlers and creation UI](https://codeberg.org/ForgeFed/Vervis/commit/372fd35f2c339aa830f7e48b8379a5d47724a3b0)
- [C2S handlers for project creation](https://codeberg.org/ForgeFed/Vervis/commit/9d6bbfdf92cfee1c98d22a1c069eb499e1125ec5)
- [S2S handlers for project creation](https://codeberg.org/ForgeFed/Vervis/commit/224c290b04de5b3101322216ef27241f51dc9d21)
- [S2S project handlers](https://codeberg.org/ForgeFed/Vervis/commit/232a0cd4df7a56f0aa7b6680913e8ef7b864e4ee)
- [HTML page for projects](https://codeberg.org/ForgeFed/Vervis/commit/64aae37b4fe8392c593c46f5224b732ad644bbeb)
- [Project component list view](https://codeberg.org/ForgeFed/Vervis/commit/acc1d13c634c32d0edbd607258ce8244fb26e2f8)

You'll see this stuff in action in the demo below.

## Adding Components to Projects

So, now we can create projects. How do we add components into these projects?
That part has been the bulk of my work in the last few months, because it
involved the implementation of 2 complicated pieces:

1. The latest full OCAP verification process already present in the ForgeFed
   specification, i.e. including support for OCAP chains (so far I've
   implemented only the simple direct mode)
2. The sequence of activity handlers that implement the process of adding a
   component to a project

I've mentioned OCAP delegation before, but let's look at it again, perhaps with
a simple example this time. Given:

- A project *P* and its component *C* which is an issue tracker
- A person *Alice* who has maintainer access to *P*

When Alice wants to close one of the issues under *C*, what sort of token can
she provide, in order to authorize the action? She doesn't have a direct Grant
from *C*, only access to *P*, so how does this work?

The magic is OCAP chains. *C* gives *P* a special Grant that says: *"Hi P! You
can extend this Grant to whoever has access to you, so that they can access me
as well."* And now *P* can extend, or "delegate" this Grant, by sending Alice a
new Grant that *links* to the Grant that *P* got from *C*. So we have a chain
of 2 Grants:

1. *C* gives a Grant to *P*, let's call it *g*
2. *P* gives a Grant to Alice, let's call it *h*

So, when Alice wants to ask *C* to close one of the issues under it, she **uses
Grant *h* as the authorization token**. Since *h* links back to *g*, *C* can
follow the chain of Grants and verify they form a valid delegation of
authority.

Did I succeed at making it sound much simpler than it really is? :)

Now let's look at the sequence of activities required for adding a project to a
component. Here's an overview of one of the possible flows.

Given:

- A project *P*
- A component *C*
- A person with admin access to *C*, Alice
- A person with admin access to *P*, Bob

The process, if initiated by Bob, looks as follows:

1. Bob sends an `Invite` activity, inviting *C* to become a component of *P*
2. *P* approves the initial request and sends an `Accept`
3. Alice, seeing the invite, sends an Accept to approve the operation on the
   component side
4. *C* sees all of this and sends an Accept, thus the operation is now approved
   from both directions
5. *P* sends to *C* a "delegate-Grant", i.e. a Grant that uses the special
   `delegate` role, authorizing *C* to start Grant chains with *P* as the
   target
6. *C* receives the delegate-Grant and uses it as the authorization as it
   starts the Grant chain, sending a start-Grant to *P*
7. *P* now extends this start-Grant as needed, by sending extension-Grants to
   its member people (and teams and parent projects)

I've implemented all of this, including just enough UI for a little demo, as
tasks **S4** and **V8** on my list. The implementation clearly informed many
details in the processes added to the specification (a reminder to the part of
me that is tempted to trust theory alone).

The list of commits for this part is quite long, so if you're looking for the
essence, the **S2S** and **UI** commits are probably the more interesting ones.

- Udates to the specification
  - [Define process of add/remove component to/from project](https://codeberg.org/ForgeFed/ForgeFed/pulls/210)
    (not merged yet, at the time of writing)
- Prepare OCAP system for component-mode
  - [DB: Entities for project-component system](https://codeberg.org/ForgeFed/Vervis/commit/224025b9b6322210a3925373a2f66478af234f42)
  - [DB: Store the 'type' of remote actors](https://codeberg.org/ForgeFed/Vervis/commit/89185164b83d8873dcbbee1a3632dc287d623a8f)
  - [Switch Invite/Join/Remove to use resource collabs URI](https://codeberg.org/ForgeFed/Vervis/commit/b2657589dd0a141cf59d2e7b808971966efc63a0)
  - [Vocab & UI: Repo, Deck and Loom now serve their collabs URI](https://codeberg.org/ForgeFed/Vervis/commit/c98d8d1cc059b8c12c5853a2973d55f3df82b6bd)
  - [C2S: When HTTP GETing an Invite/Remove topic, compare with collabs URI](https://codeberg.org/ForgeFed/Vervis/commit/710bfc27c0719164e72c3b873a29c0f3312135b3)
- Project side
  - [S2S: Project Add handler](https://codeberg.org/ForgeFed/Vervis/commit/6ae079a3108757c22914e18461778a5b605ff308)
  - [UI & Vocab: Project components list & link from collabs JSON to project](https://codeberg.org/ForgeFed/Vervis/commit/1fd46b059059b17364c3cbb2d13165466b2da676)
  - [Vocab: Support project/component in parseInvite, update handlers](https://codeberg.org/ForgeFed/Vervis/commit/1093d4e67d339e309d032ee8a1539653b279c2c6)
  - [S2S, C2S, Client: Update parseRemove to support project+component](https://codeberg.org/ForgeFed/Vervis/commit/043667ed76c5e4fd7ae1f9c2bde6b3fccb5c98db)
  - [Copy topicInvite impl into projectInvite instead of reusing topicInvite](https://codeberg.org/ForgeFed/Vervis/commit/b45aa78d7ba889b81a8a123f9c5bcc05197f2b16)
  - [S2S: topicInvite, projectInvite: If approved, send an Accept](https://codeberg.org/ForgeFed/Vervis/commit/afc45257b456995ea0d017f459bd513d81e1e788)
  - [DB: Make the Accept unique per CollabFulfillsInvite](https://codeberg.org/ForgeFed/Vervis/commit/5e87dd99d38d95ae1cefcde9f30d4dbff163881f)
  - [S2S: Upgrade the Project Invite handler to handle components](https://codeberg.org/ForgeFed/Vervis/commit/4a2f97d9dd3231b305e1e3aaf6d6c2efb5d7e8ca)
  - [Add a ProjectCollabLiveR route for use as Grant revocation URI](https://codeberg.org/ForgeFed/Vervis/commit/afb83b7761f39c0384b6defcbcd2bfb366d244db)
  - [S2S: Copy topicAccept code into projectAccept and reorganize the comment](https://codeberg.org/ForgeFed/Vervis/commit/2920deb900ba445975adcf634919903c50b52278)
  - [S2S: Project Add handler: Rearrange code in preparation for Component mode](https://codeberg.org/ForgeFed/Vervis/commit/aec2235fdc2755cf3b1e16c125a414a17b25a3a0)
  - [S2S: Update Project-Accept handler to handle Components](https://codeberg.org/ForgeFed/Vervis/commit/a083b0d8667371a7c0f11395b2560bfcc5f235c0)
  - [S2S: Project Grant handler](https://codeberg.org/ForgeFed/Vervis/commit/06e5ab9e900fe3cfd1824e7ac5154b191eaffe3b)
- Component side
  - [S2S: Deck Add handler](https://codeberg.org/ForgeFed/Vervis/commit/521eed8bb21403d0da67d417bc23277acbb156eb)
  - [S2S: Deck Invite handler: Implement component mode](https://codeberg.org/ForgeFed/Vervis/commit/e8970c1f4a1f40d564ef32652f99351c0052ee2e)
  - [S2S: Deck Accept handler: Implement component mode](https://codeberg.org/ForgeFed/Vervis/commit/9a78c832331a31e3790e11304c21b43a3cab99e0)
  - [S2S: Implement component delegator-Grant handler](https://codeberg.org/ForgeFed/Vervis/commit/4ac73a9515d9841494e79b12ec61a5c334ec32c3)
  - [S2S: Person Grant handler: Handle component-mode Grants too](https://codeberg.org/ForgeFed/Vervis/commit/fa43a49b1629ff0cc035a8e7a6009296ac68cf6d)
  - [S2S: projectAccept: When adding a Collab, delegate access-to-my-components](https://codeberg.org/ForgeFed/Vervis/commit/21aa4e7c495c2d4185888af0a35e418e81e9cf1b)
  - [C2S: Invite: Support component mode](https://codeberg.org/ForgeFed/Vervis/commit/477793688f982420a7b4c6e6c3dd61e80499f28e)
  - [C2S: Implement Add handler, for adding a component to a project](https://codeberg.org/ForgeFed/Vervis/commit/14ef892032fe8659ce293b45c0aa76a38361547e)
  - [C2S: Implement Accept handler](https://codeberg.org/ForgeFed/Vervis/commit/5d52db937723ec13566631a607b60815de71c808)
  - [UI: Deck: Projects list page](https://codeberg.org/ForgeFed/Vervis/commit/fe6f95d4973ddd19092ba1ca9011ae6bf1cff300)
- Prepare issue/PR tracker handlers for use with OCAP chains
  - [S2S: Deck: Port the Offer{Ticket} handler from the old code](https://codeberg.org/ForgeFed/Vervis/commit/1694d77705880487499439551e14c00f58e2cb56)
  - [S2S: Person: Implement trivial Offer handler](https://codeberg.org/ForgeFed/Vervis/commit/909ba94b49cdc80b9ae7025503c8c3727842cb9d)
  - [S2S: Loom: Port Offer{MR} handler from old federation code](https://codeberg.org/ForgeFed/Vervis/commit/a06003c3616e421b3e6ba8db9870a77c0f5ff671)
  - [C2S: Implement Offer{ticket/MR} handler](https://codeberg.org/ForgeFed/Vervis/commit/be569ab26d486e784502c7b06510cf28810f0cd9)
  - [UI: Use the actor system for opening a ticket, and remove offerTicketC](https://codeberg.org/ForgeFed/Vervis/commit/cb693184f8460cea2aef7f62c9d18fd378715369)
  - [S2S: Port Deck's & Loom's Resolve handlers from the old system](https://codeberg.org/ForgeFed/Vervis/commit/35eb4917a1e725bee949094bd6fe6dc7b1bdf86e)
  - [S2S: Person: Trivial Resolve handler](https://codeberg.org/ForgeFed/Vervis/commit/222ba823c1f591f2c2338adf591f5790b868b264)
  - [C2S, UI: Deck ticket closing button on ticket page](https://codeberg.org/ForgeFed/Vervis/commit/cbd81d1d0b8202ebe3f7a6df0cef9fbc03178391)
  - [C2S: Implement trivial Undo handler, remove old undoC code](https://codeberg.org/ForgeFed/Vervis/commit/3a95e6d3024703da4dcb69d568b4419d1f4f9306)
  - [Client: Port/implement pseudo-client for unresolve-a-ticket](https://codeberg.org/ForgeFed/Vervis/commit/ebe676d94bec708329f8101a2540589e6c4b547c)
  - [UI: Add reopen-this-ticket button to ticket page](https://codeberg.org/ForgeFed/Vervis/commit/91ed2c82b573f0b273d92d9a6bf49cd01c93ac49)
- Upgrade OCAP system, implementing chain verification
  - [Implement OCAP "Verifying an invocation" process from ForgeFed spec](https://codeberg.org/ForgeFed/Vervis/commit/1a3a46b6b2f856410720f7553b4f84985ef8d290)
- UI for OCAP-chained closing-a-ticket
  - [Client: Project UI for adding a component](https://codeberg.org/ForgeFed/Vervis/commit/47f993d63ff1a87ff60071609195ab546f77a88d)
  - [UI: Deck: 'Approve' button for accepting invites-to-projects](https://codeberg.org/ForgeFed/Vervis/commit/df6ece2889e3e4adcbad8eb8f61de56b986610a3)
  - [UI: Add page for publishing a Resolve with custom ticket and OCAP URIs](https://codeberg.org/ForgeFed/Vervis/commit/b420c982c0bcaeb5c5b9befb245e991b754cb6f1)
  - [S2S: Deck: Resolve: Use the full OCAP-authorization algorithm](https://codeberg.org/ForgeFed/Vervis/commit/34386bcf52ad23c4cf1a1ed3b893de1871f4ef2a)

## Teams and Longer Chains

The Grant chain I mentioned is very simple, just 2 Grants in it. Component
sends a Grant to project, then project sends a Grant to Alice. Which might lead
us to ask:

- Is that all? All this complexity just for these 2 grants?
- What about teams and organizations? What about a hierarchy of projects that
  contain other projects? Or decentralized shapes that aren't a tree/pyramid?

So let me clarify: The OCAP verification process can handle chains of any
length, including chains that involve teams and hierarchies of teams and
projects. Vervis itself doesn't yet allow to create these hierarchies (that
belongs to my next tasks, so stay tuned), but the OCAP verification
implementation already supports them. So you'll hopefully see them in action
soon.

Same for teams themselves, even without hierarchies, they (teams) are only
partially implemented, and that's why I haven't included them in the examples.
They, too, are on my todo-list to implement soon as part of my next ForgeFed
milestones.

Gradually, pieces of the puzzle are falling into place.

## Thanks

Huge thanks to my fellow ForgeFed maintainers and developers for their
continued work, including the careful review of my PRs!

Huge thanks to NLNet for funding my work on forge federation! (It's the 2nd
year, and I'm considering to apply again when the time comes!)

## Help Wanted

Perhaps you noticed Vervis has a quite unusable static-HTML UI. A while ago,
[mray](https://codeberg.org/mray) and I started designing a pretty dynamic
client application, and we made big progress with the design. But we stopped
because I can't keep up on the development side.

Do you have passion for forge federation, and for turning software development
into a community activity, where we develop and evolve our own tools, free to
play, express ourselves, solve problems and address human needs, not confined
to conflicting control and interests?

Do you have experience with frontend development, or willingness to learn?

Are you willing to give it a try, and if all goes well, apply for funding (with
our support) to sustain your work?

Come chat with us on
[Matrix](https://matrix.to/#/#general-forgefed:matrix.batsense.net)!

For more technical info about the tech stack etc., check out the
[Anvil repo](https://codeberg.org/Anvil/Anvil).

If you aren't into frontend development, there's still plenty of other things
to do: Backend development, packaging, documentation, illustration, redesigning
of this website, etc. etc.

## See It in Action

I recorded a little demo of all this! [Watch it on my PeerTube
instance](https://tube.towards.vision/w/cKKWhFErFmKN6fZECaoCrP).

If you want to play with things yourself, you can create account(s) on the demo
instances - [fig][], [grape][], [walnut][] - and try the things I've mentioned
and done in the video:

- Creating projects and ticket trackers, opening tickets
- Inviting a tracker to a project and approving the invite
- Resolving a ticket using the form, supplying a custom Grant URI that you can
  find in your inbox or in the project's outbox (or use anything else as the
  Grant URI and verify that it doesn't work :P)

If you encounter any bugs, let me know! Or [open an
issue](https://codeberg.org/ForgeFed/Vervis/issues)

## Comments

We have an account for ForgeFed on the Fediverse:
<https://floss.social/@forgefed>

Right after publishing this post, I'll make a toot there to announce the post,
and you can comment there :)

[kanban]: https://todo.towards.vision/share/lecNDaQoibybOInClIvtXhEIFjChkDpgahQaDlmi/auth?view=kanban
[Vervis]: https://codeberg.org/ForgeFed/Vervis
[fig]: https://fig.fr33domlover.site
[grape]: https://grape.fr33domlover.site
[walnut]: https://walnut.fr33domlover.site
