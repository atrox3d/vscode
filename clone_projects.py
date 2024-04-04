import json

from common import get_gitrepos
from vscode_workspace import VsCodeWorkspace
import update_options as options

def clone(workspace_path: str, recurse: bool) -> dict:
    ws = VsCodeWorkspace(workspace_path)
    clone = {}
    for repo in get_gitrepos(ws, recurse=recurse):
        if repo.remote is not None:
            print(f'ADDING | {repo.path}')
            clone[repo.path] = repo.remote
        else:
            print(f'NO REMOTE | skipping | {repo.path}')
    
    return clone

def save(clone: dict, json_path: str):
    with open(json_path, 'w') as fp:
        json.dump(clone, fp, indent=2)

def load(json_path: str):
    with open(json_path) as fp:
        clone = json.load(fp)
    return clone


def main():
    # import argparse
    # parser = options.get_parser()
    # args: argparse.Namespace = parser.parse_args()

    # if args.all:
    #     recurse = auto_commit = pull_enabled = push_enabled = True
    # else:
    #     recurse = args.recurse
    #     auto_commit = args.commit is not None
    #     push_enabled = args.push
    #     pull_enabled = args.pull

    # dry_run = args.dryrun
    # commit_message = 'automatic update' if args.commit is None else args.commit

    # for k, v in vars(args).items():
    #     print(f'PARAM  | {k} = {v}')

    recurse = True
    json_path = 'clone.json'
    workspace_path = 'code-workspace.code-workspace'

    cloned = clone(workspace_path, recurse)
    save(cloned, json_path)

    cloned = load(json_path)
    print(json.dumps(cloned, indent=2))

