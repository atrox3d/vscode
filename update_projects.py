from pathlib import Path

from vscode_workspace import VsCodeWorkspace
from atrox3d.simplegit import git
import options as options
from common import get_gitrepos

def print_repo(repo:git.GitRepo):
    print(
            f'{repo.name:25.25} '
            f'{repo.path:50.50} '
    )

def print_status(status:git.GitStatus, repo:git.GitRepo) -> None:
    action = f'PUSH({status.commits})' if status.need_push \
             else f'PULL({status.commits})' if status.need_pull \
             else 'NO_ACTION'
    dirty = f'DIRTY({status.total()})' if status.dirty else ""
    print(
            f'{repo.name:25.25} '
            f'{repo.path:50.50} '
            f'{status.branch:10.10}'
            f'{action:{len("NO_ACTION")}.{len("NO_ACTION")}} '
            f'{dirty}'
            )

def pull(repo:git.GitRepo, status:git.GitStatus, dry_run):
    if status.need_pull:
        if repo.remote:
            if dry_run:
                print(f'DRY RUN | PULL       | {status.branch}')
            else:
                print(f'PULL   | {status.branch}')
                output = git.pull(repo.path)
        else:
            print(f'PULL   | no remote')

def push(repo:git.GitRepo, status:git.GitStatus, dry_run, force=False):
    if status.need_push or force:
        if repo.remote:
            if dry_run:
                print(f'DRY RUN | PUSH       | {status.branch}')
            else:
                print(f'PUSH   | {status.branch}')
                output = git.push(repo.path)
        else:
            print(f'PUSH   | no remote')

def commit(repo:git.GitRepo, status:git.GitStatus, commit_message:str, dry_run):
    if dry_run:
        print(f'DRY RUN | AUTOCOMMIT | {status.branch}')
        print(f'DRY RUN | ADD        | {status.branch}')
        print(f'DRY RUN | COMMIT     | {status.branch} | {commit_message}')
    else:
        print(f'ADD    | {status.branch}')
        output = git.add(repo.path, all=True)
        print(f'COMMIT | {status.branch} | {commit_message}')
        output = git.commit(repo.path, commit_message, add_all=True)

def grep(path:str, terms:list[str]) -> bool:
    if not terms:
        return True
    for term in terms:
        if term in path:
            return True
    return False

def exclude(path:str, terms:list[str]) -> bool:
    if not terms:
        return False
    return grep(path, terms)

def main():
    import argparse
    parser = options.get_update_parser()
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
        if not grep(repo.path, args.grep):
            continue
        if exclude(repo.path, args.exclude):
            continue

        if args.listrepos:
            print_repo(repo)
            continue
        try:
            status = git.get_status(repo)
            if not status.dirty and args.skipclean:
                continue
            print_status(status, repo)
            
            if pull_enabled:
                pull(repo, status, dry_run)
            
            if status.dirty and auto_commit:
                commit(repo, status, commit_message, dry_run)
                if push_enabled:
                    push(repo, status, dry_run, force=True)

            if push_enabled:
                push(repo, status, dry_run)

        except git.GitException as ge:
            print(ge)
            exit()
