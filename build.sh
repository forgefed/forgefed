#!/bin/bash

set -e

git_branch=`git rev-parse --abbrev-ref HEAD`

git_commit_id=`git rev-parse HEAD`

git_commit_id_short=`git rev-parse --short HEAD`

zola build

cp context.jsonld public/ns

mkdir -p public/spec
bikeshed spec "spec.bs" "public/spec/index.html" \
    --md-text-macro="GITBRANCH $git_branch" \
    --md-text-macro="GITCOMMIT $git_commit_id" \
    --md-text-macro="GITSHORT $git_commit_id_short"
