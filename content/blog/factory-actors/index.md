+++
title = "Actor Factory"
date = 2024-08-11
[extra]
author = "Pere Lev"
+++

Until now, publishing a new resource, whether it's a comment or a project, has
been happening only locally, on the user's home server. It means that whoever
wanted to implement a ForgeFed-federated forge, would need to host the
implementations of all actor/resource/service types on one domain name, acting
as a big all-in-one forge.

This is no longer the case! And that's what this post is about. Actor creation
is obviously a part of the core of ForgeFed's API, so I decided it's time to
take care of this upgrade :)

As always, my [task board][kanban] is available.

## Federated Actions

Every request sent on the federated network is an interaction between two or
more actors. Some of these requests can occur between actors of different
servers, and some can't.

Examples of federation-supporting requests:

- Follow an (possibly remote) actor
- Open an issue (possibly on a remote issue tracker)
- Add a repository to a project (both of which might be on different servers)

Examples of requests that don't support federation, or weren't until now:

- Create a user account (this happens between your client/browser and your home
  instance of choice)
- Editing admin settings of other instances
- **Creating a project**

Until now, creating a new actor (project, ticket tracker, etc.) was limited to
your home instance, i.e. the actor is launched on the same instance where your
account is.

On one hand, it makes sense: Why would other servers allow you to create
projects on them?

On the other hand:

- It's an artificial limitation, i.e. this action could easily support
  federation
- It blocks the possibility of implementing micro-services that live on
  different domains, where each service specializes in a specific type(s) of
  actor
- It blocks the possibility of distributed teams to allow all their members to
  create resources on the team's main instance

## Factory Actor

So, shall we make actor creation support federation? That's exactly what I did!

There's a new type of actor (which will find its way to the ForgeFed
specification very soon as well), called **Factory**. The only job of a Factory
is to create resource actors (everything except Person and Factory) on its home
instance.

With that piece in place, *Create* activities are no longer sent into "thin
air", they're sent to a Factory. And the Factory handles creating the actor.
Person actors can no longer launch new projects by themselves.

Since a Factory it a resource actor, it can have its own collaborators and
teams that have access to it, and it implements the Object Capability system,
just like the other actor types. This means a Factory can have remote
collaborators, and remote teams, **thus allowing remote users to create new
actors via the Factory**.

But who factories the factory?

So, Factory is the only actor type that can be created in the "old" way, i.e.
without requiring a Factory. The client/browser sends a client-to-server (C2S)
*Create* activity to the Person's outbox, and the Person actor launches a new
Factory. However, we wouldn't want *any* user to be able to do this. So, in the
Vervis settings file, there's a list of users who are approved for creating new
Factory actors.

Summary of actor creation:

- Person: Created via the registration API (see file `API.md` in the Vervis
  source repo for details)
- Factory: Created via a C2S request to a Person actor, and limited to users
  who are allowed to create factories (normally, the server admins)
- Any other ForgeFed actor type: Created via a Factory

## The Little Details

I needed to figure out certain details before the implementation:

- How to set which actor types the Factory is able to create?
- How to control who is allowed to create Factories, who is allowed to use
  them, who is allowed to change their settings and delete them?
- How to make a Factory automatically serve every new user on *another*
  instance? e.g. so that people on the Person micro-service can create repos on
  the Repository micro-service

These details might get changes and updates, but right now here's how they
work:

- There's a new property `availableActorTypes` which specifies, for a given
  Factory, which types it's allowed to create
- That property is specified when Creating the Factory, and when editing it
- Editing uses a new activity type `Patch` where `object` is the object being
  edited and the other fields are object fields being set to a new value
- The name `Patch` is already use to represent a code patch, but the term
  `Patch` works for both cases because they appear in different situations
- I'd use `Edit` etc. but `Patch` might become standard name on the Fediverse,
  coming from the `PATCH` method of HTTP
- Who can create Factories isn't controlled by the OCAP system, but instead
  using a setting (but it could also be in the DB) that lists admin usernames
- To use a Factory to create actors, you need to have a valid `Grant` for it,
  with the role being at least `write` (a.k.a developer)
- A factory can have both Person collaborators and Teams that have access to
  it, so if a Person micro-service creates a Team containing all users, and
  that Team is given access to the remote Repository-Factory, users can now
  creates repos on the Repository micro-service

## Bonus: Synchronized Push

In web apps there's often a single big database, and concurrent access to it is
managed using atomic isolated transactions. Actor programming brings a new
approach: Each actor has its own database, its own data. Since actors handle
messages one by one, there's no concurrent access, and transactions happen on
the actor level rather than database level.

But that beautiful model works only when the actor has exclusive access to its
data and database! And that's exactly a problem Vervis had until now:

- When a human asks to merge a PR by sending an activity to the Repository
  actor's inbox, the Repository actor handles the merge
- When a human pushes commits via SSH, the SSH server component of Vervis
  handles push by directly accessing the repo, without consulting the
  Repository actor

Thus, we have 2 components that possibly concurrently access the repo! There's
no risk of corruption, thanks to Git locking concurrent access, but there's
difficulty for Repository actor handlers to be atomic, because whenever they
touch the actual Git repo, there's a chance a git-push will concurrently happen
and modify the repo.

To fix that,

- I made a much-needed upgrade to the actor system (which is going to be the
  same system that ForgeFed-v2 a.k.a OcapForge a.k.a Forgely a.k.a
  insert-better-name-here will be using!), allowing each actor type to define
  its own set of methods
- I added a method to the `Repository` actor, that simply asks it to wait while
  the SSH server handles a git-push

So technically, the Repository actor doesn't have exclusive write access to the
repo. But whenever a push happens, it now goes through the actor message queue,
which means no concurrent access anymore, and Repository actor message handlers
can now be truly atomic, and easier to implement, knowing no surprising changes
will suddenly appear.

## Implementation

- Factory Actor
  - [Add a new actor type: Factory](https://codeberg.org/ForgeFed/Vervis/commit/66870458b704d3959da11eeb237b8276786238f5)
  - [Switch to factory-based creation of Deck, Project and Group](https://codeberg.org/ForgeFed/Vervis/commit/e196ee6f3460c0c4ab063b2df030ec745f2b83f1)
  - [DB, S2S: Factory: Record set of allowed types](https://codeberg.org/ForgeFed/Vervis/commit/df4a2b221e82c4b19b4e94929a24d643e88ee42d)
  - [S2S: Factory: Implement collaborators and teams](https://codeberg.org/ForgeFed/Vervis/commit/b74d0d46c4dd9ac15b62de526874b8a848a0987e)
  - [UI, C2S, S2S: Factory: Make allowed types editable](https://codeberg.org/ForgeFed/Vervis/commit/94762ca76c31e09ea593d919e20b2a731958fca3)
  - [HomeR, NewR: List grants from extensions, not just direct ones](https://codeberg.org/ForgeFed/Vervis/commit/a03968ca0bb1cf4eaa7b29d53539f7b6888e9dd3)
- Synchronized Push
  - [Pass theater to runSsh](https://codeberg.org/ForgeFed/Vervis/commit/cd1bc1aee3d8af403e5b69b57809f78fb0db286b)
  - [Upgrade actor system, now using HList, to allow per-actor method type](https://codeberg.org/ForgeFed/Vervis/commit/ea463703b5805d33622c8745ac0f9c6a6ac22681)
  - [Make push-to-repo SSH events sequential via the Repo actor](https://codeberg.org/ForgeFed/Vervis/commit/a74b24f61a0cb190b199a4dd6907c7078f36f6a9)

## Funding

I really want to thank NLnet for funding this work! The extended grant is
allowing me to continue backend work, and allowing André to work on the
[Anvil][] frontend.

## See It in Action

I recorded a little demo of all this! [Watch it on my PeerTube
instance](https://tube.towards.vision/w/3Nz84fkVMsNHUVsNEvAP8V).

If you want to play with things yourself, you can create account(s) on the demo
instances - [fig][], [grape][], [walnut][] - and try the things I've mentioned
and done in the video.

If you encounter any bugs, let me know! Or [open an
issue](https://codeberg.org/ForgeFed/Vervis/issues)

## Comments

Come chat with us on
[Matrix](https://matrix.to/#/#general-forgefed:matrix.batsense.net)!

And we have an account for ForgeFed on the Fediverse:
<https://floss.social/@forgefed>

Right after publishing this post, I'll make a toot there to announce the post,
and you can comment there :)

[kanban]: https://todo.towards.vision/share/lecNDaQoibybOInClIvtXhEIFjChkDpgahQaDlmi/auth?view=kanban
[Vervis]: https://codeberg.org/ForgeFed/Vervis
[fig]: https://fig.fr33domlover.site
[grape]: https://grape.fr33domlover.site
[walnut]: https://walnut.fr33domlover.site
[Anvil]: https://codeberg.org/Anvil/Anvil
