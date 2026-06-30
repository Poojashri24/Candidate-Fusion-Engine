SOURCE_PRIORITY = {
    "Resume": 100,
    "CSV": 90,
    "Notes": 80
}


class FieldMerger:

    @staticmethod
    def merge(
        field,
        old_value,
        old_source,
        new_value,
        new_source,
        decision_log
    ):
        if old_value == new_value:
            return old_value, old_source

        if not new_value:
            return old_value, old_source

        if not old_value:

            decision_log.append({

                "field": field,

                "selected": new_value,

                "selected_source": new_source,

                "selected_priority": SOURCE_PRIORITY.get(
                    new_source,
                    0
                ),

                "rejected": None,

                "rejected_source": None,

                "reason": "Empty Value"

            })

            return new_value, new_source

        old_score = SOURCE_PRIORITY.get(old_source, 0)
        new_score = SOURCE_PRIORITY.get(new_source, 0)

        if new_score > old_score:

            decision_log.append({

                "field": field,

                "selected": new_value,

                "selected_source": new_source,

                "selected_priority": new_score,

                "rejected": old_value,

                "rejected_source": old_source,

                "reason": "Higher Source Priority"

            })

            return new_value, new_source

        decision_log.append({

            "field": field,

            "selected": old_value,

            "selected_source": old_source,

            "selected_priority": old_score,

            "rejected": new_value,

            "rejected_source": new_source,

            "reason": "Existing Value Preferred"

        })

        return old_value, old_source