"""Toy tenant-key authorization fixture."""


def authorize(key: dict, tenant: str) -> bool:
    """Return whether this synthetic key belongs to the requested tenant."""
    return key.get("tenant") == tenant
