from modules.vscode_workspace import Workspace
from modules.gitrepo import GitRepo

if __name__ == '__main__':
    import os
    ws = Workspace('code-workspace.code-workspace')
    for repo in ws.get_repos(recurse=True, absolute=False):
        print(repo)