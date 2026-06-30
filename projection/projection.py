from normalizers.phone_normalizer import PhoneNormalizer
from normalizers.skill_normalizer import SkillNormalizer
import re

class Projection:

    @staticmethod
    def get_attr(profile, key):

        if isinstance(profile, dict):
            return profile.get(key)

        return getattr(profile, key, None)
    

    @staticmethod
    def apply(profile, config):

        output = {}

        for field in config["fields"]:

            # --------------------------
            # Config values
            # --------------------------

            output_name = field["path"]

            source = field.get("from", output_name)

            normalize = field.get("normalize")

            required = field.get("required", False)

            value = Projection.get_value(profile, source)

            # --------------------------
            # Normalization
            # --------------------------

            if value is not None:

                if normalize == "E164":

                    if isinstance(value, list):
                        value = PhoneNormalizer.normalize(value)

                        value = value[0] if value else None

                    else:
                        value = PhoneNormalizer.normalize([value])

                        value = value[0] if value else None

                elif normalize == "canonical":

                    if isinstance(value, list):

                        skills = []

                        for s in value:

                            if isinstance(s, dict):
                                skills.append(s)

                            else:
                                skills.append({
                                    "name": s
                                })

                        value = SkillNormalizer.normalize(skills)

                        value = [

                            x["name"]

                            for x in value

                        ]

            # --------------------------
            # Missing Handling
            # --------------------------

            if value is None:

                mode = config.get(

                    "missing",

                    "omit"

                )

                if required or mode == "error":

                    raise ValueError(

                        f"Missing required field : {output_name}"

                    )

                elif mode == "null":

                    output[output_name] = None

                elif mode == "omit":

                    pass

            else:

                output[output_name] = value

        # --------------------------
        # Confidence
        # --------------------------

        if config.get(

            "include_confidence",

            False

        ):

            output["overall_confidence"] = Projection.get_attr(
    profile,
    "overall_confidence"
)

        # --------------------------
        # Provenance
        # --------------------------

        if config.get(

            "include_provenance",

            False

        ):

            output["provenance"] = Projection.get_attr(
    profile,
    "provenance"
)

        return output

    # ====================================================
    # Nested Field Resolver
    # ====================================================

    @staticmethod
    def get_value(profile, path):

        current = profile

        parts = path.split(".")

        for part in parts:

            # -----------------------------
            # emails[0]
            # -----------------------------
            if "[" in part and "]" in part and "[]" not in part:

                name = part[:part.index("[")]

                index = int(
                    re.search(r"\[(\d+)\]", part).group(1)
                )

                if isinstance(current, dict):
                    current = current.get(name)
                else:
                    current = getattr(current, name, None)

                if current is None:
                    return None

                if index >= len(current):
                    return None

                current = current[index]

            # -----------------------------
            # skills[]
            # -----------------------------
            elif part.endswith("[]"):

                name = part[:-2]

                if isinstance(current, dict):
                    current = current.get(name)
                else:
                    current = getattr(current, name, None)

                if current is None:
                    return []

            # -----------------------------
            # Normal attribute
            # -----------------------------
            else:

                if isinstance(current, list):

                    result = []

                    for item in current:

                        if isinstance(item, dict):
                            result.append(item.get(part))
                        else:
                            result.append(getattr(item, part, None))

                    current = result

                else:

                    if isinstance(current, dict):
                        current = current.get(part)
                    else:
                        current = getattr(current, part, None)

            if current is None:
                return None

        return current