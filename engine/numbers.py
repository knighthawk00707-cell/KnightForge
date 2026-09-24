from itertools import product
import random


class NumberEngine:

    @staticmethod
    def generate(
        min_length=1,
        max_length=3,
        digits="0123456789",
        start=None,
        end=None,
        zero_padding=True,
        permutations=False,
        order="Ascending",
    ):

        min_length = max(1, int(min_length))
        max_length = max(min_length, int(max_length))

        generated = []

        def collect(value):
            generated.append(value)

        # Digit strings of every width from min_length to max_length
        if permutations:

            for length in range(min_length, max_length + 1):
                for combo in product(digits, repeat=length):
                    collect("".join(combo))

        # Numeric range, emitted at every requested width
        elif start is not None and end is not None:

            low_bound = min(start, end)
            high_bound = max(start, end)

            for length in range(min_length, max_length + 1):
                for value in NumberEngine._values_for_length(
                    length,
                    low_bound,
                    high_bound,
                    zero_padding,
                ):
                    collect(value)

        # Sequential 0 .. 10^length - 1 for every width
        else:

            for length in range(min_length, max_length + 1):
                width_max = 10 ** length - 1
                for value in NumberEngine._values_for_length(
                    length,
                    0,
                    width_max,
                    zero_padding,
                ):
                    collect(value)

        if order == "Descending":
            generated.reverse()
        elif order == "Random":
            random.shuffle(generated)

        yield from generated

    @staticmethod
    def _values_for_length(length, start, end, zero_padding):
        width_max = 10 ** length - 1
        low = start
        high = min(end, width_max)

        if not zero_padding and length > 1:
            low = max(low, 10 ** (length - 1))

        if low > high:
            return

        for number in range(low, high + 1):
            if zero_padding:
                yield str(number).zfill(length)
            else:
                text = str(number)
                if len(text) == length:
                    yield text
