from models.schema import CandidateProfile


class NotesParser:

    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):

        candidate = CandidateProfile()
        candidate.source = "Notes"

        with open(self.file_path, "r", encoding="utf-8") as file:
            text = file.read()

        lines = text.splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            lower = line.lower()

            # Preferred Location

            if lower.startswith("preferred location"):

                location = line.split(":", 1)[1].strip()

                candidate.location["city"] = location

            # Expected Role

            elif lower.startswith("expected role"):

                candidate.headline = line.split(":", 1)[1].strip()

        return candidate