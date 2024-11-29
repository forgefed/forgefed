+++
title = "Docker Image"
date = 2024-10-21
[extra]
author = "Pere Lev"
+++

Good news: Vervis now has a Docker build, including a prebuilt image you can
use to deploy a Vervis instance really easily!

I never used Docker before, but I'm happy to say it was really easy to learn.
The biggest challenge I had was the slow process of debugging, as Docker was
rebuilding Vervis again and again from scratch only to find an error near the
end.

The image can be found here: <https://codeberg.org/ForgeFed/Vervis/packages>.

And here are the instructions for using it, in the README:

- [Deployment instructions](https://codeberg.org/ForgeFed/Vervis#deployment)
- [Testing intructions](https://codeberg.org/ForgeFed/Vervis#testing-the-production-image)

To prepare the docker build, the main tasks I had were:

1. Properly organize the Vervis config and state directories
2. Write the `Dockerfile` and `docker-compose.yml` recipes, for which I mostly
   used the official Docker docs and Mastodon's recipes for inspiration
3. Write deployment instructions

Several files in the repo are involved in the deployent setup, but the primary
ones are:

- [Dockerfile](https://codeberg.org/ForgeFed/Vervis/src/branch/main/Dockerfile)
- [docker-compose.yml](https://codeberg.org/ForgeFed/Vervis/src/branch/main/docker-compose.yml)

Here are the commits:

- [Start moving app state to ./state dir](https://codeberg.org/ForgeFed/Vervis/commit/27f1fe2db39019bcca6d188397d025ec315f1b17)
- [Move remaining env/state files into state/ dir](https://codeberg.org/ForgeFed/Vervis/commit/0e2ab56219ee513ee710000fd5eede3738d44077)
- [Initial Dockerfile](https://codeberg.org/ForgeFed/Vervis/commit/d077203b2f461bddaabd121cc5967596f4565d43)
- [Docker: Update Dockerfile & Add docker-compose.yml (still tweaking the setup)](https://codeberg.org/ForgeFed/Vervis/commit/b7b6fd7a2e31eff2fdcd122409e40d0e6a4a436b)
- [Docker: Config volume & State preparation when using docker-compose](https://codeberg.org/ForgeFed/Vervis/commit/d35b26c1c25f75d1c4ffdebc56e4e102a75f408e)
- [README: Revise text](https://codeberg.org/ForgeFed/Vervis/commit/4b113b8a20643d193edd83d501cc9f85cd94c7ac)
- [Docker: Instructions & utils for testing the production image](https://codeberg.org/ForgeFed/Vervis/commit/7057be55aabe6934253d871a2e30798521769ed0)

## See It in Action

I recorded a little demo! [Watch it on my PeerTube
instance](https://tube.towards.vision/w/42xz9DMzFLXJQXdsutEyu2).

If you want to play with things yourself, you can follow the instructions in
the Vervis README, which pull the Docker image and launch a container.

If you encounter any bugs, let me know! Or [open an
issue](https://codeberg.org/ForgeFed/Vervis/issues)

## Funding

I really want to thank NLnet for funding this work! The extended grant is
allowing me to continue backend work, and allowing André to work on the
[Anvil][] frontend.

Oh, and our new grant application has just been accepted! We'll now prepare the
2025 roadmap and finalize it with NLnet, more on that coming soon :)

## Comments

Come chat with us on
[Matrix](https://matrix.to/#/#general-forgefed:matrix.batsense.net)!

And we have an account for ForgeFed on the Fediverse:
<https://floss.social/@forgefed>

Right after publishing this post, I'll make a toot there to announce the post,
and you can comment there :)

[kanban]: https://todo.towards.vision/share/lecNDaQoibybOInClIvtXhEIFjChkDpgahQaDlmi/auth?view=kanban
[Vervis]: https://codeberg.org/ForgeFed/Vervis
[fig]: https://fig.fr33domlover.site
[grape]: https://grape.fr33domlover.site
[walnut]: https://walnut.fr33domlover.site
[Anvil]: https://codeberg.org/Anvil/Anvil
