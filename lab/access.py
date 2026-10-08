"""Toy tenant-key authorization fixture."""


def authorize(key: object, tenant: object) -> bool:
    """Allow only an active synthetic key for a nonempty matching tenant."""
    if not isinstance(key, dict) or not isinstance(tenant, str) or not tenant:
        return False

    key_tenant = key.get("tenant")
    return (
        isinstance(key_tenant, str)
        and bool(key_tenant)
        and key_tenant == tenant
        and key.get("revoked") is False
    )
