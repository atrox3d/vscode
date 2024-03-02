function update()
{
    if [ $# -lt 2 ]
    then
        RECURSE=0
    else
        ((RECURSE++))
        [ $RECURSE -lt 3 ] || {
            echo "MAX RECURSION REACHED $RECURSE"
            echo "RETURN"
            return
        }
    fi

    cd "$1"
    echo "cwd=$PWD"

    if [ -d .git ]
    then
        echo "GIT:OK PULL   $1"
        git pull
    else
        shopt -s nullglob

        for d in */
        do
            echo "GIT:KO UPDATE $d RECURSE"
            (update $d RECURSE)
        done
    fi
}
export -f update

jq -c '.folders[]|.path' code-workspace.code-workspace | xargs -L1 -I% bash -c 'update %'