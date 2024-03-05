#!/usr/bin/env bash

# echo $0 $BASH_SOURCE $PWD
# exit

function syntax(){ echo "syntax: $0 push|pull"; }
function die(){ echo "FATAL";syntax;exit 1; }

[ $# -ge 1 ] || die
ACTION=${1,,}
grep -q $ACTION <<< "push pull" || die

export IGNORE_PATHS='__pycache__/ venv .idea'
function update()
{
    [ $# -lt 3 ] && RECURSE=0 || ((RECURSE++))
    [ $RECURSE -lt 3 ] || { echo "MAX RECURSION REACHED $RECURSE";echo "RETURN";return; }

    cd "$1"
    echo "+-------------------------------------------------------------------------------"
    echo "[CURRENT DIR]" 
    echo "$PWD"
    echo "+-------------------------------------------------------------------------------"
    # echo "[CHECK] "$(basename $PWD)" in ${IGNORE_PATHS}"
    grep -q "$(basename $PWD)" <<< "${IGNORE_PATHS}" && { echo "[IGNORING] $(basename $PWD)";return; }
    # echo "[CHECK] "$1" in ${IGNORE_PATHS}"
    grep -q "$1" <<< "${IGNORE_PATHS}" && { echo "[IGNORING] $(basename $PWD)";return; }
    
    action=$2

    if [ -d .git ]
    then
        echo "[GIT:OK][${action^^}] $1"
        git $action
    else
        shopt -s nullglob
        for d in */
        do
            echo "[GIT:KO][UPDATE RECURSE ($RECURSE)]"
            echo "[PATH] $d"
            (update $d $action RECURSE)
        done
    fi
    echo
}
export -f update

jq -c '.folders[]|.path' code-workspace.code-workspace | xargs -L1 -I% bash -c "update % $ACTION"
