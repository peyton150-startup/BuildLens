"""Hold what happened during one working session.

Contract:
    in        nothing, a new Session starts empty
    out       changes, a list of diff-text strings in the order recorded
    unchanged everything outside this object
"""


class Session:
    def __init__(self):
        self.changes = []

    def record(self, diff_text):
        self.changes.append(diff_text)

    def history(self):
        history_list = list(self.changes)
        return history_list
