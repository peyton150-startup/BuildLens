"""Hold what happened during one working session.

Contract:
    supported writes go through record(diff_text)
    record rejects non-string values with TypeError("must be a string")
    history returns a copied list of diff-text strings in recorded order
    rejected writes leave the recorded history unchanged
"""


class Session:
    def __init__(self):
        self._changes: list[str] = []

    def record(self, diff_text: str) -> None:
        if not isinstance(diff_text, str):
            raise TypeError("must be a string")

        self._changes.append(diff_text)

    def history(self) -> list[str]:
        history_list = list(self._changes)
        return history_list
