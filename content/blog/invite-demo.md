+++
title = "Federated Invites in Vervis"
date = 2023-06-19
[extra]
author = "Pere Lev"
+++

Vervis has already had for a while the ability to add collaborators to
resources (repos, issue trackers, PR trackers). However:

- There's been no visible UI for it
- There's been only one role: Admin
- Due to the actor refactoring, all federation code has needed porting to the
  new actor system, otherwise it wouldn't work anymore
- There's been no way to remove collaborators, only to add them

What I've now done:

- Defined a
  [set of standard roles](https://codeberg.org/ForgeFed/ForgeFed/pulls/201)
  in the specification (in collaboration with several people giving feedback
  and review <3)
- Ported issue tracker federation handlers:
  - [Accept-Reject](https://codeberg.org/ForgeFed/Vervis/commit/9955a3c0ad7f459b1579e1a2fe61c6cb663a9a7c)
  - [Invite](https://codeberg.org/ForgeFed/Vervis/commit/85f77fcac47b1fbedfabe7f87d9383c92a5deef5)
  - [Join](https://codeberg.org/ForgeFed/Vervis/commit/59e99f405adc862d253e7da819cadeaf29b380c7)
- [Switched the entire actor system to converged
  handlers](https://codeberg.org/ForgeFed/Vervis/commit/d33f272ede92e5f526e793e1e0c02d8fff3e41f5),
  i.e. the same code handles both local and remote activities, which should
  greatly simplify things from now on
- [Ported the C2S Invite handler to the new actor
  system](https://codeberg.org/ForgeFed/Vervis/commit/ffb5dadac7310a58aa0c0889192e75accf3767dc)
  and
  [wrote a C2S Remove handler](https://codeberg.org/ForgeFed/Vervis/commit/9673887479908451e5ca7a57a8254f1ba7a60bbc)
- [Wrote S2S handlers for Remove](https://codeberg.org/ForgeFed/Vervis/commit/7b64ab56b17cc187cfcdbdbbf8a9024b93a98197)
- Add UI for issue trackers:
  - [Publishing an Invite](https://codeberg.org/ForgeFed/Vervis/commit/aaa92d8141c8755e1262074313c091a919acddee)
  - [Publishing a Remove](https://codeberg.org/ForgeFed/Vervis/commit/58518811e38012bff6eaa106f38621cc9ac673d9)
  - [Add](https://codeberg.org/ForgeFed/Vervis/commit/928ad8f9a94eb71061138f97124a13e021a9d282)
    and
    [Remove](https://codeberg.org/ForgeFed/Vervis/commit/c8c2106eabe69a3e1a99fc92493df44a9625a5be)
    a new collaborator
- [Implement support for the 6 roles](https://codeberg.org/ForgeFed/Vervis/commit/581838e5503da740b2944d61d06f794bdf862c51)

Caveats:

- This UI is still a temporary low-usability UI, to be replaced by
  [Anvil](https://codeberg.org/Anvil/Anvil) in the future
- Due to that, since there's no real dynamic client app yet, there's no easy
  way to accept invites; I'm not implementing UI for that because it's really a
  frontend feature, but I'll try to find an easy way to add it to the current
  UI to allow for easier testing/debugging
- However, accepting Invites is fully implemented, both in C2S and in S2S
  federation, and I hope soon you can see the whole thing in action

How to see invites in action:

1. If you want to play with things, create accounts on the demo instances
   ([fig][], [grape][], [walnut][]). If you just want to browse, no account is
   needed, and you can take a loot at the
   [demo tracker](https://fig.fr33domlover.site/decks/mbWob) I just created
2. Once you're logged in, the homepage has a *Create a new ticket tracker*
   link, use it to create a tracker
3. The homepage now lists the tracker, with the Admin role, which you've been
   automatically given
4. The newly created tracker has a *Outbox* link where you can see its
   activities; One of them is a the `Grant` activity that gives you Admin
   access - it's the "capability" you use when performing actions on the
   tracker such as closing or reopening issues
5. You should also see a bell icon at the top left, with 2 new notifications:
   One is the *Grant*, the other is the tracker accepting your
   (automatically-sent) Follow
6. The tracker also has a *collaborators* link, where you're the only one
   listed
7. You can try removing yourself, you'll get a message saying you can't remove
   yourself
8. The tracker also has a *Invite* link where you can add a collaborator; this
   will work only if *you* have the Admin role in the tracker
9. The homepage has an *Invite someone to a resource* link, which allows to add
   remote collaborators by their actor UI, to local or even remote resources
   (such as an issue/ticket tracker) by specifying their URI; This also
   requires to paste the URI of that `Grant` activity we saw in the tracker's
   outbox

Among those 6 standard roles, perhaps the 2 least-access ones deserve some
explanation. These roles are:

- `visit`: Provides read-only access, even commenting isn't possible
- `report`: Provides the basic operations normally allowed without being
  explicitly added to a project, e.g. opening issues and PRs

Why do these roles exist?

- For projects with regular public visibility (the only kind of visibility
  currently implemented in Vervis), operations requiring `visit` or `report`
  roles indeed don't need a capability to be specified, in other words you're
  "implicitly" granted these roles merely by being a registered user
- For resources that are meant to be used just for a defined team and not the
  wider global community, or for resources suffering from spam/abuse, the
  visibility level can be swiched from "public" to "closed": It means everyone
  still implicitly gets the `visit` role, but doing `report`-level operations
  requires explicit permission
- Finally, projects can switch to `private` mode, in which even viewing
  requires explicit permission (e.g. for sensitive content such as keys,
  passwords, personal information, moderation action reports, etc.)

[fig]: https://fig.fr33domlover.site
[grape]: https://grape.fr33domlover.site
[walnut]: https://walnut.fr33domlover.site
