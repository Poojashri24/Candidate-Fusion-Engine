class ConfidenceEngine:

    SOURCE_PRIORITY = {
        "Resume": 0.95,
        "CSV": 0.90,
        "Notes": 0.80
    }

    @staticmethod
    def score(source):

        return ConfidenceEngine.SOURCE_PRIORITY.get(
            source,
            0.50
        )

    @staticmethod
    def overall(profile):

        scores = []

        for skill in profile.skills:
            scores.append(skill["confidence"])

        if not scores:
            return 0.80

        return round(sum(scores) / len(scores), 2)