from dataclasses import dataclass, field


DEFAULT_SUBSTITUTION_RULES = {
    "a": ["@", "4"],
    "e": ["3"],
    "i": ["1", "!"],
    "o": ["0"],
    "s": ["$", "5"],
    "t": ["7", "+"],
}


COMMON_SUFFIXES = [
    "1",
    "12",
    "123",
    "1234",
    "12345",
    "111",
    "000",
    "007",
    "69",
    "99",
    "13",
]


@dataclass
class GeneratorSettings:

    # ======================================
    # Base Data
    # ======================================

    base_strings: list = field(default_factory=list)

    use_case: bool = True
    case_lowercase: bool = True
    case_uppercase: bool = False
    case_capitalize: bool = True
    case_alternate: bool = False

    # ======================================
    # Number Generation
    # ======================================

    use_numbers: bool = True

    min_length: int = 1
    max_length: int = 4

    range_from: int = 0
    range_to: int = 9999

    zero_padding: bool = True
    permutations: bool = False
    number_order: str = "Ascending"

    # ======================================
    # Symbols
    # ======================================

    symbols: list = field(
        default_factory=lambda: [
            "!",
            "@",
            "#",
            "$",
        ]
    )
    symbol_mode: str = "ends"

    # ======================================
    # Substitutions
    # ======================================

    use_substitutions: bool = True
    substitution_mode: str = "single"
    substitution_rules: dict = field(default_factory=dict)

    # ======================================
    # Extra transforms
    # ======================================

    use_reverse: bool = False
    use_duplicate: bool = False
    combine_bases: bool = False
    use_common_suffixes: bool = False
    append_years: bool = False
    year_from: int = 1990
    year_to: int = 2026

    # ======================================
    # Placement
    # ======================================

    placement: dict = field(default_factory=dict)

    # ======================================
    # Length filter
    # ======================================

    min_password_length: int = 0
    max_password_length: int = 0

    # ======================================
    # Export
    # ======================================

    remove_duplicates: bool = True
    sort_results: bool = False
    estimate_only: bool = False
