from modules.vscode_workspace import Workspace
from modules import git_helper as git

if __name__ == '__main__':
    import os
    ws = Workspace('code-workspace.code-workspace')
    for folder in ws.get_folders(False):
        if git.is_repo(folder):
            print(folder, git.get_remote(folder))
        else:
            print(folder, 'not a git repo')