import json
from pathlib import Path

# from atrox3d.simplegit import git


class VsCodeWorkspace:
    def __init__(self, workspace_config_path:str) -> None:
        '''
        tries to load json workspace file into self.data
        '''
        self.path = Path(workspace_config_path).resolve()
        with open(str(self.path)) as fp:
            self.data: dict = json.load(fp)

    def get_configitems(self) -> dict[str, str]:
        '''
        returns array "folders" from workspace json,
        each element is a dict with [name] and path
        '''
        return self.data['folders']

    def get_configtuples(self, default_name=None) -> list[tuple[str, str]]:
        '''
        returns a list of tuples containing [name or default_name] and path
        for each workspace folder
        '''
        return ((folder.get('name', default_name), folder['path']) 
                for folder in self.get_configitems())

    def get_foldernames(self, default_name=None) -> list[str]:
        '''
        returns a list of only [names or default_names] for each workspace folder
        '''
        return (item['name'] for item in self.get_configitems())

    def get_folderpaths(self, absolute=True) -> list[str]:
        '''
        returns a list of only absolute paths for each workspace folder
        '''
        folders = (item['path'] for item in self.get_configitems())
        if absolute:
            return (str(Path(folder).resolve()) for folder in folders)
        return folders
    
    def get_missingpaths(self):
        return [path for name, path in self.get_configtuples()
                if not Path(path).exists()]
            
    
    # def get_clones(self, absolute=False):
    #     return (repo.asdict() for repo in 
    #             self.get_gitrepos(absolute, recurse=True)
    #             if repo.remote is not None)
    
    # def save_clones(self, path:str) -> None:
    #     with open(path, 'w') as fp:
    #         json.dump(list(self.get_clones()), fp, indent=2)
    


if __name__ == '__main__':
    ws = VsCodeWorkspace('code-workspace.code-workspace')
    # for method in ws.get_configitems, ws.get_configtuples, ws.get_foldernames, ws.get_folderpaths, ws.get_gitrepos:
        # print(method.__name__)
        # print(list(method()))
        # print()
    print( ws.get_missingpaths())