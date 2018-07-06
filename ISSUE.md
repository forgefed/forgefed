What information is kept about issues? When creating an issue, what info can be provided?

Gitea: https://github.com/go-gitea/gitea/blob/master/models/issue.go#L26

GitLab: <https://gitlab.com/gitlab-org/gitlab-ce/blob/master/db/schema.rb>

Vervis: <https://dev.angeley.es/s/fr33domlover/r/vervis/s/config/models>

----

Class: Issue
    description: Represent an issue for a specific repository

Properties:
    repository: a URI to an existing repository
    number: the issue number, in the context of a repository (#1, #2, ...)
    author: a URI to the user who created the issue
    title: title of the issue
    content: text of the issue
    creationDate:

Action (for federation):
    Create
    Update
    Delete

---

Here's a suggestion/example for a JSON-LD newly created issue sent between
servers as a notification. It's not a canonical instruction yet, just an aid
for now, to get an idea of what it may look like.

    {
      "@context": [
          "https://www.w3.org/ns/activitystreams",
          { "rfv": "https://peers.community/ns/repo-fed-vocab#"
          }
        ],
      "type": "Create",
      "id": "https://notabug.org/fr33domlover/posts/595c1fd3-a0db-415c-a059-bf7ae99ecd3f",
      "to": "https://notabug.org/zPlus/freepost",
      "actor": "https://notabug.org/fr33domlover",
      "object": {
          "type": "rfv:Note",
          "id": "https://notabug.org/zPlus/freepost/issues/217",
          "attributedTo": "https://notabug.org/fr33domlover",
          "to": "https://notabug.org/zPlus/freepost",
          "rfv:tracker": "https://notabug.org/zPlus/freepost",
          "rfv:issue-number": 217,
          "rfv:title": "Implement ActivityPub federation",
          "rfv:description": "What if Freepost becomes an AP server?",
          "rfv:creation-time": "2018-07-06 14:28:57"
        }
    }
