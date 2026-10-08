import unittest

from lab.access import authorize


class AlwaysEqual(str):
    def __new__(cls, value):
        instance = super().__new__(cls, value)
        instance.equal_calls = 0
        return instance

    def __eq__(self, other):
        self.equal_calls += 1
        return True


class EvilDict(dict):
    def get(self, *args, **kwargs):
        self.get_calls += 1
        raise AssertionError("custom dictionary get must not execute")


class AccessTests(unittest.TestCase):
    def test_active_matching_key_is_allowed(self):
        self.assertTrue(
            authorize({"tenant": "synthetic-a", "revoked": False}, "synthetic-a")
        )

    def test_revoked_matching_key_is_denied(self):
        self.assertFalse(
            authorize({"tenant": "synthetic-a", "revoked": True}, "synthetic-a")
        )

    def test_wrong_tenant_is_denied(self):
        self.assertFalse(
            authorize({"tenant": "synthetic-a", "revoked": False}, "synthetic-b")
        )

    def test_requested_tenant_subclass_is_denied_without_custom_equality(self):
        tenant = AlwaysEqual("synthetic-b")
        self.assertFalse(
            authorize({"tenant": "synthetic-a", "revoked": False}, tenant)
        )
        self.assertEqual(tenant.equal_calls, 0)

    def test_key_tenant_subclass_is_denied_without_custom_equality(self):
        tenant = AlwaysEqual("synthetic-b")
        self.assertFalse(
            authorize({"tenant": tenant, "revoked": False}, "synthetic-a")
        )
        self.assertEqual(tenant.equal_calls, 0)

    def test_dictionary_subclass_is_denied_without_custom_get(self):
        key = EvilDict(tenant="synthetic-a", revoked=False)
        key.get_calls = 0
        self.assertFalse(authorize(key, "synthetic-a"))
        self.assertEqual(key.get_calls, 0)

    def test_missing_fields_are_denied(self):
        for key in ({}, {"tenant": "synthetic-a"}, {"revoked": False}):
            with self.subTest(key=key):
                self.assertFalse(authorize(key, "synthetic-a"))

    def test_revoked_must_be_the_boolean_false(self):
        for revoked in (None, 0, 1, "false", "", [], {}):
            with self.subTest(revoked=revoked):
                self.assertFalse(
                    authorize({"tenant": "synthetic-a", "revoked": revoked}, "synthetic-a")
                )

    def test_malformed_keys_are_denied_without_raising(self):
        for key in (None, False, 0, "synthetic-a", [], (), set()):
            with self.subTest(key=key):
                self.assertFalse(authorize(key, "synthetic-a"))

    def test_malformed_or_empty_tenants_are_denied(self):
        for tenant in (None, False, 0, 1, "", [], {}):
            with self.subTest(tenant=tenant):
                self.assertFalse(
                    authorize({"tenant": tenant, "revoked": False}, tenant)
                )
                self.assertFalse(
                    authorize({"tenant": "synthetic-a", "revoked": False}, tenant)
                )
                self.assertFalse(
                    authorize({"tenant": tenant, "revoked": False}, "synthetic-a")
                )


if __name__ == "__main__":
    unittest.main()
