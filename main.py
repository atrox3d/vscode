from modules.vscode_workspace import Workspace
from modules import git_helper as git

if __name__ == '__main__':
    import os
    ws = Workspace('code-workspace.code-workspace')
    for name, folder in ws.get_tuples():
        if git.is_repo(folder):
            print(name, git.get_remote(folder))
        else:
            print(name, 'not a git repo')