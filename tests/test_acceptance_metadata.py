import unittest

from scripts.check_pr_metadata import validate


SYNTHETIC_ISSUES = {101: {"number": 101}}


def acceptance_fixture(delivery, phase, link="Refs #101"):
    fields = {
        "Summary": "Synthetic staged acceptance outcome",
        "Linked issues": link,
        "Delivery": delivery,
        "Acceptance phase": phase,
        "Verification": "Synthetic local checks passed; remote acceptance pending",
        "Risk and recovery": "Low risk: synthetic metadata; revert the test change",
        "Known limitations": "No live API, merge, or human approval tested",
    }
    return {
        "title": "test(governance): cover staged acceptance metadata",
        "body": "\n\n".join(f"## {name}\n\n{value}" for name, value in fields.items()),
    }


class AcceptanceMetadataTests(unittest.TestCase):
    def test_complete_delivery_closing_depends_on_acceptance_phase(self):
        cases = (
            ("pre-merge", "Refs #101", []),
            ("pre-merge", "Closes #101", []),
            ("post-merge", "Refs #101", []),
            (
                "post-merge",
                "Closes #101",
                ["Partial/post-merge delivery cannot use closing keywords"],
            ),
        )
        for phase, link, expected_errors in cases:
            with self.subTest(phase=phase, link=link):
                self.assertEqual(
                    validate(
                        acceptance_fixture("complete", phase, link),
                        linked_issues=SYNTHETIC_ISSUES,
                    ),
                    expected_errors,
                )

    def test_partial_delivery_development_links_are_rejected_in_both_phases(self):
        for phase in ("pre-merge", "post-merge"):
            for closing_links in ((), (101,)):
                with self.subTest(phase=phase, closing_links=closing_links):
                    expected_errors = (
                        ["Partial/post-merge delivery cannot have closing Development links"]
                        if closing_links else []
                    )
                    self.assertEqual(
                        validate(
                            acceptance_fixture("partial", phase),
                            closing_issue_numbers=closing_links,
                            linked_issues=SYNTHETIC_ISSUES,
                        ),
                        expected_errors,
                    )

    def test_unknown_delivery_and_phase_are_rejected_independently(self):
        cases = (
            ("staged", "pre-merge", ["Delivery must be complete or partial"]),
            (
                "complete",
                "during-merge",
                ["Acceptance phase must be pre-merge or post-merge"],
            ),
            (
                "staged",
                "during-merge",
                [
                    "Delivery must be complete or partial",
                    "Acceptance phase must be pre-merge or post-merge",
                ],
            ),
        )
        for delivery, phase, expected_errors in cases:
            with self.subTest(delivery=delivery, phase=phase):
                self.assertEqual(
                    validate(
                        acceptance_fixture(delivery, phase),
                        linked_issues=SYNTHETIC_ISSUES,
                    ),
                    expected_errors,
                )
