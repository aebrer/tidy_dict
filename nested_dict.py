class NestedDict(dict):
    def __missing__(self, key):
        self[key] = NestedDict()
        return self[key]

    def __str__(self, t=1):
        if len(self.keys()) == 0:
            if t == 1:
                t = 0
            return "\t"*(t-1) + "{Empty NestedDict}"
        elif t == 1:
            string = "NestedDict::{"
        else:
            string ="\t"*(t-1) + "{"

        for key in list(self.keys()):

            if type(self[key]) == NestedDict:
                string = string + "\n\n" + "\t"*t + str(key) + ":"
                string = string + "\n" + "\t"*t + self[key].__str__(t+1)
            else:
                string = string + "\n" + "\t"*t + str(key) + ":"
                string = string + "\t\t" + str(self[key])

        if t == 1:
            t = 0
        return string + "\n" + "\t"*t + "}"

