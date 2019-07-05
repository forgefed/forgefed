#!/bin/bash

inputs="forgefed forgefed-vocabulary"

git_branch=`git rev-parse --abbrev-ref HEAD`

git_commit_id=`git rev-parse HEAD`

git_commit_id_short=`git rev-parse --short HEAD`

now=`date --utc +%Y-%m-%d`

dirty () {
    git diff-index --quiet HEAD --
}

render () {
    dir="$1"
    file="$2"

    if [ "$3" == "true" ]; then
        toc="--table-of-contents"
    else
        toc=""
    fi

    dirty
    if [ $? -eq 0 ]; then
        gitdirty=""
    else
        gitdirty="--variable gitdirty"
    fi

    pandoc $dir/$file.md \
        --from markdown \
        --to html \
        --template html/template.html \
        $toc \
        $gitdirty \
        --variable "gitbranch:$git_branch" \
        --variable "gitcommitid:$git_commit_id" \
        --variable "gitcommitidshort:$git_commit_id_short" \
        --variable "date:$now" \
        --number-sections \
        --output html/$file.html
}

render html index "false"

for file in $inputs; do
    render specification $file "true"
done
