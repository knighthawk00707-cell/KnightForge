from itertools import product

from models.settings import DEFAULT_SUBSTITUTION_RULES


class SubstitutionEngine:

    DEFAULT_RULES = DEFAULT_SUBSTITUTION_RULES

    @staticmethod
    def generate(word, rules, mode="single"):
        if not rules:
            yield word
            return

        yield word

        if mode == "all":
            choices = []
            for char in word:
                replacements = [char]
                lower = char.lower()
                if lower in rules:
                    replacements.extend(rules[lower])
                choices.append(list(dict.fromkeys(replacements)))

            for combo in product(*choices):
                candidate = "".join(combo)
                if candidate != word:
                    yield candidate
            return

        for index, char in enumerate(word):
            lower = char.lower()
            if lower not in rules:
                continue
            for replacement in rules[lower]:
                yield word[:index] + replacement + word[index + 1 :]
