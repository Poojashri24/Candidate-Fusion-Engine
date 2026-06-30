import json
import os

from parsers.csv_parser import CSVParser
from parsers.pdf_parser import PDFParser
from parsers.resume_extractor import ResumeExtractor
from parsers.notes_parser import NotesParser

from registry.candidate_registry import CandidateRegistry
from registry.enrichment import CandidateEnricher

from utils.file_loader import FileLoader
from validation.validator import Validator
  
from normalizers.email_normalizer import EmailNormalizer
from normalizers.phone_normalizer import PhoneNormalizer
from normalizers.skill_normalizer import SkillNormalizer

from confidence.confidence_engine import ConfidenceEngine
from utils.provenance import Provenance
from projection.projection import Projection


def normalize_candidate(candidate):

    candidate.emails = EmailNormalizer.normalize(
        candidate.emails
    )

    candidate.phones = PhoneNormalizer.normalize(
        candidate.phones
    )

    candidate.skills = SkillNormalizer.normalize(
        candidate.skills
    )

    candidate.overall_confidence = ConfidenceEngine.overall(
        candidate
    )

    candidate.provenance = Provenance.build(
        candidate
    )


def main():

    print("\n========== Candidate Fusion Engine ==========\n")

    # --------------------------------------------
    # Candidate Registry
    # --------------------------------------------

    registry = CandidateRegistry()

    enricher = CandidateEnricher()

    # --------------------------------------------
    # Load CSV
    # --------------------------------------------

    csv_candidates = CSVParser(
        "input/recruiter.csv"
    ).parse()
    for candidate in csv_candidates:

        candidate.emails = EmailNormalizer.normalize(candidate.emails)

        candidate.phones = PhoneNormalizer.normalize(candidate.phones)
    registry.add_candidates(csv_candidates)
    registry.stats["csv"] = len(csv_candidates)

    # --------------------------------------------
    # Load Resumes
    # --------------------------------------------

    resume_files = FileLoader.pdf_files("input/resumes")

    for pdf in resume_files:

        registry.stats["resume"] += 1

        text = PDFParser(pdf).extract_text()
        

        from parsers.ai_resume_extractor import AIResumeExtractor

        try:

            data = AIResumeExtractor().extract(text)

            profile = ResumeExtractor.from_ai(data)

        except:

            profile = ResumeExtractor(text).extract()

            enricher.enrich(registry, profile)

    # --------------------------------------------
    # Load Notes
    # --------------------------------------------

    note_files = FileLoader.txt_files("input/notes")

    for txt in note_files:

        registry.stats["notes"] += 1

        profile = NotesParser(txt).parse()

        enricher.enrich(registry, profile)

    # --------------------------------------------
    # Normalize Candidates
    # --------------------------------------------

    for candidate in registry.all():

        normalize_candidate(
            candidate
        )

    # --------------------------------------------
    # Load Runtime Config
    # --------------------------------------------

    # Configuration will come from Streamlit.
    # Keep a default config when running main.py directly.

    config = {
        "fields": [
            {
                "path": "full_name"
            },
            {
                "path": "emails",
                "from": "emails[0]"
            },
            {
                "path": "skills",
                "from": "skills[].name"
            }
        ],
        "include_confidence": True,
        "include_provenance": True,
        "missing": "omit"
    }

    # --------------------------------------------
    # Runtime Projection
    # --------------------------------------------

    from dataclasses import asdict

    final_profiles = []

    for candidate in registry.all():

        errors = Validator.validate(asdict(candidate), config)

        profile = asdict(candidate)

        profile["validation"] = {
            "status": len(errors) == 0,
            "errors": errors
        }

        final_profiles.append(profile)

    # --------------------------------------------
    # Save JSON
    # --------------------------------------------

    os.makedirs(
        "output",
        exist_ok=True
    )

    from datetime import datetime

    output = {

        "generated_at": datetime.now().isoformat(),

        "total_candidates": len(final_profiles),

        "profiles": final_profiles

    }

    with open(
            "output/canonical_profiles.json",
            "w",
            encoding="utf-8") as f:

        json.dump(
            output,
            f,
            indent=4,
            ensure_ascii=False
        )

    # --------------------------------------------
    # Console Output
    # --------------------------------------------

    print("\n========== FINAL REGISTRY ==========\n")

    for candidate in registry.all():

        print(f"Candidate ID      : {candidate.candidate_id}")
        print(f"Name              : {candidate.full_name}")
        print(f"Headline          : {candidate.headline}")
        print(f"Emails            : {candidate.emails}")
        print(f"Phones            : {candidate.phones}")
        if candidate.links["linkedin"]:
            print("LinkedIn         :", candidate.links["linkedin"])

        if candidate.links["github"]:
            print("GitHub           :", candidate.links["github"])

        if candidate.links["portfolio"]:
            print("Portfolio        :", candidate.links["portfolio"])
        print(f"Location          : {candidate.location}")
        print("Matched Sources")

        for src in candidate.matched_sources:

            if isinstance(src, dict):

                print(
                    f"  • {src['source']} "
                    f"(Matched On: {src['matched_on']}, "
                    f"Score: {src['match_score']})"
                )

            else:

                print(f"  • {src}")

        print(f"Confidence        : {candidate.overall_confidence}")
        projected = Projection.apply(candidate, config)

        errors = Validator.validate(projected, config)

        if errors:

            print("\nValidation")

            print("FAILED")

            for err in errors:

                print(" •", err)

        else:

            print("\nValidation")

            print("PASSED")

        print("\nSkills")

        if candidate.skills:

            for skill in candidate.skills:

                print(f"  • {skill['name']}")

        print("\nExperience")

        if candidate.experience:

            for exp in candidate.experience:

                print(
                    f"  • {exp.get('company')} - {exp.get('title')}"
                )

        print("\nEducation")

        if candidate.education:

            for edu in candidate.education:

                print(
                    f"  • {edu.get('degree')} | {edu.get('institution')}"
                )

        print("\nDecision Log")

        if candidate.decision_log:

            for log in candidate.decision_log:

                print(log)

        print("\nProvenance")

        if candidate.provenance:

            for item in candidate.provenance:

                print(item)

        print("\n" + "=" * 70 + "\n")

    # --------------------------------------------
    # Registry Statistics
    # --------------------------------------------

    registry.summary()

    print("✅ Canonical JSON generated successfully.")
    print("📁 output/canonical_profiles.json")


if __name__ == "__main__":
    main()