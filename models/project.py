import json


class Project:

    def __init__(self):

        self.data = {
            "strings": [],
            "numbers": {
                "enabled": True,
                "min": 1,
                "max": 2,
            },
            "symbols": [
                "!",
                "@",
                "#",
                "$",
            ],
            "rules": {},
        }

    def save(self, filename):

        with open(filename, "w") as f:
            json.dump(
                self.data,
                f,
                indent=4,
            )

    def load(self, filename):

        with open(filename) as f:
            self.data = json.load(f)