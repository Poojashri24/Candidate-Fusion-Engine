import unittest

from models.schema import CandidateProfile
from projection.projection import Projection


class TestProjection(unittest.TestCase):

    def test_projection_fields(self):

        candidate = CandidateProfile()

        candidate.full_name = "Poojashri D"
        candidate.emails = ["pooja@gmail.com"]
        candidate.overall_confidence = 0.95
        candidate.provenance = []

        config = {
            "fields": [
                {
                    "path": "candidate_name",
                    "from": "full_name"
                },
                {
                    "path": "email",
                    "from": "emails[0]"
                }
            ],
            "include_confidence": True,
            "include_provenance": False,
            "missing": "omit"
        }

        output = Projection.apply(candidate, config)

        self.assertEqual(
            output["candidate_name"],
            "Poojashri D"
        )

        self.assertEqual(
            output["email"],
            "pooja@gmail.com"
        )

        self.assertEqual(
            output["overall_confidence"],
            0.95
        )


if __name__ == "__main__":
    unittest.main()