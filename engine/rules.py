class RuleEngine:

    @staticmethod
    def validate(password, settings):

        if len(password) < settings.required_min_length:
            return False

        if len(password) > settings.required_max_length:
            return False

        if settings.require_uppercase:
            if not any(c.isupper() for c in password):
                return False

        if settings.require_lowercase:
            if not any(c.islower() for c in password):
                return False

        if settings.require_number:
            if not any(c.isdigit() for c in password):
                return False

        if settings.require_symbol:
            if password.isalnum():
                return False

        return True