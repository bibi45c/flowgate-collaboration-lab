import copy
import contextlib
import io
import os
import unittest
from unittest import mock

from scripts import check_pr_metadata as metadata
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

    def test_same_repository_issue_url_is_accepted(self):
        pr = fixture(link="Refs https://github.com/bibi45c/flowgate-collaboration-lab/issues/1")
        self.assertEqual(validate(pr, linked_issues={1: {"number": 1}}), [])

    def test_other_repository_url_is_not_a_lab_issue(self):
        self.assertTrue(validate(fixture(link="Refs https://github.com/other/project/issues/1")))

    def test_qualified_reference_uses_repository_identity(self):
        text = "bibi45c/flowgate-collaboration-lab#1 other/project#2 #3"
        self.assertEqual(metadata.issue_references(text), {1, 3})

    def test_fenced_fake_form_is_rejected(self):
        for fence in ("```", "~~~~", "   ````"):
            with self.subTest(fence=fence):
                pr = fixture()
                pr["body"] = fence + "\n" + pr["body"] + "\n" + fence
                self.assertTrue(validate(pr))

    def test_fenced_example_does_not_create_duplicate_heading(self):
        pr = fixture()
        pr["body"] += "\n\n```markdown\n## Delivery\ncomplete\n```"
        self.assertEqual(validate(pr, linked_issues={1: {"number": 1}}), [])

    def test_link_only_in_fence_is_not_real_reference(self):
        self.assertTrue(validate(fixture(link="```\nRefs #1\n```")))


class LiveMetadataTests(unittest.TestCase):
    HEAD = "a" * 40
    BASE = "b" * 40

    def live(self, link="Refs #1"):
        pr = fixture(link=link)
        pr.update(head={"sha": self.HEAD}, base={"sha": self.BASE},
                  state="open", draft=False, updated_at="synthetic-version-1")
        return pr

    def api_for(self, initial, final=None):
        pulls = iter([initial, final or initial])
        def fake(path, payload=None):
            if path == f"repos/{metadata.REPO}/pulls/6":
                return next(pulls)
            if path == "graphql":
                return {"data": {"repository": {"pullRequest": {"closingIssuesReferences": {
                    "nodes": [], "pageInfo": {"hasNextPage": False}}}}}}
            if "/commits?" in path:
                return []
            if path == f"repos/{metadata.REPO}/issues/1":
                return {"number": 1}
            raise AssertionError(f"Unexpected API path: {path}")
        return fake

    def test_url_lookup_and_validation_share_parser(self):
        pr = self.live("Refs https://github.com/bibi45c/flowgate-collaboration-lab/issues/1")
        with mock.patch.object(metadata, "api", side_effect=self.api_for(pr)) as api:
            report = metadata.audit(metadata.REPO, 6, self.HEAD, self.BASE)
        self.assertEqual(report["errors"], [])
        self.assertEqual(sum(call.args[0].endswith("/issues/1") for call in api.call_args_list), 1)

    def test_missing_expected_version_fails_before_api(self):
        with mock.patch.object(metadata, "api") as api:
            with self.assertRaisesRegex(ValueError, "expected head"):
                metadata.audit(metadata.REPO, 6, None, self.BASE)
            api.assert_not_called()

    def test_stale_event_head_or_base_is_rejected(self):
        for key in ("head", "base"):
            with self.subTest(key=key):
                pr = self.live()
                pr[key]["sha"] = "c" * 40
                with mock.patch.object(metadata, "api", return_value=pr) as api:
                    with self.assertRaisesRegex(ValueError, "triggering event"):
                        metadata.audit(metadata.REPO, 6, self.HEAD, self.BASE)
                    self.assertEqual(api.call_count, 1)

    def test_changed_head_base_or_body_during_lookup_is_rejected(self):
        for key in ("head", "base", "body", "updated_at"):
            with self.subTest(key=key):
                initial = self.live()
                final = copy.deepcopy(initial)
                if key in {"head", "base"}:
                    final[key]["sha"] = "c" * 40
                else:
                    final[key] += " changed"
                with mock.patch.object(metadata, "api", side_effect=self.api_for(initial, final)):
                    report = metadata.audit(metadata.REPO, 6, self.HEAD, self.BASE)
                self.assertTrue(any("changed during" in error for error in report["errors"]))

    def test_existing_cli_bootstraps_through_environment(self):
        report = {"errors": []}
        with mock.patch.dict(os.environ, {"LAB_EXPECTED_HEAD": self.HEAD, "LAB_EXPECTED_BASE": self.BASE}):
            with mock.patch("sys.argv", ["guard", "--repo", metadata.REPO, "--number", "6"]):
                with mock.patch.object(metadata, "audit", return_value=report) as audit:
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertFalse(metadata.main())
                audit.assert_called_once_with(metadata.REPO, 6, self.HEAD, self.BASE)

    def test_cli_without_expected_versions_does_not_contact_api(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with mock.patch("sys.argv", ["guard", "--repo", metadata.REPO, "--number", "6"]):
                with mock.patch.object(metadata, "api") as api, contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as error:
                        metadata.main()
                    self.assertEqual(error.exception.code, 2)
                    api.assert_not_called()
