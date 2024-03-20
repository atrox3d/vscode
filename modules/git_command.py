from pathlib import Path
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


res = run('git status -u --porcelain')
print(res)
for line in res.stdout.split('\n'):
    print(line)