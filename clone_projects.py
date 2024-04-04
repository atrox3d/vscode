import json
from pathlib import Path

from common import get_gitrepos
from vscode_workspace import VsCodeWorkspace
# import update_options as options
from atrox3d.simplegit import git


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
    print(f'SAVING  | {json_path}')
    with open(json_path, 'w') as fp:
        json.dump(clone, fp, indent=2)

def load(json_path: str):
    print(f'LOADING | {json_path}')
    with open(json_path) as fp:
        clone = json.load(fp)
    return clone

def replicate(json_path:str, base_path: str, dryrun=True, break_on_error=True):
    clone = load(json_path)

    # if not Path(base_path).exists():
        # raise FileNotFoundError(f'PATH NOT FOUND: {base_path}')
    
    for path, remote in clone.items():
        dest_path = (Path(base_path) / path).resolve()
        if dryrun:
            print(f'DRYRUN | {dest_path}')
        else:
            print(f'CLONE TO PATH | {dest_path}')
            try:
                output = git.clone(remote, dest_path)
                print(output)
            except git.GitException as ge:
                print(ge)
                if break_on_error:
                    return

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

    replicate(json_path, 'D:\\users\\username\\codetest\\vscode', dryrun=False, break_on_error=True)

