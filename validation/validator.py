class Validator:

    @staticmethod
    def validate(profile, config):

        errors = []

        for field in config.get("fields", []):

            name = field["path"]
            required = field.get("required", False)
            expected = field.get("type")

            value = profile.get(name)

            # Required validation
            if required and (
                value is None
                or value == ""
                or value == []
            ):
                errors.append(f"{name} is required")
                continue

            if value is None:
                continue

            # Type validation
            if expected == "string":

                if not isinstance(value, str):
                    errors.append(f"{name} must be string")

            elif expected == "number":

                if not isinstance(value, (int, float)):
                    errors.append(f"{name} must be number")

            elif expected == "string[]":

                if not isinstance(value, list):
                    errors.append(f"{name} must be array")

                elif not all(isinstance(x, str) for x in value):
                    errors.append(f"{name} must contain strings")

        return errors