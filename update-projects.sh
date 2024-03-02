jq -c '.folders[]|.path' code-workspace.code-workspace | xargs -L1 -I% sh -c 'cd %;echo %;git pull'
