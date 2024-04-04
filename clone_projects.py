from pathlib import Path

from vscode_workspace import VsCodeWorkspace
from atrox3d.simplegit import git
import update_options as options

def get_gitrepos(ws:VsCodeWorkspace, absolute=False, recurse=False):
    '''
    return a list of GitRepo objects for each workspace folder,
    excluding non-git repos

    if recurse==True, searches recursively every git repo inside 
    each workspace item

    if absolute==True, the paths are converted to absolute paths
    '''
    for name, path in ws.get_configtuples():
        path = Path(path).resolve() if absolute else Path(path)
        if recurse:
            for repo_git_folder in path.glob('**/.git/'):
                yield git.get_repo(repo_git_folder.parent, name=name)
        else:
            try:
                yield git.get_repo(path, name=name)
            except git.NotAGitRepo:
                pass



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
    ws = VsCodeWorkspace('code-workspace.code-workspace')
    clone = {}
    for repo in get_gitrepos(ws, recurse=recurse):
        if repo.remote is not None:
            pass
        else:
            print(f'NO REMOTE | skipping | {repo.path}')