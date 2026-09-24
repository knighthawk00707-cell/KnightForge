from engine.filter import FilterEngine
from engine.numbers import NumberEngine
from engine.placement import PlacementEngine
from engine.strings import StringEngine
from engine.substitutions import SubstitutionEngine
from engine.symbols import SymbolEngine
from engine.transforms import TransformEngine
from models.settings import COMMON_SUFFIXES, DEFAULT_SUBSTITUTION_RULES


class PasswordGenerator:

    @staticmethod
    def generate(settings):
        seen = set() if getattr(settings, "remove_duplicates", True) else None

        for password in PasswordGenerator._candidates(settings):
            if not FilterEngine.valid(password, settings):
                continue

            if seen is not None:
                if password in seen:
                    continue
                seen.add(password)

            yield password

    @staticmethod
    def _candidates(settings):
        string_pool = []

        for text in settings.base_strings:
            if not text:
                continue

            text = text.strip()
            if not text:
                continue

            if getattr(settings, "use_case", True):
                string_pool.extend(
                    StringEngine.generate_cases(
                        text,
                        lowercase=getattr(settings, "case_lowercase", True),
                        uppercase=getattr(settings, "case_uppercase", False),
                        capitalize=getattr(settings, "case_capitalize", True),
                        alternate=getattr(settings, "case_alternate", False),
                    )
                )
            else:
                string_pool.append(text)

        string_pool = TransformEngine.expand(
            string_pool,
            combine=getattr(settings, "combine_bases", False),
            reverse=getattr(settings, "use_reverse", False),
            duplicate=getattr(settings, "use_duplicate", False),
        )

        if getattr(settings, "use_substitutions", True):
            rules = settings.substitution_rules or DEFAULT_SUBSTITUTION_RULES
            substitution_mode = getattr(settings, "substitution_mode", "single")
        else:
            rules = {}
            substitution_mode = "single"

        insert_values = list(PasswordGenerator._inserts(settings))
        symbol_mode = getattr(settings, "symbol_mode", "ends")
        symbols = settings.symbols or []

        for original in string_pool:
            for substituted in SubstitutionEngine.generate(
                original,
                rules,
                mode=substitution_mode,
            ):
                yield substituted

                yield from SymbolEngine.generate(
                    substituted,
                    symbols,
                    mode=symbol_mode,
                )

                for insert in insert_values:
                    for placed in PlacementEngine.generate(
                        substituted,
                        insert,
                        settings.placement,
                    ):
                        yield placed
                        yield from SymbolEngine.generate(
                            placed,
                            symbols,
                            mode=symbol_mode,
                        )

    @staticmethod
    def _inserts(settings):
        values = []

        if getattr(settings, "use_numbers", True):
            values.extend(
                NumberEngine.generate(
                    min_length=settings.min_length,
                    max_length=settings.max_length,
                    start=settings.range_from,
                    end=settings.range_to,
                    zero_padding=settings.zero_padding,
                    permutations=settings.permutations,
                    order=settings.number_order,
                )
            )

        if getattr(settings, "use_common_suffixes", False):
            values.extend(COMMON_SUFFIXES)

        if getattr(settings, "append_years", False):
            year_from = getattr(settings, "year_from", 1990)
            year_to = getattr(settings, "year_to", 2026)
            start = min(year_from, year_to)
            end = max(year_from, year_to)
            values.extend(str(year) for year in range(start, end + 1))

        return list(dict.fromkeys(values))
