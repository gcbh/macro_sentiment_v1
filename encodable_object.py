class EncodableObject(object):
    def __init__(self):
        object.__init__(self)
    def get_json_state(self):
        return self.__dict__
