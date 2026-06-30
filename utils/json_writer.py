import json


class JsonWriter:

    @staticmethod
    def save(data, path):

        with open(path, "w", encoding="utf-8") as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )