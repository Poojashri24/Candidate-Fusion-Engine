from collections import defaultdict


class CandidateRegistry:

    def __init__(self):

        # -----------------------------
        # Master Candidate Registry
        # -----------------------------

        self.candidates = []

        # -----------------------------
        # Fast Lookup Indexes
        # -----------------------------

        self.phone_index = {}
        self.email_index = {}

        # -----------------------------
        # Statistics
        # -----------------------------

        self.stats = defaultdict(int)

    # =====================================================
    # Add Candidate(s)
    # =====================================================

    def add_candidates(self, candidates):

        for candidate in candidates:

            # Prevent duplicate object insertion
            if candidate in self.candidates:
                continue

            self.candidates.append(candidate)

            self.refresh_indexes(candidate)

            if candidate.source == "CSV":
                self.stats["csv"] += 1

            if candidate.source != "CSV":
                self.stats["new"] += 1

    # =====================================================
    # Lookup Methods
    # =====================================================

    def find_by_phone(self, phone):

        if not phone:
            return None

        return self.phone_index.get(phone)

    def find_by_email(self, email):

        if not email:
            return None

        return self.email_index.get(email.lower())

    # =====================================================
    # Refresh Lookup Indexes
    # =====================================================

    def refresh_indexes(self, candidate):

        for phone in candidate.phones:

            if phone:
                self.phone_index[phone] = candidate

        for email in candidate.emails:

            if email:
                self.email_index[email.lower()] = candidate

    # =====================================================
    # Candidate Access
    # =====================================================

    def all(self):
        return self.candidates

    def size(self):
        return len(self.candidates)

    # =====================================================
    # Statistics
    # =====================================================

    def statistics(self):

        merged = 0

        for candidate in self.candidates:

            if len(candidate.matched_sources) > 1:
                merged += 1

        return {

            "csv_candidates": self.stats["csv"],

            "resume_candidates": self.stats["resume"],

            "notes_candidates": self.stats["notes"],

            "merged_candidates": merged,

            "new_candidates": self.stats["new"],

            "final_candidates": len(self.candidates)

        }

    # =====================================================
    # Pretty Summary
    # =====================================================

    def summary(self):

        stats = self.statistics()

        print("\n========== REGISTRY SUMMARY ==========\n")

        print(f"CSV Records Processed      : {stats['csv_candidates']}")
        print(f"Resume Files Processed     : {stats['resume_candidates']}")
        print(f"Notes Files Processed      : {stats['notes_candidates']}")
        print(f"Merged Profiles            : {stats['merged_candidates']}")
        print(f"New Profiles Created       : {stats['new_candidates']}")
        print(f"Final Canonical Profiles   : {stats['final_candidates']}")

        print("\n======================================\n")