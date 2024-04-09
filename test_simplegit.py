# from pathlib import Path

# from vscode_workspace import VsCodeWorkspace
from atrox3d.simplegit import git


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
    try:
        path = '.'
        repo = git.get_repo(path)
        print(repo)
        status = git.get_status(repo)
        print(status)

        result = git.pull(path)
        print(result)

        if status.dirty:
            result = git.add(path, all=True)
            print(result)

            result = git.commit(path, 'test commit', add_all=True)
            print(result)

            result = git.push(path)
            print(result)

    except git.GitCommandException as gce:
        print(gce)

        

