from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

@dataclass
class Config():
    name:str
    index: int
    path: Path

@dataclass
class Batch():
    path: Path              # Directory
    rng: tuple[int, int]
    length: int
    configs: list[Path] = field(default_factory=list)
    gconfigs: list[Path] = field(default_factory=list)
    health: Any = None   