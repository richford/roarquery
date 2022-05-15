"""Query Firestore collections."""
import subprocess  # noqa: S404
from typing import List

from .utils import drop_empty


def get_collections() -> List[str]:
    """Get collections from a database."""
    output = subprocess.check_output(["fuego", "c"])  # noqa: S603, S607
    return drop_empty(output.decode("utf-8").split("\n"))
