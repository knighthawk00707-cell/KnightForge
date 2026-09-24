class StringEngine:

    @staticmethod
    def generate_cases(
        text,
        lowercase=True,
        uppercase=False,
        capitalize=False,
        alternate=False,
    ):
        produced = []

        def add(value):
            if value not in produced:
                produced.append(value)

        if not any((lowercase, uppercase, capitalize, alternate)):
            add(text)
            yield from produced
            return

        if lowercase:
            add(text.lower())

        if uppercase:
            add(text.upper())

        if capitalize and text:
            add(text[:1].upper() + text[1:].lower())

        if alternate:
            chars = []
            make_upper = False
            for char in text:
                if char.isalpha():
                    chars.append(char.upper() if make_upper else char.lower())
                    make_upper = not make_upper
                else:
                    chars.append(char)
            add("".join(chars))

        yield from produced
