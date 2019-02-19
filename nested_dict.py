"""
nested dictionary class, for easy sparse matrices
"""

class NestedDict(dict):
    def __missing__(self, key):
        self[key] = NestedDict()
        return self[key]

    def __str__(self, t=1):
        '''outputs an easily readable string representation'''
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

    def __repr__(self):
        '''outputs an accurate string representation that you can initialize an exact copy from'''
        if len(self.keys()) == 0:
            return "NestedDict()"
        else:
            string = "NestedDict("

        for key in list(self.keys()):

            if type(self[key]) == NestedDict:
                string += f"{key} = {self[key].__repr__()},"
            else:
                string += f"{key} = {self[key]},"

        return f"{string})"

    def to_dict(self):
        '''convert to a normal dict'''
        new_dict = {}
        for key, val in self.items():
            if type(val) == NestedDict:
                new_dict[key] = val.to_dict()
            else:
                new_dict[key] = val
        return new_dict

