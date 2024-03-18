from modules.vscode_workspace import Workspace

if __name__ == '__main__':
    ws = Workspace('code-workspace.code-workspace')
    print(ws.get_folders())
    