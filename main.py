from modules.vscode import Workspace
from modules.simplegit import git

if __name__ == '__main__':
    ws = Workspace('code-workspace.code-workspace')
    for repo in ws.get_repos(recurse=False):
        # print(f'{repo = }')
        try:
            status = repo.get_status()
            # print(f'{status = }')
            # print(repo)
            print(
                  f'{repo.name:30.30} '
                  f'{repo.path.stem:30.30} '
                  f'{status.position} '
                  f'{status.commits} '
                  f'{status.push} '
                  f'{status.pull} '
                  f'{"DIRTY" if repo.is_dirty() else ""}'
                  )
        except git.GitCommandException as gce:
            print(gce)
            exit()
    
    test = git.get_repo('vscode', '.')
    print(test)
    status = git.get_status(test)
    print(status)

