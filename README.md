# GitPub: federating Git services

GitPub is a decentralized federation protocol based on the W3C's [ActivityPub][ActivityPub], which
extends [ActivityStream 2.0][ActivityStream2]. It provides a server to server API for pull request,
forking and subscription of repositories provided by Git web services (services like Github, Gitlab, 
Gogs, Gitea).

[ActivityPub]: https://www.w3.org/TR/activitypub/
[ActivityStream2]: https://www.w3.org/TR/activitystreams-core/

## Collaboration

A specification like this must be agreed upon by at least some of Git web service implementations. If you are a developer of such a software, please [open an issue][issue-tracker]. We'll simply add you as a collaborator.

If you are experienced in writing specifications, you're also welcomed to join the effort.

## License

The specification documents are licensed to a variation of [W3C Document License][w3c-document-license]. 
You may obtain a copy of the document license [here](LICENSES/DOCUMENT_LICENSE.md). The code
components in this specification are licensed to MIT License. You may obtain a copy of the
license [here](LICENSE/SOFTWARE_LICENSE.md).

[w3c-document-license]: https://www.w3.org/Consortium/Legal/2015/doc-license
[issue-tracker]: https://github.com/git-federation/gitpub/issues