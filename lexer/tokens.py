class Token:
    def __init__(self, coord, type, code, value):
        self.coord = coord
        self.type = type
        self.code = code
        self.value = value

    def getCoord(self):
        return self.coord

    def getType(self):
        return self.type

    def getCode(self):
        return self.code

    def getValue(self):
        return self.value

    def getTokens(self):
        if self.notEOF():
            return f'{self.coord}    {self.type}    {self.value}    {self.code}'
        return ''

    def notEOF(self):
        return self.type != "EOF"