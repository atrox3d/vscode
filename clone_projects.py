import json
from pathlib import Path

from common import get_gitrepos
from vscode_workspace import VsCodeWorkspace
import options
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

def replicate(json_path:str, base_path: str, dryrun=True, breakonerrors=True):
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
                if breakonerrors:
                    return

def main():
    import argparse
    parser = options.get_clone_parser()
    args: argparse.Namespace = parser.parse_args()

    for k, v in vars(args).items():
        print(f'PARAM  | {k} = {v}')

    recurse = args.recurse
    json_path = args.json
    workspace_path = args.workspace
    dryrun = args.dryrun
    breakonerrors =  args.breakonerrors


    replicate(json_path, 'D:\\users2\\username\\codetest\\vscode', 
              dryrun=dryrun, breakonerrors=breakonerrors)

