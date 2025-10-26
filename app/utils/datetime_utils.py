from datetime import datetime
from typing import Any, Optional


def parse_datetime(value: Any) -> Optional[datetime]:
    """Convert ISO timestamp string to datetime. Returns None if invalid."""
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None
