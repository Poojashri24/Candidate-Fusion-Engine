class Provenance:

    @staticmethod
    def build(profile):

        provenance = []

        # -----------------------------
        # Emails
        # -----------------------------
        for email in profile.emails:

            provenance.append({

                "field": "email",

                "value": email,

                "source": profile.source,

                "method": "Structured" if profile.source == "CSV" else "Regex Extraction",

                "confidence": 0.99 if profile.source == "CSV" else 0.95

            })

        # -----------------------------
        # Phones
        # -----------------------------
        for phone in profile.phones:

            provenance.append({

                "field": "phone",

                "value": phone,

                "source": profile.source,

                "method": "Structured" if profile.source == "CSV" else "Regex Extraction",

                "confidence": 0.99 if profile.source == "CSV" else 0.95

            })

        # -----------------------------
        # Skills
        # -----------------------------
        for skill in profile.skills:

            provenance.append({

                "field": "skill",

                "value": skill["name"],

                "source": profile.source,

                "method": "Skill Dictionary Match",

                "confidence": skill.get("confidence", 0.95)

            })

        # -----------------------------
        # Experience
        # -----------------------------
        for exp in profile.experience:

            provenance.append({

                "field": "experience",

                "value": f"{exp.get('company')} - {exp.get('title')}",

                "source": profile.source,

                "method": "Section Extraction",

                "confidence": 0.90

            })

        # -----------------------------
        # Education
        # -----------------------------
        for edu in profile.education:

            provenance.append({

                "field": "education",

                "value": f"{edu.get('degree')} | {edu.get('institution')}",

                "source": profile.source,

                "method": "Section Extraction",

                "confidence": 0.90

            })
        # -----------------------------
# Links
# -----------------------------
        for link in profile.links["linkedin"]:
            provenance.append({
                "field": "linkedin",
                "value": link,
                "source": profile.source,
                "method": "Regex Extraction",
                "confidence": 0.95
            })

        for link in profile.links["github"]:
            provenance.append({
                "field": "github",
                "value": link,
                "source": profile.source,
                "method": "Regex Extraction",
                "confidence": 0.95
            })

        for link in profile.links["portfolio"]:
            provenance.append({
                "field": "portfolio",
                "value": link,
                "source": profile.source,
                "method": "Regex Extraction",
                "confidence": 0.95
            })

        return provenance