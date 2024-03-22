from modules.vscode_workspace import Workspace
from modules import git_helper as git

if __name__ == '__main__':
    import os
    ws = Workspace('code-workspace.code-workspace')
    for repo in ws.get_repos(recurse=False, absolute=False):
        # print(f'{repo = }')
        try:
            status = git.get_status(repo)
            # print(f'{status = }')
            # print(repo)
            print(
                  f'{repo.name:30.30} '
                  f'{repo.path.stem:30.30} '
                  f'{status.position} '
                  f'{status.commits} '
                  f'{"DIRTY" if status.dirty else ""}'
                  )
        except git.GitCommandException as gce:
            print(gce)
            exit()
    
    test = git.get_repo('vscode', '.')
    print(test)
    status = git.get_status(test)
    print(status)

