import pandas as pd

from models.schema import CandidateProfile


class CSVParser:

    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):

        df = pd.read_csv(self.file_path)

        candidates = []

        for index, row in df.iterrows():

            candidate = CandidateProfile()

            candidate.candidate_id = f"CAND-{index+1:03d}"

            candidate.source = "CSV"

            candidate.matched_sources.append("CSV")

            candidate.full_name = str(row["name"]).strip()

            candidate.emails.append(
                str(row["email"]).strip()
            )

            candidate.phones.append(
                str(row["phone"]).strip()
            )

            candidate.headline = str(
                row["title"]
            ).strip()

            company = str(
                row["current_company"]
            ).strip()

            candidate.experience.append({

                "company": company,

                "title": candidate.headline,

                "start": None,

                "end": None,

                "summary": None

            })

            location = str(
                row["location"]
            ).strip()

            parts = [
                x.strip()
                for x in location.split(",")
            ]

            if len(parts) > 0:
                candidate.location["city"] = parts[0]

            if len(parts) > 1:
                candidate.location["country"] = parts[1]

            candidates.append(candidate)

        return candidates