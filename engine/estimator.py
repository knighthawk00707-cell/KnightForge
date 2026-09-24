class PasswordEstimator:

    @staticmethod
    def estimate(settings):
        string_count = max(len(settings.base_strings), 1)
        total = string_count

        case_variations = 0
        if getattr(settings, "case_lowercase", True):
            case_variations += 1
        if getattr(settings, "case_uppercase", False):
            case_variations += 1
        if getattr(settings, "case_capitalize", True):
            case_variations += 1
        if getattr(settings, "case_alternate", False):
            case_variations += 1
        if not getattr(settings, "use_case", True):
            case_variations = 1

        total *= max(case_variations, 1)

        if getattr(settings, "combine_bases", False) and string_count > 1:
            total += string_count * (string_count - 1)

        if getattr(settings, "use_reverse", False):
            total *= 2

        if getattr(settings, "use_duplicate", False):
            total *= 2

        if getattr(settings, "use_substitutions", True):
            if getattr(settings, "substitution_mode", "single") == "all":
                total *= 8
            else:
                total *= 4

        insert_count = 1
        if getattr(settings, "use_numbers", True):
            min_length = max(1, settings.min_length)
            max_length = max(min_length, settings.max_length)
            start = min(settings.range_from, settings.range_to)
            end = max(settings.range_from, settings.range_to)

            if getattr(settings, "permutations", False):
                for length in range(min_length, max_length + 1):
                    insert_count += 10 ** length
            else:
                for length in range(min_length, max_length + 1):
                    width_max = 10 ** length - 1
                    low = start
                    high = min(end, width_max)
                    if not settings.zero_padding and length > 1:
                        low = max(low, 10 ** (length - 1))
                    if high >= low:
                        insert_count += high - low + 1

        if getattr(settings, "use_common_suffixes", False):
            insert_count += 11

        if getattr(settings, "append_years", False):
            year_from = getattr(settings, "year_from", 1990)
            year_to = getattr(settings, "year_to", 2026)
            insert_count += abs(year_to - year_from) + 1

        total *= max(insert_count, 1)

        symbol_count = len(settings.symbols or [])
        if symbol_count:
            mode = getattr(settings, "symbol_mode", "ends")
            if mode == "all":
                total *= 1 + symbol_count * 8
            elif mode in ("suffix", "prefix", "wrap"):
                total *= 1 + symbol_count
            else:
                total *= 1 + symbol_count * 2

        return max(int(total), 0)
