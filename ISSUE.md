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