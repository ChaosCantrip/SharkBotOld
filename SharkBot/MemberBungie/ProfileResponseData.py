class ProfileResponseData:

    def __init__(self, data: dict):
        self.data = data

    def __getattr__(self, item):
        return self.data[item]
