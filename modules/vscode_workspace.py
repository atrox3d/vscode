import json
from pathlib import Path

class Workspace:
    def __init__(self, path:str) -> None:
        self.path = Path(path).resolve()
        with open(str(self.path)) as fp:
            self.data = json.load(fp)

    def get_folders(self, resolve=True) -> list[str]:
        folders = [folder['path'] for folder in self.data['folders']]
        if resolve:
            return [str(Path(folder).resolve()) for folder in folders]
        return folders

    def get_names(self) -> list[str]:
        return [folder.get('name', None) for folder in self.data['folders']]
    
    def get_items(self) -> list[tuple[str, str]]:
        return [(folder.get('name', None), folder['path']) for folder in self.data['folders']]


if __name__ == '__main__':
    ws = Workspace('code-workspace.code-workspace')
    # print(ws.get_folders(False))
    # print(ws.get_items())
    