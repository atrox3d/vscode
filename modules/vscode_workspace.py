import json
from pathlib import Path

from .gitrepo import GitRepo, GitCommandException

class Workspace:
    def __init__(self, path:str) -> None:
        self.path = Path(path).resolve()
        with open(str(self.path)) as fp:
            self.data = json.load(fp)

    def get_items(self):
        return self.data['folders']

    def get_tuples(self, default_name=None) -> list[tuple[str, str]]:
        return [(folder.get('name', default_name), folder['path']) 
                for folder in self.get_items()]

    def get_names(self, default_name=None) -> list[str]:
        return [name for name, path in self.get_tuples(default_name)]

    def get_folders(self, absolute=True) -> list[str]:
        folders = [path for name, path in self.get_tuples()]
        if absolute:
            return [str(Path(folder).resolve()) for folder in folders]
        return folders
    
    def get_repos(self, absolute=False, default_name=None, recurse=True):
        for name, path in self.get_tuples(default_name):
            path = Path(path).resolve() if absolute else Path(path)
            if recurse:
                for gitrepo in path.glob('**/.git/'):
                    yield GitRepo(name, gitrepo.parent, None)
            elif GitRepo.is_repo(path):
                yield GitRepo(name, path, None)
            # else:
                # yield GitRepo(name, None, None)


if __name__ == '__main__':
    ws = Workspace('code-workspace.code-workspace')
    print(ws.get_folders(False))
    # print(ws.get_items())
    # print(ws.get_names())
    