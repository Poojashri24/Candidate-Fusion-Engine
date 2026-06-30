import os


class FileLoader:

    @staticmethod
    def pdf_files(folder):

        if not os.path.exists(folder):
            return []

        return sorted([
            os.path.join(folder, file)
            for file in os.listdir(folder)
            if file.lower().endswith(".pdf")
        ])

    @staticmethod
    def txt_files(folder):

        if not os.path.exists(folder):
            return []

        return sorted([
            os.path.join(folder, file)
            for file in os.listdir(folder)
            if file.lower().endswith(".txt")
        ])