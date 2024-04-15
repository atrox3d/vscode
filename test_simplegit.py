# from pathlib import Path
import argparse

# from vscode_workspace import VsCodeWorkspace
from atrox3d.simplegit import git


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--add', action='store_true', default=False)
    parser.add_argument('-c', '--commit', action='store_true', default=False)
    parser.add_argument('-p', '--pull', action='store_true', default=False)
    parser.add_argument('-P', '--push', action='store_true', default=False)
    parser.add_argument('-A', '--all', action='store_true', default=False)

    return parser.parse_args()

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

def main():

    args = parse_args()
    print(args)
    try:
        print(f'GETTIG REPO FROM "."')
        path = '.'
        repo = git.get_repo(path)
        print(repo)

        print(f'GETTIG STATUS FOR REPO "."')
        status = git.get_status(repo)
        print(status)

        if args.pull or args.all:
            print(f'PULLING FROM {repo.remote}')
            result = git.pull(path)
            print(result)
        else:
            print(f'SKIPPING PULL')

        if status.dirty:
            if args.add or args.all:
                print(f'ADDING FILES')
                result = git.add(path, all=True)
                print(result)
            else:
                print(f'SKIPPING ADD')

            if args.commit or args.all:
                print(f'COMMITTING CHANGES')
                result = git.commit(path, 'test commit', add_all=True)
                print(result)
            else:
                print(f'SKIPPING COMMIT')

            if args.push or args.all:
                print(f'PUSHING CHANGES')
                result = git.push(path)
                print(result)
            else:
                print(f'SKIPPING PUSH')

    except git.GitCommandException as gce:
        print(gce)

        

