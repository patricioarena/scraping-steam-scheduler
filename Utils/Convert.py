class Convert(object):
    def __init__(self):
        pass

    def to_json(self, o):
        obj = {}
        for attr, value in o.__dict__.items():
            obj[attr] = value
        return obj