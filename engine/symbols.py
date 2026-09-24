class SymbolEngine:

    @staticmethod
    def generate(password, symbols, mode="ends"):
        if not symbols:
            return

        for symbol in symbols:
            if mode == "suffix":
                yield password + symbol
            elif mode == "prefix":
                yield symbol + password
            elif mode == "wrap":
                yield symbol + password + symbol
            elif mode == "all":
                for i in range(len(password) + 1):
                    yield password[:i] + symbol + password[i:]
            else:
                yield symbol + password
                yield password + symbol
