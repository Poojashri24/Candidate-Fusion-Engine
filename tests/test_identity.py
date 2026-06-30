import unittest

from identity.resolver import IdentityResolver
from models.schema import CandidateProfile


class TestIdentity(unittest.TestCase):

    def test_phone_match(self):

        c1 = CandidateProfile()
        c2 = CandidateProfile()

        c1.phones = ["+919876543210"]
        c2.phones = ["+919876543210"]

        result = IdentityResolver.match(c1, c2)

        self.assertTrue(result["matched"])
        self.assertEqual(result["method"], "phone")

    def test_email_match(self):

        c1 = CandidateProfile()
        c2 = CandidateProfile()

        c1.emails = ["abc@gmail.com"]
        c2.emails = ["abc@gmail.com"]

        result = IdentityResolver.match(c1, c2)

        self.assertTrue(result["matched"])
        self.assertEqual(result["method"], "email")


if __name__ == "__main__":
    unittest.main()