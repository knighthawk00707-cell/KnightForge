class FilterEngine:

    @staticmethod
    def valid(password, settings):
        minimum = getattr(settings, "min_password_length", 0) or 0
        maximum = getattr(settings, "max_password_length", 0) or 0

        if minimum > 0 and len(password) < minimum:
            return False

        if maximum > 0 and len(password) > maximum:
            return False

        return True
