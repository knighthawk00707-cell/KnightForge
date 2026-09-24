import random


class PlacementEngine:

    @staticmethod
    def generate(base, insert, settings=None):

        if settings is None:
            settings = {}
        # If no placement option is enabled,
        # default to Prefix + Suffix.
        if not any(settings.values()):
            settings["prefix"] = True
            settings["suffix"] = True

        generated = set()

        def add(password):
            if password not in generated:
                generated.add(password)
                yield password

        # --------------------------
        # Prefix
        # --------------------------

        if settings.get("prefix", True):

            yield from add(insert + base)

        # --------------------------
        # Suffix
        # --------------------------

        if settings.get("suffix", True):

            yield from add(base + insert)

        # --------------------------
        # Every Position
        # --------------------------

        if settings.get("every_position", False):

            for i in range(len(base) + 1):

                yield from add(
                    base[:i] + insert + base[i:]
                )

        # --------------------------
        # Before Every Character
        # --------------------------

        if settings.get("before_each", False):

            password = ""

            for ch in base:
                password += insert + ch

            yield from add(password)

        # --------------------------
        # After Every Character
        # --------------------------

        if settings.get("after_each", False):

            password = ""

            for ch in base:
                password += ch + insert

            yield from add(password)

        # --------------------------
        # Between Characters
        # --------------------------

        if settings.get("between_each", False):

            if len(base) > 1:

                password = insert.join(base)

                yield from add(password)

        # --------------------------
        # Random Position
        # --------------------------

        if settings.get("random_position", False):

            pos = random.randint(
                0,
                len(base)
            )

            yield from add(
                base[:pos] + insert + base[pos:]
            )