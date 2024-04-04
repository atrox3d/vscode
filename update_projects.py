from pathlib import Path

from vscode_workspace import VsCodeWorkspace
from atrox3d.simplegit import git
import update_options as options
from common import get_gitrepos


def print_status(status:git.GitStatus, repo:git.GitRepo) -> None:
    action = f'PUSH({status.commits})' if status.push else f'PULL({status.commits})' if status.pull else 'NO_ACTION'
    dirty = f'DIRTY({len(status.added)+len(status.deleted)+len(status.modified)+len(status.untracked)})' if status.dirty else ""
    print(
            f'{repo.name:25.25} '
            f'{repo.path:50.50} '
            f'{status.branch:10.10}'
            f'{action:{len("NO_ACTION")}.{len("NO_ACTION")}} '
            f'{dirty}'
            )

def pull(repo:git.GitRepo, status:git.GitStatus, dry_run):
    if status.pull:
        if repo.remote:
            if dry_run:
                print(f'DRY RUN | PULL       | {status.branch}')
            else:
                print(f'PULL   | {status.branch}')
                git.pull(repo.path)
        else:
            print(f'PULL   | no remote')

def push(repo:git.GitRepo, status:git.GitStatus, dry_run, force=False):
    if status.push or force:
        if repo.remote:
            if dry_run:
                print(f'DRY RUN | PUSH       | {status.branch}')
            else:
                print(f'PUSH   | {status.branch}')
                git.push(repo.path)
        else:
            print(f'PUSH   | no remote')

def commit(repo:git.GitRepo, status:git.GitStatus, commit_message:str, dry_run):
    if dry_run:
        print(f'DRY RUN | AUTOCOMMIT | {status.branch}')
        print(f'DRY RUN | ADD        | {status.branch}')
        print(f'DRY RUN | COMMIT     | {status.branch} | {commit_message}')
    else:
        print(f'ADD    | {status.branch}')
        git.add(repo.path, all=True)
        print(f'COMMIT | {status.branch} | {commit_message}')
        git.commit(repo.path, commit_message, all=True)


def main():
    import argparse
    parser = options.get_parser()
    args: argparse.Namespace = parser.parse_args()

    if args.all:
        recurse = auto_commit = pull_enabled = push_enabled = True
    else:
        recurse = args.recurse
        auto_commit = args.commit is not None
        push_enabled = args.push
        pull_enabled = args.pull

    dry_run = args.dryrun
    commit_message = 'automatic update' if args.commit is None else args.commit

    for k, v in vars(args).items():
        print(f'PARAM  | {k} = {v}')

    ws = VsCodeWorkspace('code-workspace.code-workspace')
    for repo in get_gitrepos(ws, recurse=recurse):
        try:
            status = git.get_status(repo)
            print_status(status, repo)
            
            if pull_enabled:
                pull(repo, status, dry_run)
            
            if status.dirty and auto_commit:
                commit(repo, status, commit_message, dry_run)
                if push_enabled:
                    push(repo, status, dry_run, force=True)

            if push_enabled:
                push(repo, status, dry_run)

        except git.GitCommandException as gce:
            print(gce)
            exit()
