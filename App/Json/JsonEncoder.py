from json import JSONEncoder

class JsonEncoder(JSONEncoder):
    @staticmethod
    def prepare(text):
        try:
            return text[text.index('__') + 2:]
        except ValueError:
            return text

    def default(self, o):
        print(o.get_title())
        return {self.prepare(k): v for k, v in vars(o).items()}
