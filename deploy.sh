#!/bin/bash

[ -z "${BOT_TOKEN}" ] && { echo "no token detected"; exit 1; }

git clone https://${BOT_TOKEN}@codeberg.org/ForgeFed/pages.git /tmp/pages
rm -fr /tmp/pages/*
cp -rva html/* /tmp/pages
cd /tmp/pages
cat > .domains <<EOF
forgefed.org
www.forgefed.org
EOF
git add .
if git diff --staged --exit-code >& /dev/null ; then
    echo No changes to push
else
    git config user.email forgefedbot@forgefed.org
    git config user.name 'ForgeFedBot'
    git commit -m 'Update from deploy.sh'
    git push -u origin main
fi
