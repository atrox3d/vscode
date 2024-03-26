print(f'IMPORT | {__name__}')

import json
from pathlib import Path

if __name__ == '__main__':
    from simplegit import git
else:
    from .simplegit import git

class Workspace:
    def __init__(self, path:str) -> None:
        '''
        tries to load json workspace file into self.data
        '''
        self.path = Path(path).resolve()
        with open(str(self.path)) as fp:
            self.data: dict = json.load(fp)

    def get_items(self) -> dict[str, str]:
        '''
        returns array "folders" from workspace json,
        each element is a dict with name and path
        '''
        return self.data['folders']

    def get_tuples(self, default_name=None) -> list[tuple[str, str]]:
        '''
        returns a list of tuples containing name and path
        for each workspace folder
        '''
        return ((folder.get('name', default_name), folder['path']) 
                for folder in self.get_items())

    def get_names(self, default_name=None) -> list[str]:
        '''
        returns a list of only names for each workspace folder
        '''
        return (item['name'] for item in self.get_items())

    def get_paths(self, absolute=True) -> list[str]:
        folders = (item['path'] for item in self.get_items())
        if absolute:
            return (str(Path(folder).resolve()) for folder in folders)
        return folders
    
    def get_repos(self, absolute=False, recurse=False):
        for name, path in self.get_tuples():
            path = Path(path).resolve() if absolute else Path(path)
            if recurse:
                for repo_git_folder in path.glob('**/.git/'):
                    yield git.get_repo(name, repo_git_folder.parent)
            else:
                try:
                    yield git.get_repo(name, path)
                except git.NotAGitRepo:
                    pass

if __name__ == '__main__':
    ws = Workspace('code-workspace.code-workspace')
    for method in ws.get_items, ws.get_tuples, ws.get_names, ws.get_paths, ws.get_repos:
        print(method.__name__)
        print(list(method()))
        print()
