+++
title = "Teams"
date = 2023-12-09
[extra]
author = "Pere Lev"
+++

So far, we've mostly been playing here with Ticket Trackers and Projects. Teams
are now joining the OCAP game as well.

After the words there's a visual demo as well.

Take a look at my [task board][kanban] (and the previous blog posts) for more
context while reading.

## Access Management Overview

The ForgeFed specification and the Vervis implementation have had 2 pieces of
the access management puzzle:

- Adding direct collaborators to resources (such as Ticket Trackers and
  Projects)
- Adding components (such as Ticket Trackers) to Projects

To proceed from there, there are preparation steps:

- Implementing the missing basics for the Team actor
- Implementing adding-direct-collaborators for Teams

The rest of the pieces are:

- Allowing projects to have parents and children
- Allowing teams to have parents and children
- Allowing teams to have access to components
- Allowing teams to have access to projects

This blog post is introducing the 2 **preparation** steps.

## The Team Actor

Software developers can gather in **teams**. Teams have existed in the Vervis
DB schema for a long time, but their old original pre-federation implementation
became irrelevant. I've created an updated, OCAP-ready implementation, which
includes team creation, viewing and browsing, which is task **V4** on my task
list, in the following commits:

- [Vocabulary and View](https://codeberg.org/ForgeFed/Vervis/commit/2797e5f3beda255d40847dd89ea4d9600d029607)
- [C2S handlers for team creation](https://codeberg.org/ForgeFed/Vervis/commit/ea7476db9d1b4ff71767509c335de32f007559a1)
- [S2S handlers for team creation](https://codeberg.org/ForgeFed/Vervis/commit/8d543c001618ae507af485b1d5e3a8c854bcc612)
- [Port basic S2S handlers adapted from Project actors](https://codeberg.org/ForgeFed/Vervis/commit/8584c6387c53759d7a2c378bb37ad9b621026c2b)
- [Team creation UI and additional displays](https://codeberg.org/ForgeFed/Vervis/commit/7517db9619c584d400774cf531777f34aea9b0ba)

You'll see this stuff in action in the demo below.

## Authorized Chain Extensions

With team basics in place, I proceeded to tasks **V6** and **S2**, which are
about adding and removing team members. While examining my control flow
diagrams, I noticed a piece missing, that seemed important to implement first.

When a direct collaborator is added to a component (e.g. a ticket tracker), the
activity flow is simple:

1. An offer is made, to add a new collaborator
2. The component approves the validity of the offer
3. The candidate collaborator accepts the offer
4. The components sends the collaborator a Grant activity

However, for Projects and for Teams, there's an additional part: They need to
be able to send extension Grants to the collaborator. They receive access
privileges from their components/child projects/parent teams, and they need to
be able to forward these privileges to the collaborator.

The additional part was already implemented, but it was missing the
"delegator-Grant" step: A special Grant activity giving the privilege to do the
forwarding mentioned above. I recently added that missing bit to the
specification, and decided it's a good timing to implement it, since Teams are
going to need it as well. I'm calling it "authoried chain extensions", because
the OCAP chain extensions now become authorized via a delegator-Grant, instead
of being sent without context.

Implementing that delegator-Grant piece involved 2 parts:

- Track delegator-Grants on the Project/Team side
- Track the entire OCAP flow on the Person actor side (which I haven't done at
  all until now, because it wasn't needed on the server)

I thus upgraded the OCAP-chain tracking system for Projects and Teams, adding
that delegator-Grant piece, in the following commits:

- DB:
  [here](https://codeberg.org/ForgeFed/Vervis/commit/5d0f707c55f7620d20cad0f382af466eaf0c7f05)
  [here](https://codeberg.org/ForgeFed/Vervis/commit/05d3a1eaefa6154cf3e7472ee00baacfb4bb7fdd),
  and
  [here](https://codeberg.org/ForgeFed/Vervis/commit/b2b4d8778df4e9d87107cdee94422201044a990d)
- S2S:
  [here](https://codeberg.org/ForgeFed/Vervis/commit/88e6818edc2218806b01dfc7dfe22c4625f0c3d5),
  [here](https://codeberg.org/ForgeFed/Vervis/commit/3c0a3d13170cbc61bc6eecffc453a61f44c40d95),
  [here](https://codeberg.org/ForgeFed/Vervis/commit/39dc2089b2df0bdf753458cc4e75a8aed7d3e265),
  [here](https://codeberg.org/ForgeFed/Vervis/commit/11a79b00fbb005ad7533607640a14b667bd46218)
  and
  [here](https://codeberg.org/ForgeFed/Vervis/commit/6dceaa1cffd6c1bc68d60b251f0cc948c085f3fa)
- C2S:
  [here](https://codeberg.org/ForgeFed/Vervis/commit/0c0007c892d1aaa3901124dd8920fad0c779830b),
  [here](https://codeberg.org/ForgeFed/Vervis/commit/442e36dcc15d8003708988bbd7a445a449a305c5)
  and
  [here](https://codeberg.org/ForgeFed/Vervis/commit/12e228438953bfbfaea4da1e1ffec91b6305d024)

## Team Membership

With those pieces in place, I proceeded to implementing the actual Activity
handlers for the Team actor to enable the direct-collaborator flow, which is
how team member addition and removal work behind the scenes. And of course I
added UI for team member addition and removal.

- Specification:
  - The process of adding/removing people to/from teams was documented together
    with the process for Projects, in
    [PR #210](https://codeberg.org/ForgeFed/ForgeFed/pulls/210) which I
    mentioned in the previous blog post (and in the tasks related to it)
  - There's also the new
    [PR #214](https://codeberg.org/ForgeFed/ForgeFed/pulls/214) which adds
    details specific to teams
- [S2S: Team: Implement direct-collaborator flow, adapted from Project](https://codeberg.org/ForgeFed/Vervis/commit/702ad39b961b3a9a45a91f881b171dac83ddcb17)
- [UI: Team: Buttons and form for adding and removing members](https://codeberg.org/ForgeFed/Vervis/commit/5af2fdd58bfb4c0ef0ea08862b9777ad63da180a)
- [UI: Display personal resources using Permit records](https://codeberg.org/ForgeFed/Vervis/commit/119779b9b30650f24756fa9d7c7a29b69da05f3d)
- [UI: For each Permit, display delegator-Grant and extensions](https://codeberg.org/ForgeFed/Vervis/commit/e65563cd19c124275317143fc11ce966118ee719)
- [UI: Dashboard: Display personal invites](https://codeberg.org/ForgeFed/Vervis/commit/ce1e542401f5ac7760ce9633fd475ac13513f15d)
- [UI: Dashboard: Add 'Accept' button to invites you haven't yet accepted](https://codeberg.org/ForgeFed/Vervis/commit/ee91a6403e4249391ca01fd61ae9f010b3813e6b)

## See It in Action

I recorded a little demo of all this! [Watch it on my PeerTube
instance](https://tube.towards.vision/w/rUkqwQ8aLRnZutzgGjPzyd).

If you want to play with things yourself, you can create account(s) on the demo
instances - [fig][], [grape][], [walnut][] - and try the things I've mentioned
and done in the video:

- Creating teams
- Inviting a collaborator
- Accepting the invite
- As the new collaborator, using the access granted by the team (which right
  now is limited to adding (or removing) more collaborators, until more pieces
  of the system are implemented in the next tasks)

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
