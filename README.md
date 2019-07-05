# ForgeFed: federating Git services

ForgeFed (formerly GitPub) is a decentralized federation protocol based on the W3C's [ActivityPub][ActivityPub], which
extends [ActivityStream 2.0][ActivityStream2]. It provides a server to server API for pull request,
forking and subscription of repositories provided by Git web services (services like GitHub, GitLab, 
Gogs, Gitea).

[ActivityPub]: https://www.w3.org/TR/activitypub/
[ActivityStream2]: https://www.w3.org/TR/activitystreams-core/

## Updates

### ForgeFed Community Forum

In order to consolidate development and community discussions, there is now a **public web forum** on the socialhub.network website. That forum is the home to ActvityPub and several projects that use ActvityPub as their federation protocol; and so it is a natural fit for ForgeFed. Everyone is invited to use that forum instead of this GitHub repo or the mailing list.

Thanks to SocialHub and FeNeAs for making that possible.

Web Forum: https://socialhub.network/c/forgefed

### ForgeFed in the Fediverse

There is also a user on the Mastodon network to which fediverse users can subscribe for progress updates. Feel free to interact with that actor or use hashtag: #ForgeFed on the Mastodon network.

Fediverse: `@forgefed@floss.social` (https://floss.social/@forgefed)

### ForgeFed Repository

This GitHub repo has not been updated in some time, and it is unclear at the moment whether or not @yookoala still wants to maintain it. The NotABug repo contains the most recent documentation and reference source code, all currently under the maximally permissive CC0 license.

Repository: https://notabug.org/peers/forgefed

## Collaboration

A specification like this must be agreed upon by at least some of Git web service implementations.
If you are a developer of such a software, please [join our discussion][work-group-discussion] and speak up.
We'll simply add you to the work group.

If you are experienced in writing specifications, you're also welcome to join the effort.

## Mailing List

We're still waiting for all the tentative work group members to join the mailing list.

All major discussion and decision making will happen in our Framalistes
[mailing list][mailing-list-archive].
Non-members may use the GitHub issue tracker or send us a mail at:
[git-federation@framalistes.org][mailing-list-address].
We can not guarantee to read all mail or GitHub comments; but we will try.

## License

The specification documents are licensed under a variation of the [W3C Document License][w3c-document-license]. 
You may obtain a copy of the document license [here](LICENSES/DOCUMENT_LICENSE.md). The code
components in this specification are licensed under the MIT License. You may obtain a copy of the
license [here](LICENSE/SOFTWARE_LICENSE.md).

[w3c-document-license]: https://www.w3.org/Consortium/Legal/2015/doc-license
[work-group-discussion]: https://github.com/forgefed/forgefed/issues/5
[mailing-list-archive]: https://framalistes.org/sympa/arc/git-federation
[mailing-list-address]: mailto://git-federation@framalistes.org
