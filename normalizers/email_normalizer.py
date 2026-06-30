from email_validator import validate_email, EmailNotValidError


class EmailNormalizer:

    @staticmethod
    def normalize(emails):

        normalized = []

        for email in emails:

            try:

                valid = validate_email(
                    email,
                    check_deliverability=False
                )

                normalized.append(valid.email.lower())

            except EmailNotValidError:
                pass

        return list(set(normalized))