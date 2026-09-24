from itertools import permutations


class TransformEngine:

    @staticmethod
    def expand(
        bases,
        combine=False,
        reverse=False,
        duplicate=False,
    ):
        expanded = list(dict.fromkeys(bases))

        if combine and len(expanded) > 1:
            combined = []
            for left, right in permutations(expanded, 2):
                combined.append(left + right)
            expanded.extend(combined)

        extras = []

        snapshot = list(expanded)

        if reverse:
            extras.extend(item[::-1] for item in snapshot if item)

        if duplicate:
            extras.extend(item + item for item in snapshot if item)

        expanded.extend(extras)

        return list(dict.fromkeys(expanded))
