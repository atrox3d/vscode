import json
from pathlib import Path

class Workspace:
    def __init__(self, path:str) -> None:
        self.path = Path(path).resolve()

        with open(str(self.path)) as fp:
            self.data = json.load(fp)
        
        self.folders = self.data['folders']

if __name__ == '__main__':
    ws = Workspace('code-workspace.code-workspace')
    print(ws.folders)
    