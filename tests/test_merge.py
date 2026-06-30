import unittest

from merger.field_merger import FieldMerger


class TestMerge(unittest.TestCase):

    def test_resume_priority(self):

        decision_log = []

        value, source = FieldMerger.merge(

            "headline",

            "Software Engineer",
            "CSV",

            "Backend Developer",
            "Resume",

            decision_log

        )

        self.assertEqual(
            value,
            "Backend Developer"
        )

        self.assertEqual(
            source,
            "Resume"
        )

        self.assertEqual(
            len(decision_log),
            1
        )


if __name__ == "__main__":
    unittest.main()