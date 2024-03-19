from pathlib import Path
import subprocess
import os


class GitCommandException(subprocess.CalledProcessError):
    pass

def is_repo(path:str) -> bool:
    path = Path(path).resolve()
    if path.exists():
        gitdir =  path / '.git'
        if gitdir.exists():
            return gitdir.is_dir()
        return False
    
    raise FileNotFoundError(f'is_repo: {path} does not exist')

def get_remote(path:str) -> str:
    cwd = os.getcwd()
    os.chdir(Path(path).resolve())
    command = 'git remote -v'.split()
    try:
        result = subprocess.run(command, check=True, shell=False, capture_output=True, text=True)
        if result.stdout:
            name, url, mode = result.stdout.split('\n')[0].split()
            return url
        else:
            return None
    except subprocess.CalledProcessError as cpe:
        raise GitCommandException(**vars(cpe))
    finally:
        os.chdir(cwd)

if __name__ == '__main__':
    import sys
    path = Path(sys.argv[1]).resolve()
    
    if is_repo(path):
        try:
            print(get_remote(path))
        except GitCommandException as gce:
            print(gce.stderr)
    else:
        print(f'not a git repo: {path}')
