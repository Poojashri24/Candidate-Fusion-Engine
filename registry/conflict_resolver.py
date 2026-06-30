SOURCE_PRIORITY = {
    "Resume": 100,
    "CSV": 90,
    "Notes": 80
}


class ConflictResolver:

    @staticmethod
    def choose(current_value,
               current_source,
               incoming_value,
               incoming_source):

        if not incoming_value:
            return current_value, current_source

        if not current_value:
            return incoming_value, incoming_source

        current_score = SOURCE_PRIORITY.get(
            current_source,
            0
        )

        incoming_score = SOURCE_PRIORITY.get(
            incoming_source,
            0
        )

        if incoming_score > current_score:

            return incoming_value, incoming_source

        return current_value, current_source