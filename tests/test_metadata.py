import unittest

from scripts.check_pr_metadata import validate


def fixture(delivery="partial", phase="pre-merge", link="Refs #1"):
    fields = {"Summary": "Synthetic outcome", "Linked issues": link, "Delivery": delivery, "Acceptance phase": phase, "Verification": "Unit tests passed on the recorded source; CI pending", "Risk and recovery": "Low: synthetic in-memory data; revert PR", "Known limitations": "No real provider or human review tested"}
    return {"title": "fix(accounting): settle reservations once", "body": "\n\n".join(f"## {name}\n\n{value}" for name, value in fields.items())}


class MetadataTests(unittest.TestCase):
    def test_plain_partial_reference_is_allowed(self):
        self.assertEqual(validate(fixture(), linked_issues={1: {"number": 1}}), [])

    def test_bad_title_is_rejected(self):
        pr = fixture()
        pr["title"] = "fix stuff"
        self.assertTrue(validate(pr))

    def test_partial_closing_keyword_is_rejected(self):
        self.assertTrue(validate(fixture(link="Closes #1")))

    def test_manual_closing_reference_is_rejected(self):
        self.assertTrue(validate(fixture(), closing_issue_numbers=[1]))

    def test_post_merge_closing_commit_is_rejected(self):
        self.assertTrue(validate(fixture(delivery="complete", phase="post-merge"), commit_messages=["fix(access): deny revoked keys\n\nFixes #1"]))

    def test_complete_pre_merge_closing_is_allowed(self):
        self.assertEqual(validate(fixture(delivery="complete", link="Closes #1"), closing_issue_numbers=[1]), [])

    def test_comment_only_section_is_rejected(self):
        pr = fixture()
        pr["body"] = pr["body"].replace("Synthetic outcome", "<!-- fill this -->")
        self.assertTrue(validate(pr))

    def test_reference_to_pr_instead_of_issue_is_rejected(self):
        self.assertTrue(validate(fixture(), linked_issues={1: {"pull_request": {}}}))

    def test_duplicate_sections_are_rejected(self):
        pr = fixture()
        pr["body"] += "\n\n## Delivery\ncomplete"
        self.assertTrue(validate(pr))
