from models.constants import SKILL_MAPPING


class SkillNormalizer:

    @staticmethod
    def normalize(skills):

        unique = {}

        for skill in skills:

            name = skill["name"].lower()

            canonical = SKILL_MAPPING.get(name, skill["name"])

            unique[canonical] = {

                "name": canonical,

                "confidence": skill.get("confidence", 0.9),

                "sources": skill.get("sources", [])

            }

        return list(unique.values())