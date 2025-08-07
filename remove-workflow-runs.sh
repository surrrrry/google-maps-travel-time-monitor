#!/usr/bin/env bash

# remove upto 1000 workflow runs
# borrowed from https://blog.oddbit.com/post/2022-09-22-delete-workflow-runs/
gh run list -L 1000 --json databaseId  -q '.[].databaseId' |
  xargs -IID gh api \
    "repos/$(gh repo view --json nameWithOwner -q .nameWithOwner)/actions/runs/ID" \
    -X DELETE
