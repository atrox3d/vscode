from pathlib import Path
from dataclasses import dataclass

@dataclass
class GitRepo:
    name: str
    path: Path
    remote: str = None
