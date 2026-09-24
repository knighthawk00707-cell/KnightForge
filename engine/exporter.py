from pathlib import Path


class Exporter:

    @staticmethod
    def export(passwords, filename, sort_results=False):
        output = Path(filename)
        count = 0

        if sort_results:
            items = sorted(passwords)
            with output.open("w", encoding="utf-8") as file:
                for password in items:
                    file.write(password + "\n")
                    count += 1
            return count

        with output.open("w", encoding="utf-8") as file:
            for password in passwords:
                file.write(password + "\n")
                count += 1

        return count
