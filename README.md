# ForgeFed - Federation Protocol for Forge Services

ForgeFed is a federation protocol extending the W3C's [ActivityPub][activity-pub]
protocol to provide a uniform server-to-server API for interoperability across
networked software project management services (aka: forges), with limited
pub/sub access for messaging and notifications to and from the larger fediverse.
It's domain model is maximally generic, as to allow a proliferation of
heterogeneous peers to define their own use-cases, by implementing feature
compatibility selectively.

In plain words, forges can communicate and share project data and metadata
(code, tickets, patches, activity-streams, and so on), regardless of which forge
software is running and which host it is running on. Furthermore, interoperability
is not limited to forges. Dedicated services, implementing any of the project
management tools, commonly offered by forges (version control, code review,
issue trackers, forums, mailing lists, and so on), as well as any custom tools,
can share any of the same project data, which is relevant to that tool.
It allows users of any ForgeFed-compliant service to interact with other
ForgeFed-compliant services, without being a registered user of any foreign service,
just as if they were registered. In this way, people who choose to self-host
services or use custom tools, have the additional benefit/responsibility
of fully controlling of their own authentication/identity and their own data.

All of the most common user interactions are supported such as: cloning/forking,
merge-requests/patches, bug-reports/code-review, subscriptions/favorites with
VCS-agnostic, service-agnostic, and client-agnostic genericity.

You can find the published specification on the [ForgeFed website][website].


## Work-group Collaboration

***UPDATE 2022-05: The following information is due to change soon. For example,
the FeNeAs forum is no longer in service. Attend the next
[online conference][online-conference] if you are interested.***

[online-conference]: https://forum.forgefriends.org/t/forgefed-videoconference-june-13th-2pm-utc/715

The formal work-group and associated development discussions are conducted openly
~~on the [ForgeFed Community Forum][feneas-forum] on the FeNeAs website~~; with
informal, real-time Collaboration often taking place on the #forgefed IRC channel on
the libera.chat network. Everyone is invited to participate in either venue. Before
posting, please read [this primer][overview] for a brief overview of the project
motivation and goals. For a detailed overview of the project motivation and goals,
you could read the archive of the [2018 exploratory discussions][mail-archive].

The artifacts produced by this work-group are still in the early stages; and there
is still much work to do, and ample design-space for discussion and contributions.
In order to be most widely adopted, we strive to assemble the most diverse and
representative group of stake-holders including: users, implementers, and various
domain experts. Anyone who is experienced with working on an existing forge or a
federated "social" service, or who is planning to implement new ones, and anyone
with experience in writing technical specification documents, or has UX expertise
is encouraged to join the work-group and/or contribute artifacts. Please submit
any tangible contributions (artwork, software, documentation) and technical critique
regarding the published artifacts to the [ForgeFed issue tracker][notabug-issues]
and [ForgeFed wiki][notabug-wiki] on NotABug.

- [Working Group](https://talk.feneas.org/t/working-group-instructions/196)
- [Community Group](https://talk.feneas.org/t/monthly-community-review-round-instructions/192)

### The VCS is mirrored on multiple hosts:

* [ForgeFed on Notabug][notabug-repo]
* [ForgeFed on Pagure][pagure-repo]
* [ForgeFed on Codeberg][codeberg-repo]

### Projects participating in the discussions have included:

* [Federated Networks Association][feneas]
* [GitDit][git-dit]
* [GitLab][gitlab]
* [Gitea][gitea]
* [GoFed][go-fed]
* [Gogs][gogs]
* [NotABug][notabug]
* [Pagure][pagure]
* [Peers Community][peers]
* [SocialHome][socialhome]
* [sr.ht][srht]
* [Vervis][vervis]


## ForgeFed on the Fediverse

Connect with [ForgeFed on the fediverse][fediverse] for
progress updates and general tooting.


## Website build instructions

    ./build.sh


## License

All artifacts produced by the ForgeFed work-group are freely available under
the [CC0 1.0 Universal (CC0 1.0) Public Domain Dedication][cc0]. All
contributions to the wiki must also be offered freely as such.

The ForgeFed logo was contributed by Libera IRC user: ['iko'][iko].


[activity-pub]:    https://www.w3.org/TR/activitypub/
[website]:         https://forgefed.org/

[overview]:        https://codeberg.org/ForgeFed/ForgeFed/src/branch/master/doc/README.md
[mail-archive]:    https://framalistes.org/sympa/arc/git-federation

[notabug-repo]:    https://notabug.org/peers/forgefed/
[pagure-repo]:     https://pagure.io/forge-fed/forge-fed
[codeberg-repo]:   https://codeberg.org/ForgeFed/forgefed

[feneas]:          https://feneas.org
[git-dit]:         https://github.com/neithernut/git-dit
[gitlab]:          https://about.gitlab.com/
[gitea]:           https://gitea.io/en-us/
[go-fed]:          http://go-fed.org/
[gogs]:            https://gogs.io/
[notabug]:         https://notabug.org/
[pagure]:          https://pagure.io/
[peers]:           https://peers.community/
[socialhome]:      https://socialhome.network/
[srht]:            https://meta.sr.ht/
[vervis]:          https://dev.angeley.es/s/fr33domlover/r/vervis

[fediverse]:       https://floss.social/@forgefed

[cc0]:             https://creativecommons.org/publicdomain/zero/1.0/
[iko]:             https://iko.im/
