from identity.resolver import IdentityResolver
from merger.field_merger import FieldMerger


class CandidateEnricher:

    # =====================================================
    # Main Enrichment
    # =====================================================

    def enrich(self, registry, profile):

        # ---------- Fast Lookup by Phone ----------

        from normalizers.phone_normalizer import PhoneNormalizer

        profile.phones = PhoneNormalizer.normalize(profile.phones)

        for phone in profile.phones:

            candidate = registry.find_by_phone(phone)

            if candidate:

                self.merge(
                    candidate,
                    profile,
                    "phone",
                    1.0
                )

                registry.refresh_indexes(candidate)

                return

        # ---------- Fast Lookup by Email ----------

        for email in profile.emails:

            candidate = registry.find_by_email(email)

            if candidate:

                self.merge(
                    candidate,
                    profile,
                    "email",
                    0.95
                )

                registry.refresh_indexes(candidate)

                return

        # ---------- Fallback to Name Similarity ----------

        for candidate in registry.all():

            result = IdentityResolver.match(
                candidate,
                profile
            )

            if result["matched"]:

                self.merge(
                    candidate,
                    profile,
                    result["method"],
                    result["score"]
                )

                registry.refresh_indexes(candidate)

                return

        # ---------- No Match ----------

        self.handle_unmatched_candidate(
            registry,
            profile
        )

    # =====================================================
    # Handle Unmatched Candidate
    # =====================================================

    def handle_unmatched_candidate(
        self,
        registry,
        profile
    ):

        # Recruiter Notes should never create candidates

        if profile.source == "Notes":
            return

        # Resume without identity should not create candidate

        if (
            not profile.full_name
            and not profile.emails
            and not profile.phones
        ):
            return

        profile.candidate_id = (
            f"CAND-{registry.size()+1:03d}"
        )

        if profile.source:

            profile.matched_sources = [{

    "source": profile.source,

    "matched_on": "New Candidate",

    "match_score": 1.0

}]

        registry.add_candidates([profile])

    # =====================================================
    # Merge
    # =====================================================

    def merge(
        self,
        candidate,
        profile,
        matched_on,
        match_score
    ):

        self.merge_contacts(candidate, profile)

        self.merge_headline(candidate, profile)

        self.merge_location(candidate, profile)

        self.merge_skills(candidate, profile)

        self.merge_experience(candidate, profile)

        self.merge_education(candidate, profile)

        self.update_sources(
            candidate,
            profile,
            matched_on,
            match_score
        )

    # =====================================================
    # Contacts
    # =====================================================

    def merge_contacts(
        self,
        candidate,
        profile
    ):

        candidate.emails = list(
            set(candidate.emails + profile.emails)
        )

        candidate.phones = list(
            set(candidate.phones + profile.phones)
        )

    # =====================================================
    # Headline
    # =====================================================

    def merge_headline(
        self,
        candidate,
        profile
    ):

        candidate.headline, candidate.source = FieldMerger.merge(

            "headline",

            candidate.headline,

            candidate.source,

            profile.headline,

            profile.source,

            candidate.decision_log

        )

    # =====================================================
    # Location
    # =====================================================

    def merge_location(
        self,
        candidate,
        profile
    ):

        city, _ = FieldMerger.merge(

            "city",

            candidate.location["city"],

            candidate.source,

            profile.location["city"],

            profile.source,

            candidate.decision_log

        )

        country, _ = FieldMerger.merge(

            "country",

            candidate.location["country"],

            candidate.source,

            profile.location["country"],

            profile.source,

            candidate.decision_log

        )

        candidate.location["city"] = city
        candidate.location["country"] = country

    # =====================================================
    # Skills
    # =====================================================

    def merge_skills(
        self,
        candidate,
        profile
    ):

        candidate.skills.extend(profile.skills)

        unique = {}

        for skill in candidate.skills:

            unique[skill["name"]] = skill

        candidate.skills = list(unique.values())

    # =====================================================
    # Experience
    # =====================================================

    def merge_experience(
    self,
    candidate,
    profile
):

        companies = {}

        for exp in candidate.experience:

            company = exp.get("company")

            if company:

                companies[company] = exp

        for exp in profile.experience:

            company = exp.get("company")

            if not company:
                continue

            if company not in companies:

                companies[company] = exp

            else:

                existing = companies[company]

                old_title = existing.get("title")
                new_title = exp.get("title")

                old_priority = candidate.source
                new_priority = profile.source

                if (
                    new_priority == "Resume"
                    and new_title
                ):

                    existing["title"] = new_title

                if exp.get("summary"):
                    existing["summary"] = exp["summary"]

                if exp.get("start"):
                    existing["start"] = exp["start"]

                if exp.get("end"):
                    existing["end"] = exp["end"]

        candidate.experience = list(companies.values())
    # =====================================================
    # Education
    # =====================================================

    def merge_education(
        self,
        candidate,
        profile
    ):

        existing = set()

        merged = []

        for edu in candidate.education:

            key = (
                edu.get("institution"),
                edu.get("degree")
            )

            existing.add(key)

            merged.append(edu)

        for edu in profile.education:

            key = (
                edu.get("institution"),
                edu.get("degree")
            )

            if key not in existing:

                merged.append(edu)

        candidate.education = merged

    # =====================================================
    # Source Tracking
    # =====================================================

    def update_sources(
    self,
    candidate,
    profile,
    matched_on,
    match_score
):

        # Convert old string format to dictionary
        converted = []

        for src in candidate.matched_sources:

            if isinstance(src, str):

                converted.append({

                    "source": src,

                    "matched_on": "Initial Registration",

                    "match_score": 1.0

                })

            else:

                converted.append(src)

        candidate.matched_sources = converted

        for src in candidate.matched_sources:

            if src["source"] == profile.source:
                return

        candidate.matched_sources.append({

            "source": profile.source,

            "matched_on": matched_on,

            "match_score": match_score

        })