#!/usr/bin/env bash

# echo $0 $BASH_SOURCE $PWD
# exit
exec &> >(tee "update.log")


function syntax(){ echo "syntax: $0 push|pull"; }
# export -f syntax
function die(){ echo "FATAL ${@}";syntax;echo "[DIE] exit 255";exit 255; }
# export -f die

[ $# -ge 1 ] || die
ACTION=${1,,}
grep -q $ACTION <<< "push pull" || die

[ "${2^^}" == "STOP" ] && STOP=true || STOP=false

IGNORE_PATHS='__pycache__ venv .idea'
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
        echo "[GIT:OK][RECURSE ($RECURSE)][${action^^}] $1"
        git $action
        [ $? -eq 0 ] || { echo "git errorlevel $? - return 255";return 255; }
    else
        shopt -s nullglob
        for d in */
        do
            echo "[GIT:KO][UPDATE RECURSE ($RECURSE)]"
            echo "[PATH] $d"
            (update $d $action RECURSE)
            [ $? -eq 0 ] || { echo "update errorlevel $? - return 255";return 255; }
        done
    fi
    echo
}
# export -f update

# jq -c '.folders[]|.path' code-workspace.code-workspace | xargs -L1 -I% bash -c "update % ${ACTION} || { echo '[BASH] exit 255';exit 255; }"
# jq -c '.folders[]|.path' code-workspace.code-workspace | xargs -L1 -I% bash -c "update % ${ACTION};echo '[UPDATE] errorlevel $?'"
jq -cr '.folders[]|.path' code-workspace.code-workspace | tr -d '\r' | while read d
do
    echo $d
    (update $d $ACTION)
    exitcode=$?
    # echo exitcode=$exitcode
    if $STOP
    then
        [ $exitcode -eq 0 ] || read -p 'enter to continue, ctrl-c to stop' </dev/tty
    fi
done
