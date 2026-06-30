from rapidfuzz import fuzz


class IdentityResolver:

    @staticmethod
    def match(candidate, profile):
        """
        Returns:
        {
            "matched": bool,
            "method": str,
            "score": float
        }
        """

        # -------------------------
        # Phone Match (Highest Priority)
        # -------------------------

        if candidate.phones and profile.phones:

            common = set(candidate.phones) & set(profile.phones)

            if common:
                return {
                    "matched": True,
                    "method": "phone",
                    "score": 1.00
                }

        # -------------------------
        # Email Match
        # -------------------------

        if candidate.emails and profile.emails:

            candidate_emails = {
                email.lower()
                for email in candidate.emails
            }

            profile_emails = {
                email.lower()
                for email in profile.emails
            }

            if candidate_emails & profile_emails:

                return {
                    "matched": True,
                    "method": "email",
                    "score": 0.95
                }

        # -------------------------
        # Name Similarity
        # -------------------------

        if candidate.full_name and profile.full_name:

            similarity = fuzz.ratio(
                candidate.full_name.lower(),
                profile.full_name.lower()
            )

            if similarity >= 90:

                return {
                    "matched": True,
                    "method": "name",
                    "score": 0.80
                }

        # -------------------------
        # No Match
        # -------------------------

        return {
            "matched": False,
            "method": None,
            "score": 0.0
        }