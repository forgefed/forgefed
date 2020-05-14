# Specification (20 subtasks)

The following subtasks involve research and writing of the technical
specification.

- **(S1)** C2S for the features already documented: a section of the
  specification dedicated to the Client-to-Server protocol (C2S), with
  description how commenting and how opening a ticket would be done in C2S.

- **(S2)** Opening a merge request or patch: specification sections explaining
  how a merge request and a patch would be created across servers.

- **(S3)** Following, addressing, verified inbox forwarding: specification
  sections defining the process of following forge-related objects and actors;
  the required or recommended recipients for the various activities; a
  mechanism for verified ActivityPub inbox forwarding.

- **(S4)** Ticket dependencies: specification sections defining the process and
  federation of creating ticket dependencies, hosting, and deleting them.

- **(S5)** Ticket updates and flow: specification sections defining how
  modifications of tickets are made, communicated and federated.

- **(S6)** Merge requests and patches updates/flow: specification sections
  defining how modifications of patches and Merge Requests are made,
  communicated and federated, including new versions and including code review.

- **(S7)** UI translation: specification sections defining how software user
  interface localization management services (such as Weblate) would be
  represented and interacted with in a federated manner, and how they would
  interact with other forge objects, such as repositories and tickets.

- **(S8)** VCS remote push: specification sections defining how users’ SSH keys
  would be uploaded, represented and published, and the process of announcing
  the pushing of commits to remotely-hosted repositories (i.e. ones hosted on
  different servers than the user’s home instance) in a verifiable way.

- **(S9)** Wiki: specification sections defining how wikis and pages would be
  created, modified and deleted, and how wikis are integrated with other
  project tools (eg. repository or tickets). This feature should integrate
  XWiki if possible, since they are working on wiki federation.

- **(S10)** Search, discovery, WebFinger, instance exploration: specification
  sections defining how search and discovery of projects across the federated
  network would work, whether/how the different types of actors would be
  represented in WebFinger, and a representation of the public projects and
  content that a server hosts.

- **(S11)** Teams, groups, roles, access control: specification sections
  defining how federated teams and groups would be created and modified, how
  roles would be assigned to members, and how access controls would be defined,
  enforced and announced.

- **(S12)** CI, CD: specification sections defining how Continuous Integration
  and Deployment services would communicate and interact with repositories.

- **(S13)** Releases, packaging, package repos: specification sections defining
  how packaged releases of repository content or content derived from it would
  be created, published and manipulated, and linked with automatic CI builds.

- **(S14)** Kanban: specification sections defining how kanbans and their
  contents would be created, managed and federated.

- **(S15)** Forks, stars, software specific vocabulary for repos: specification
  sections defining how repositories could provide properties such as license,
  programming language, dependencies, etc., and how forking and starring of
  repositories is done, represented and communicated.

- **(S16)** Verifiable builds: specification sections defining how software
  builds would provide build recipes and hashes of the results to allow for
  verifiable reproducible builds.

- **(S17)** OCAPs: specification defining how Object Capabilities would be used
  for authorization and access control in forges.

- **(S18)** GPG key publishing and commit/tag signature verification:
  specification sections defining how a user’s personal GPG keys would be
  uploaded, published, used for verifying cryptographic signatures on commits
  and tags within repositories, and used for signing other kinds of objects
  such as tickets.

- **(S19)** VCS specifics: specification defining the aspects of ForgeFed
  specific or unique to each version control system, in particular Git and
  Darcs, and how to use ForgeFed with these version control systems. If there’s
  interest and feedback from the community, add Mercurial and/or SVN as well.

- **(S20)** Migration/Import: specification defining how to migrate (or
  “import”) a project from one instance to another including tickets, patches,
  wikis, and every other objects pertaining to the project. Migrations will
  allow complete “forks” of projects, and eliminate vendor lock-in.

# Pagure (15 subtasks)

The following subtasks are software development work which gradually implements
federation in [Pagure](https://pagure.io/pagure).

- **(P1)** Representation of ActivityPub actors for users, groups and
  repositories: users, groups and repositories have JSON-LD representations
  according to the specification, along with HTTP Signature keys for use when
  signing activities.

- **(P2)** Async delivery system: delivery of ActivityPub activities happens
  asynchronously in the background, and failed deliveries are automatically
  retried.

- **(P3)** Discoverability of instances via NodeInfo/ServiceInfo and the
  fediverse server discovery websites: implementation of NodeInfo/ServiceInfo
  and other requirements for allowing Pagure instances to be crawled by
  fediverse discovery websites like fediverse.party, fediverse.space,
  the-federation.info.

- **(P4)** Federated discussion, threads and comments: via ActivityPub S2S,
  allow tickets and merge requests to receive comments from users of remote
  ForgeFed servers, and also support discussion of remote issues and merge
  requests.

- **(P5)** Opening and closing a ticket: via ActivityPub S2S, allow repository
  issues to be opened and closed by users of remote ForgeFed instances, and
  allow opening and closing of remote issues.

- **(P6)** Opening and closing a MR/patch: via ActivityPub S2S, allow merge
  requests to be opened and closed by users of remote ForgeFed instances, and
  allow opening and closing remote merge requests.

- **(P7)** Following, addressing, inbox forwarding: users and repos can be
  followed by remote users; users can follow remote users and repos; Pagure
  performs ActivityPub inbox forwarding when expected to do so by other
  ForgeFed servers.

- **(P8)** Ticket dependencies: creation, deletion, hosting: issues can be
  depended by remote issues, and can depend on remote issues, implemented
  according to the specification.

- **(P9)** Ticket updates/flow: issues can be modified by remote users, and
  users can modify remote issues, including priority, milestones, labels,
  assigned person.

- **(P10)** MR/patch updates/flow: merge requests can be modified by remote
  users, and users can modify remote merge requests.

- **(P11)** VCS remote push and SSH key publishing: users’ SSH keys are
  published according to the specification; commits can be pushed by local
  users and by users of remote forges who have been given access, and both
  local and remote push events are announced in a verifiable way according to
  the specification.

- **(P12)** Releases, forks and stars: repos can be forked and starred by
  remote users; users can fork and star remote repos; repositories releases are
  announced according to the specification.

- **(P13)** Search, discovery, instance exploration: there are search and
  exploration pages, and they can display both local and remote actors (users,
  repositories).

- **(P14)** Teams, groups, roles, access control: groups can have remote
  members; users can become members of remote groups; roles and access controls
  can be defined and assigned according to the specification.

- **(P15)** OCAPs: Object Capabilities are used according to the specification,
  for authorizing federated access to resource modification and to viewing
  non-public resources.

# Vervis (15 subtasks)

The following subtasks are software development work which continues the
implementation of federation in
[Vervis](https://dev.angeley.es/s/fr33domlover/r/vervis).

- **(V1)** Discoverability of instances via NodeInfo/ServiceInfo and the
  fediverse server discovery websites: implementation of NodeInfo/ServiceInfo
  and other requirements for allowing Vervis instances to be listed by
  fediverse discovery websites like fediverse.party, fediverse.space,
  the-federation.info.

- **(V2)** Opening and closing a ticket: via ActivityPub S2S, allow issues to
  be opened and closed by users of remote ForgeFed instances, and have some UI
  for opening and closing remote issues.

- **(V3)** Opening a MR/patch: via ActivityPub S2S, allow merge requests to be
  opened and closed by users of remote ForgeFed instances, and have some UI for
  opening and closing remote merge requests.

- **(V4)** Ticket dependencies: creation, deletion, hosting: issues can be
  depended by remote issues, and can depend on remote issues, implemented
  according to the specification.

- **(V5)** Ticket updates/flow: issues can be modified by remote users, and
  users can modify remote issues, including priority, milestones, labels,
  assigned person.

- **(V6)** MR/patch updates/flow: merge requests can be modified by remote
  users, and users can modify remote merge requests.

- **(V7)** VCS remote push and SSH key publishing: user SSH keys are published
  according to the specification; commits can be pushed by remote users who
  have been given access, and the push is announced according to the
  specification.

- **(V8)** Releases, forks and stars: repos can be forked and starred by remote
  users; users can fork and star remote repos; repo releases are announced
  according to the specification.

- **(V9)** Wiki: wikis and their contents can be created and manipulated by
  remote users, ideally interoperating with XWiki federation.

- **(V10)** Search, discovery, instance exploration: there are search and
  exploration pages, and they can display both local repos and known remote
  repos.

- **(V11)** Teams, groups, roles, access control: teams can have remote
  members; users can become members of remote teams; roles and access controls
  can be defined and assigned according to the specification.

- **(V12)** OCAPs: Object Capabilities are used according to the specification,
  for authorizing federated access to resource modification and to viewing
  non-public resources.

- **(V13)** GPG key publishing and commit/tag signature verification: user’s
  personal GPG keys can be uploaded, published, and used for verifying
  cryptographic signatures on commits and tags according to the specification.

- **(V14)** Client: development of a dynamic client application that supports
  at least viewing and manipulation of tickets and merge requests, commenting,
  viewing of repos and users, search and exploration, and communicates with the
  Vervis server according to the specification, using ActivityPub C2S, OAuth2
  and vocabulary defined in the specification.

- **(V15)** Migration/Import: development of migration/import function for
  repositories, tickets and other project data according to the specification.

# Documentation (1 subtask)

- **(D1)** Implementation guide: a detailed human-friendly document with
  suggestions, recommendations and code examples, that guides developers in the
  process of implementing ForgeFed in their own applications.
