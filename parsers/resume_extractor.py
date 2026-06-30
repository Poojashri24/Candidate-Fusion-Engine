import re

from models.schema import CandidateProfile
from models.constants import SKILL_MAPPING

@staticmethod
def from_ai(data):

    candidate = CandidateProfile()

    candidate.source = "Resume"

    candidate.full_name = data.get("full_name")

    candidate.emails = data.get("emails", [])

    candidate.phones = data.get("phones", [])

    candidate.headline = data.get("headline")

    candidate.skills = [

        {

            "name": s,

            "confidence": 0.98,

            "sources": ["AI"]

        }

        for s in data.get("skills", [])

    ]

    candidate.experience = data.get("experience", [])

    candidate.education = data.get("education", [])

    return candidate

class ResumeExtractor:

    def __init__(self, text):
        self.text = text

    # =====================================================
    # Main Extraction
    # =====================================================

    def extract(self):

        candidate = CandidateProfile()
        candidate.source = "Resume"

        lines = [
            line.strip()
            for line in self.text.split("\n")
            if line.strip()
        ]

        candidate.full_name = self.extract_name(lines)

        candidate.emails = self.extract_email()

        candidate.phones = self.extract_phone()

        candidate.headline = self.extract_headline(lines)

        candidate.location = self.extract_location()

        candidate.skills = self.extract_skills()

        candidate.experience = self.extract_experience()

        candidate.education = self.extract_education()

        candidate.links["linkedin"] = []

        candidate.links["github"] = []

        linkedin = self.extract_linkedin()
        github = self.extract_github()

        if linkedin:
            candidate.links["linkedin"].append(linkedin)

        if github:
            candidate.links["github"].append(github)
        

        return candidate

    # =====================================================
    # Name
    # =====================================================

    def extract_name(self, lines):

        for line in lines[:5]:

            if (
    len(line.split()) >= 2
    and len(line) < 40
    and "@" not in line
    and ":" not in line
):
                return line

        return None

    def extract_linkedin(self):
        match = re.search(
            r"(https?://(www\.)?linkedin\.com/[^\s]+|linkedin\.com/[^\s]+)",
            self.text,
            re.IGNORECASE
        )
        return match.group(0) if match else None
    
    def extract_github(self):
        match = re.search(
            r"(https?://github\.com/[^\s]+|github\.com/[^\s]+)",
            self.text,
            re.IGNORECASE
        )
        return match.group(0) if match else None
    # =====================================================
    # Email
    # =====================================================

    def extract_email(self):

        emails = re.findall(

            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

            self.text

        )

        return list(set(emails))

    # =====================================================
    # Phone
    # =====================================================

    def extract_phone(self):

        phones = re.findall(

            r"(?:\+91[\s-]?)?[6-9]\d{9}",

            self.text.replace(" ", "")

        )

        return list(set(phones))

    # =====================================================
    # Headline
    # =====================================================

    def extract_headline(self, lines):

        ignore = {
            "email",
            "phone",
            "location",
            "linkedin",
            "github",
            "professional summary",
            "summary",
            "skills",
            "experience",
            "education",
            "projects"
        }

        name = self.extract_name(lines)

        for line in lines[:10]:

            lower = line.lower()

            if (
                line == name
                or "@" in line
                or ":" in line
                or lower in ignore
            ):
                continue

            if len(line) < 60:
                return line

        return None

    # =====================================================
    # Location
    # =====================================================

    def extract_location(self):

        cities = [

            "Bangalore",
            "Chennai",
            "Hyderabad",
            "Mumbai",
            "Delhi",
            "Pune",
            "Kolkata",
            "Noida",
            "Ahmedabad",
            "Coimbatore"

        ]

        location = {

            "city": None,

            "region": None,

            "country": None

        }

        for city in cities:

            if city.lower() in self.text.lower():

                location["city"] = city

                location["country"] = "India"

                break

        return location

    # =====================================================
    # Skills
    # =====================================================

    def extract_skills(self):

        text = self.text.lower()

        skills = []

        for key, value in SKILL_MAPPING.items():

            pattern = r"\b" + re.escape(key.lower()) + r"\b"

            if re.search(pattern, text):

                skills.append({

                    "name": value,

                    "confidence": 0.95,

                    "sources": ["Resume"]

                })

        unique = {}

        for skill in skills:

            unique[skill["name"]] = skill

        return list(unique.values())

# =====================================================
# Duration Checker
# =====================================================

    def is_duration(self, text):

        return bool(
            re.search(
                r"(19|20)\d{2}|Present|Current|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December",
                text,
                re.IGNORECASE
            )
        )

    # =====================================================
    # Experience
    # =====================================================
    
    def extract_experience(self):

        experience = []

        lines = [
            line.strip()
            for line in self.text.split("\n")
            if line.strip()
        ]

        stop_sections = {
    "EDUCATION",
    "PROJECTS",
    "PROJECT",
    "CERTIFICATIONS",
    "CERTIFICATION",
    "SKILLS",
    "TECHNICAL SKILLS",
    "ACHIEVEMENTS",
    "LANGUAGES",
    "SUMMARY",
    "PROFESSIONAL SUMMARY",
    "PROFILE"
}

        start = -1

        for i, line in enumerate(lines):

            if line.strip().upper() in {
    "EXPERIENCE",
    "WORK EXPERIENCE",
    "PROFESSIONAL EXPERIENCE",
    "EMPLOYMENT HISTORY"
}:
                start = i + 1
                break

        if start == -1:
            return experience

        i = start

        while i < len(lines):

            line = lines[i]

            if line.upper() in stop_sections:
                break

            title = line

            if i + 2 >= len(lines):
                break

            company = lines[i + 1]
            duration = lines[i + 2]

            # Skip invalid experience entries
            if not self.is_duration(duration):
                i += 1
                continue

            summary = []

            i += 3

            while i < len(lines):

                current = lines[i]

                if current.strip().upper() in stop_sections:
                    break

                # Next job detected
                if (
                    i + 2 < len(lines)
                    and not current.startswith("•")
                    and not current.startswith("(cid:127)")
                    and not lines[i + 1].startswith("•")
                ):
                    break

                if current.startswith("•") or current.startswith("(cid:127)"):

                    current = current.replace("•", "")
                    current = current.replace("(cid:127)", "")
                    summary.append(current.strip())

                i += 1

            experience.append({

                "title": title,
                "company": company,
                "duration": duration,
                "summary": " ".join(summary)

            })

        return experience
    # =====================================================
    # Education
    # =====================================================

    def extract_education(self):

        education = []

        lines = [
            line.strip()
            for line in self.text.split("\n")
            if line.strip()
        ]

        start = -1

        for i, line in enumerate(lines):
            if line.upper() == "EDUCATION":
                start = i + 1
                break

        if start == -1:
            return education

        stop_sections = {
            "PROJECTS",
            "EXPERIENCE",
            "SKILLS",
            "CERTIFICATIONS",
            "ACHIEVEMENTS",
            "LANGUAGES"
        }

        keywords = {
            "b.e",
            "b.tech",
            "m.tech",
            "m.e",
            "b.sc",
            "m.sc",
            "bachelor",
            "master"
        }

        i = start

        while i < len(lines):

            if lines[i].upper() in stop_sections:
                break

            lower = lines[i].lower()

            if any(k in lower for k in keywords):

                education.append({
                    "degree": lines[i],
                    "institution": lines[i+1] if i+1 < len(lines) else "",
                    "year": lines[i+2] if i+2 < len(lines) else ""
                })

                break

            i += 1

        return education
    
