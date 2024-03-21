from modules.vscode_workspace import Workspace
from modules import git_helper as git

if __name__ == '__main__':
    import os
    ws = Workspace('code-workspace.code-workspace')
    for repo in ws.get_repos(recurse=False, absolute=False):
        print(f'{repo = }')
        try:
            git.status(repo)
        except git.GitCommandException as gce:
            print(gce)
            exit()