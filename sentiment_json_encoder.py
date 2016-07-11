from json import JSONEncoder

class SentimentEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, EncodableObject):
            return obj.get_json_state()
        else:
            return JSONEncoder.default(self, obj)
