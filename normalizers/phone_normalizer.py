import phonenumbers


class PhoneNormalizer:

    @staticmethod
    def normalize(numbers):

        phones = []

        for num in numbers:

            try:

                phone = phonenumbers.parse(num, "IN")

                phones.append(

                    phonenumbers.format_number(

                        phone,

                        phonenumbers.PhoneNumberFormat.E164

                    )

                )

            except:
                pass

        return list(set(phones))