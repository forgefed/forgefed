Class: PullRequest
    description: represents a remote PR object

Properties:
    creationDate
    author
    to: a remote repository to be notified of this new PR

Actions:
    Create
    Delete
    Update: if the PR is updated (new commits), the remote PR should be updated with the new content