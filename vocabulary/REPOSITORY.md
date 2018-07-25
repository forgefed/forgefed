Class: Repository
    descritpion: represents a repository (git, darcs, mercurial, ...)

Properties:
    name
    location
    owner: URL to an user (actor)

Actions:
    push: notify the federation network on new content push
    delete