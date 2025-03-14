class BaseLM:
    def __init__(self, name: str):
        if not name.count('/') == 1:
            raise NameError()
        self.organization, self.model = name.split('/')