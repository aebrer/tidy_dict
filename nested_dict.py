class NestedDict(dict):
    def __missing__(self, key):
        self[key] = NestedDict()
        return self[key]

    def __str__(self):
        string = "\nNestedDict::{"

        for key in self.keys():
            if type(self[key]) == NestedDict:
                string = string + "\n\n\t" + str(key) + ":"
                string = string + "\n\t" + str(self[key])
            else:
                string = string + "\n\t" + str(key) + ":"
                string = string + "\t\t" + str(self[key])
        return string + "}"

    def build(self, key):
        if key not in self:
            if isinstance(key, tuple):
                if len(key) >= 2:
                    self[key[0]] = NestedDict()
                    return self.build(key[0]).build(key[1:])
                if len(key) == 1:
                    self[key[0]] = list()
                    return self.build(key[0])
        else:
            return self[key]

    def get(self, key):
        if key not in self:
            if isinstance(key, tuple):
                if len(key) >= 2:
                    return self.get(key[0]).get(key[1:])
                if len(key) == 1:
                    return self.get(key[0])
        else:
            return self[key]

