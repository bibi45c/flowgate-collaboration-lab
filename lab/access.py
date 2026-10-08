"""Toy tenant-key authorization fixture."""


def authorize(key: object, tenant: object) -> bool:
    """Allow an active synthetic key using only built-in dict and str inputs."""
    if type(key) is not dict or type(tenant) is not str or not tenant:
        return False

    key_tenant = key.get("tenant")
    return (
        type(key_tenant) is str
        and bool(key_tenant)
        and key_tenant == tenant
        and key.get("revoked") is False
    )
