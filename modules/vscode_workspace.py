import json
from pathlib import Path

class Workspace:
    def __init__(self, path:str) -> None:
        self.path = Path(path).resolve()
        with open(str(self.path)) as fp:
            self.data = json.load(fp)

    def get_items(self):
        return self.data['folders']

    def get_tuples(self, default_name=None) -> list[tuple[str, str]]:
        return [(folder.get('name', default_name), folder['path']) for folder in self.get_items()]

    def get_names(self, default_name=None) -> list[str]:
        # return [folder.get('name', None) for folder in self.data['folders']]
        return [item[0] for item in self.get_tuples(default_name)]

    def get_folders(self, resolve=True) -> list[str]:
        # folders = [folder['path'] for folder in self.data['folders']]
        folders = [item[1] for item in self.get_tuples()]
        if resolve:
            return [str(Path(folder).resolve()) for folder in folders]
        return folders
        
    


if __name__ == '__main__':
    ws = Workspace('code-workspace.code-workspace')
    print(ws.get_folders(False))
    # print(ws.get_items())
    # print(ws.get_names())
    