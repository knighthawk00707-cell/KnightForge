class Pipeline:

    def __init__(self):

        self.rules = []

    def add_rule(self, rule):

        self.rules.append(rule)

    def run(self, words):

        result = words

        for rule in self.rules:

            result = rule.apply(result)

        return result