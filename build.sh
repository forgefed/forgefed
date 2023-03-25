#!/bin/bash

set -e

# Fixes pandoc mangling emojis
export LANG=C.UTF-8

git_branch=`git rev-parse --abbrev-ref HEAD`

git_commit_id=`git rev-parse HEAD`

git_commit_id_short=`git rev-parse --short HEAD`

now=`date --utc +%Y-%m-%d`

dirty () {
    git diff-index --quiet HEAD --
}

runPandoc () {
    local dir="$1"
    local file="$2"

    if [ "$3" == "true" ]; then
        local toc="--table-of-contents --number-sections"
    else
        local toc=""
    fi

    local output="html/$file.html"
    local suffix=".html"

    pandoc $dir/$file.md \
        --from markdown \
        --to html \
        --template html/template.html \
        $toc \
        --variable "gitbranch:$git_branch" \
        --variable "gitcommitid:$git_commit_id" \
        --variable "gitcommitidshort:$git_commit_id_short" \
        --variable "date:$now" \
        --variable "other-theme:$otherTheme" \
        --variable "suffix:$suffix" \
        --output "$output"
        #$gitdirty \
}

render () {
    local dir="$1"
    local file="$2"
    local toc="$3"
    runPandoc $dir $file $toc
}

#dirty
#if [ $? -eq 0 ]; then
#    gitdirty=""
#else
#    gitdirty="--variable gitdirty"
#fi

cp rdf/context.jsonld html/ns

render html index "false"

render html funding-plan "false"

mkdir -p html/spec
bikeshed spec "spec.bs" "html/spec/index.html" \
    --md-text-macro="GITBRANCH $git_branch" \
    --md-text-macro="GITCOMMIT $git_commit_id" \
    --md-text-macro="GITSHORT $git_commit_id_short"
