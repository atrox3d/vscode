from pathlib import Path
import subprocess
import os


def is_repo(path:str) -> bool:
    gitdir =  (Path(path).resolve() / '.git')
    return gitdir.is_dir()

def get_remote(path:str) -> str:
    os.chdir(Path(path).resolve())
    # print(os.getcwd())
    command = 'git remote -v'.split()
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout.split('\n'))
    if result.returncode == 0:
        print(result.stdout.split('\n')[0].split())
        name, url, mode = result.stdout.split('\n')[0].split()
        print(url)

if __name__ == '__main__':
    path = '../zio/cryptedit/'
    print(is_repo(path))
    get_remote(path)
