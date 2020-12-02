class Prefixes:

    def __init__(self):
        super().__init__()
        self.prefixInfo = [[545901826776760340, '%']]

    def getPrefix(self, guild):
        for data in self.prefixInfo:
            if data[0] == guild:
                return data[1]
        return "!"

    def setPrefix(self, guild, prefix):
        count = 0
        for data in self.prefixInfo:
            if data[0] == guild:
                self.prefixInfo.pop(count)
                self.prefixInfo.append([guild, prefix])
            else:
                count = count + 1
        
        self.prefixInfo.append([guild, prefix])
        return prefix

    def showPrefixes(self):
        print(self.prefixInfo)