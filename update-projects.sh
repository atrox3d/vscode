#!/usr/bin/env bash

function syntax(){ echo "syntax: $0 push|pull"; }
function die(){ echo "FATAL";syntax;exit 1; }

[ $# -ge 1 ] || die
ACTION=${1,,}
grep -q $ACTION <<< "push pull" || die

function update()
{
    [ $# -lt 3 ] && RECURSE=0 || ((RECURSE++))
    [ $RECURSE -lt 3 ] || { echo "MAX RECURSION REACHED $RECURSE";echo "RETURN";return; }

    cd "$1"
    echo "cwd=$PWD"
    action=$2

    if [ -d .git ]
    then
        echo "GIT:OK ${action^^}   $1"
        git $action
    else
        shopt -s nullglob
        for d in */
        do
            echo "GIT:KO UPDATE $d RECURSE"
            (update $d $action RECURSE)
        done
    fi
}
export -f update

jq -c '.folders[]|.path' code-workspace.code-workspace | xargs -L1 -I% bash -c "update % $ACTION"