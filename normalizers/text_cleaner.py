import re


class TextCleaner:

    @staticmethod
    def clean(text):

        if text is None:
            return None

        text = text.replace("(cid:127)", "")
        text = text.replace("\t", " ")

        text = re.sub(r"\s+", " ", text)

        return text.strip()