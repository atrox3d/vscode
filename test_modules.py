from pathlib import Path

from vscode_workspace import VsCodeWorkspace
from atrox3d.simplegit import git
from common import get_gitrepos


def print_status(status:git.GitStatus, repo:git.GitRepo) -> None:
    action = f'PUSH({status.commits})' if status.need_push else f'PULL({status.commits})' if status.need_pull else 'NO_ACTION'
    dirty = f'DIRTY({status.total()})' if status.dirty else ""
    print(
            f'{repo.name:25.25} '
            f'{repo.path:50.50} '
            f'{status.branch:10.10}'
            f'{action:{len("NO_ACTION")}.{len("NO_ACTION")}} '
            f'{dirty}'
            )

def main():
    ws = VsCodeWorkspace('code-workspace.code-workspace')
    header = (
            f'{"name":25.25} '
            f'{"path":50.50} '
            f'{"branch":10.10}'
            f'{"action":{len("NO_ACTION")}.{len("NO_ACTION")}} '
            f'{"dirty"}'
    ).upper()
    print('_' * len(header))
    print('LIST OF WORKSPACE REPOS AND THEIR STATUS')
    print(header)
    print('_' * len(header))
    for repo in get_gitrepos(ws, recurse=False):
        try:
            status = git.get_status(repo)
            print_status(status, repo)
        except git.GitStatusException as gse:
            print(gse)
            exit()
