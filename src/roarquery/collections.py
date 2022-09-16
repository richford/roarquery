"""Query Firestore collections."""
import subprocess  # nosec
from typing import List

from .utils import drop_empty


def get_collections() -> List[str]:
    """Get collections from a database."""
    output = subprocess.check_output(["fuego", "c"])  # nosec
    return drop_empty(output.decode("utf-8").split("\n"))
