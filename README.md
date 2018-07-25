# ForgeNet - Work-group for Federated Forge Services

ForgeNet is a federation protocol extending the W3C's [ActivityPub][activity-pub] protocol to provide a uniform server-to-server API for interoperability between networked version control services, with limited Pub/Sub access for messaging and notifications to and from the larger Fediverse. It allows users of any compliant service to interact with other compliant forge services without being a registered user of that foreign service, just as if they were. In this way, users that choose to self-host have the additional benefit/responsibility of being in full control of their own authentication/identity and their own data.

All of the most common user interactions are supported such as: cloning/forking, merge-requests/patches, bug-reports/code-review, subscriptions/favorites with VCS-agnostic and service-agnostic genericity.


## Collaboration

The formal work-group discussions and decision making are conducted on our mailing list, and is limited to members of the work-group. However, the [discussions are publicly readable][mail-archive] via the web. Everyone else is encouraged to participate using the issue trackers and wikis on either of our public repositories on [GitHub][github-issues] or [NotABug][notabug-issues], or by sending email to the [mailing list][mailing-list]. Note that the mailing list is moderated for non-members; so there could be some delay posting it.

The artifacts produced by this work-group are still in the early stages; and there is still much work to do and ample room for discussion. In order to be most widely adopted, we strive to assemble the most diverse and representative discussion group of stake-holders including: users, implementors, and various domain experts. Anyone who is experienced with working on an existing forge or federated "social" service, or who is planning to implement new ones, and anyone with experience in writing technical specification documents, or has UX expertise is encouraged to join the work-group. Just send an email to the [mailing list][mailing-list] stating that you would like to join the work-group and how your experience could complement the project.

Services currently represented in the discussions:

* [GitLab][gitlab]
* [GitTea][gittea]
* [Gogs][gogs]
* [Pagure][pagure]
* [SocialHome][socialhome]
* [sr.ht][srht]
* [Vervis][vervis]


## License

All artifacts produced by this work-group are freely available under the [CC0 1.0 Universal (CC0 1.0) Public Domain Dedication][cc0]. All contributions to the wiki must also be offered freely as such.


[activity-pub]:   https://www.w3.org/TR/activitypub/
[mailing-list]:   mailto://git-federation@framalistes.org
[mail-archive]:   https://framalistes.org/sympa/arc/git-federation
[github-issues]:  https://github.com/git-federation/gitpub/issues
[notabug-issues]: https://notabug.org/peers/forge-net/issues
[cc0]:            https://creativecommons.org/publicdomain/zero/1.0/
[gitlab]:         https://about.gitlab.com/
[gittea]:         https://gitea.io/en-us/
[gogs]:           https://gogs.io/
[pagure]:         https://pagure.io/
[socialhome]:     https://socialhome.network/
[srht]:           https://meta.sr.ht/
[vervis]:         https://dev.angeley.es/s/fr33domlover/p/vervis
