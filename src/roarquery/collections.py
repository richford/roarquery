import subprocess

from .utils import drop_empty


def get_collections() -> list:
    """Get collections from a database."""
    output = subprocess.check_output(["fuego", "c"])
    return drop_empty(output.decode("utf-8").split("\n"))
