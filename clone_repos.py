import json
# from pathlib import Path

from common import get_gitrepos
from vscode_workspace import VsCodeWorkspace
import options
# import atrox3d.simplegit as git
from atrox3d.simplegit import git, repos

def collect_repos(workspace_path: str, recurse: bool) -> dict:
    ws = VsCodeWorkspace(workspace_path)
    repos = {}
    for repo in get_gitrepos(ws, recurse=recurse):
        if repo.remote is not None:
            print(f'ADDING | {repo.path}')
            repos[repo.path] = repo.remote
        else:
            print(f'NO REMOTE | skipping | {repo.path}')
    
    return repos

def save_repos(repos: dict, json_path: str):
    print(f'SAVING  | {json_path}')
    with open(json_path, 'w') as fp:
        json.dump(repos, fp, indent=2)

def load_repos(json_path: str):
    print(f'LOADING | {json_path}')
    with open(json_path) as fp:
        repos = json.load(fp)
    return repos

def backup_repos(workspace_path: str, json_path:str, recurse: bool):
    clone = collect_repos(workspace_path, recurse)
    save_repos(clone, json_path)

def main():
    import argparse
    parser = options.get_clone_parser()
    args: argparse.Namespace = parser.parse_args()

    for k, v in vars(args).items():
        print(f'PARAM  | {k} = {v}')

    if args.command == 'backup':
        backup_repos(args.workspace, args.json, args.recurse)
    elif args.command == 'restore':
        repos.restore(args.json, args.destpath, args.dryrun, args.breakonerrors)
    else:
        # this should never run, because argparse takes care of it
        raise ValueError(f'uknown subcommand {args.command!r}')




