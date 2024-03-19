from modules.vscode_workspace import Workspace
from modules import git_helper as git

if __name__ == '__main__':
    import os
    ws = Workspace('code-workspace.code-workspace')
    ws.get_repos()