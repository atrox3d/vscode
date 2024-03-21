import subprocess
import os
import shlex

class GitCommandException(subprocess.CalledProcessError):
    pass

class NotAGitRepo(Exception):
    pass

def run(command: str) -> subprocess.CompletedProcess:
    args = shlex.split(command)
    try:
        completed = subprocess.run(command, check=True, shell=False, capture_output=True, text=True)
        return completed
    except subprocess.CalledProcessError as cpe:
        raise GitCommandException(**vars(cpe))

def pushd(fn):
    def wrapper(*args, **kwargs):
        cwd = os.getcwd()
        result = fn(*args, **kwargs)
        os.chdir(cwd)
        return result
    return wrapper
