from models.schema import CandidateProfile

from identity.resolver import IdentityResolver


class MergeEngine:

    def merge(self, profiles):

        merged_profiles = []

        for profile in profiles:

            found = False

            for merged in merged_profiles:

                if IdentityResolver.is_same_candidate(
                        merged,
                        profile):

                    self.combine(
                        merged,
                        profile
                    )

                    found = True

                    break

            if not found:

                merged_profiles.append(profile)

        return merged_profiles

    def combine(self, merged, profile):

        merged.emails = list(

            set(

                merged.emails +

                profile.emails

            )

        )

        merged.phones = list(

            set(

                merged.phones +

                profile.phones

            )

        )

        merged.skills.extend(

            profile.skills

        )

        merged.experience.extend(

            profile.experience

        )

        merged.education.extend(

            profile.education

        )
        # Merge links
        for link in profile.links["linkedin"]:
            if link not in merged.links["linkedin"]:
                merged.links["linkedin"].append(link)

        for link in profile.links["github"]:
            if link not in merged.links["github"]:
                merged.links["github"].append(link)

        for link in profile.links["portfolio"]:
            if link not in merged.links["portfolio"]:
                merged.links["portfolio"].append(link)

        for link in profile.links["other"]:
            if link not in merged.links["other"]:
                merged.links["other"].append(link)

        # Generic headline selection

        priorities = {

            "Resume": 3,

            "CSV": 2,

            "Notes": 1

        }

        if profile.headline:

            if merged.headline is None:

                merged.headline = profile.headline

            else:

                current = priorities.get(
                    merged.source,
                    0
                )

                incoming = priorities.get(
                    profile.source,
                    0
                )

                if incoming > current:

                    merged.headline = profile.headline

                    merged.source = profile.source

        if profile.location["city"]:

            merged.location["city"] = profile.location["city"]

        if profile.location["country"]:

            merged.location["country"] = profile.location["country"]
        