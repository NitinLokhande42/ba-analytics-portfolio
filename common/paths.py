"""Small helpers shared by every project so scripts can be run from any working directory."""
from pathlib import Path


def project_dir(file: str) -> Path:
    """Return the project root (parent of data/ or src/) for a script's __file__."""
    return Path(file).resolve().parent.parent


def data_dir(file: str) -> Path:
    d = project_dir(file) / "data"
    d.mkdir(exist_ok=True)
    return d


def output_dir(file: str) -> Path:
    d = project_dir(file) / "output"
    d.mkdir(exist_ok=True)
    return d
