from pathlib import Path


def is_repo(path:str) -> bool:
    gitdir =  (Path(path).resolve() / '.git')
    return gitdir.is_dir()

if __name__ == '__main__':
    print(is_repo('../zio/cryptedit'))