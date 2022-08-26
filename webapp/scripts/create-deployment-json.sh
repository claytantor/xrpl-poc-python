#!/bin/bash

if [[ ! -z "$1" ]]; then
    env="$1"
elif [[ "$CIRCLE_BRANCH" == "main" ]]; then
    env="prd"
elif [[ "$CIRCLE_BRANCH" == "dev" ]]; then
    env="dev"
else
    env="local"
fi

dt_timestamp=$(date +%s)
git_branchname=${CIRCLE_BRANCH:-$(git branch | grep \* | cut -d ' ' -f2)}
git_hash=$(git rev-parse --verify HEAD)

manifest=$(printf '{"env":"%s", "branch":"%s", "commitSha":"%s", "timestamp":"%s"}\n' \
    "$env" "$git_branchname" "$git_hash" "$dt_timestamp")
echo $manifest

mkdir -p ./environment/
echo $manifest > ./environment/deployment.json