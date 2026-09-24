from dataclasses import fields

from models.settings import GeneratorSettings


class ProjectController:

    @staticmethod
    def save(settings, filename):
        import json
        from dataclasses import asdict

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(asdict(settings), f, indent=4)

    @staticmethod
    def load(filename):
        import json

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        allowed = {item.name for item in fields(GeneratorSettings)}
        filtered = {key: value for key, value in data.items() if key in allowed}
        return GeneratorSettings(**filtered)
