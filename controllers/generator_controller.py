from engine.generator import PasswordGenerator
from engine.exporter import Exporter


class GeneratorController:

    @staticmethod
    def preview(settings, limit=100):
        passwords = []

        for i, password in enumerate(PasswordGenerator.generate(settings)):
            passwords.append(password)

            if i + 1 >= limit:
                break

        return passwords

    @staticmethod
    def export(settings, filename):
        generator = PasswordGenerator.generate(settings)
        return Exporter.export(
            generator,
            filename,
            sort_results=getattr(settings, "sort_results", False),
        )