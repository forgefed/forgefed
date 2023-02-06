# ForgeFed

<a href="https://codeberg.org/ForgeFed/ForgeFed">
    <img alt="Get it on Codeberg" src="https://codeberg.org/Codeberg/GetItOnCodeberg/media/branch/main/get-it-on-neon-blue.png" height="60">
</a>

ForgeFed is an ActivityPub-based federation protocol for software forges. You
can read more about ForgeFed and the protocol specification on our
[website][Website].

## Contributing

There's a huge variety of tasks to do! Come talk with us on the [forum][] or
[chat][]. More eyes going over the spec are always welcome! And feel free to
open an issue if you notice missing details or unclear text or have improvement
suggestions or requests.

However, to maintain a manageable working environment, we do reserve the issue
tracker for *practical, actionable work items*. If you want to talk first to
achieve more clarity, we prefer you write to us on the [forum][] or [chat][], and
opening an issue may come later.

If you wish to join the work on the ForgeFed specification, here are some
technical but important details:

- We don't push commits to the main branch, we always open a pull request
- Pull requests making changes to the specification content must have at least
  2 reviews and then they wait for a cooldown period of 2 weeks during which
  more people can provide feedback, raise challenges and conflicts, improve the
  proposed changes etc.
- If you wish to continuously participate in shaping the specification, it
  would be useful to go over the open PRs once a week or so, to make sure you
  have a chance to communicate your needs, ideas and thoughts before changes
  get merged into the spec

Important files in this repo to know about:

- The file `resources.md` lists which team members have access to which project
  resources, openness and transparency are important to us!
- The actual specification source texts are in the `spec/` directory
- JSON-LD context files are in the `rdf/` directory

## Repo mirrors

* [ForgeFed on Notabug][Notabug]
* [ForgeFed on Pagure][Pagure]
* [ForgeFed on GitHub][GitHub]

## Website build instructions

The ForgeFed website is generated via a script using the Markdown files in this
repository. See `./build.sh` for more details.

## License

All contents of this repository are are freely available under the
[CC0 1.0 Universal (CC0 1.0) Public Domain Dedication][cc0].

The ForgeFed logo was created by [iko][].

## Historical resources

ForgeFed started its life on a [mailing list][Mailing-list]. The old ForgeFed forum at
talk.feneas.org can be viewed via the Internet Archive's
[Wayback Machine][Old-forum].

[Website]: https://forgefed.org
[Forum]:   https://socialhub.activitypub.rocks/c/software/forgefed
[Chat]:    https://matrix.to/#/#forgefed:libera.chat

[Notabug]: https://notabug.org/peers/forgefed/
[Pagure]:  https://pagure.io/forge-fed/forge-fed
[Github]:  https://github.com/forgefed/forgefed

[Mailing-list]: https://framalistes.org/sympa/arc/git-federation
[Old-forum]:    https://web.archive.org/web/20210306224235/https://talk.feneas.org/c/forgefed/10

[cc0]: https://creativecommons.org/publicdomain/zero/1.0/
[iko]: https://iko.im/
