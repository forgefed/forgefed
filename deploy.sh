#!/bin/bash

rsync \
    --rsh='ssh -p 1234' \
    --recursive \
    --chown=hakyll:hakyll \
    --compress \
    --delete \
    --verbose \
    html/ \
    hakyll@angeley.es:forgefed
