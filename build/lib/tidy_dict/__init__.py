"""
nested dictionary class, with automatic csv printing
"""


class TidyDict(dict):
    def __missing__(self, key):
        self[key] = TidyDict()
        return self[key]

    def __str__(self, t=1):
        '''outputs an easily readable string representation'''
        if len(self.keys()) == 0:
            if t == 1:
                t = 0
            return "\t" * (t - 1) + "{Empty TidyDict}"
        elif t == 1:
            string = "TidyDict::{"
        else:
            string = "\t" * (t - 1) + "{"

        for key in list(self.keys()):

            if type(self[key]) == TidyDict:
                string = string + "\n\n" + "\t" * t + str(key) + ":"
                string = string + "\n" + "\t" * t + self[key].__str__(t + 1)
            else:
                string = string + "\n" + "\t" * t + str(key) + ":"
                string = string + "\t\t" + str(self[key])

        if t == 1:
            t = 0
        return string + "\n" + "\t" * t + "}"

    def __repr__(self):
        '''outputs an accurate string representation that you can initialize an exact copy from'''
        if len(self.keys()) == 0:
            return "TidyDict()"
        else:
            string = "TidyDict("

        for key in list(self.keys()):

            if type(self[key]) == TidyDict:
                string += f"{key} = {self[key].__repr__()},"
            else:
                string += f"{key} = {self[key]},"

        return f"{string})"

    def to_dict(self):
        '''convert to a normal dict'''
        new_dict = {}
        for key, val in self.items():
            if type(val) == TidyDict:
                new_dict[key] = val.to_dict()
            else:
                new_dict[key] = val
        return new_dict

    def _flatten_dict(self):
        out = []
        def flatten(x, name=''):
            if type(x) is TidyDict:
                for a in x:
                    flatten(x[a], name + a + ',')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + ',')
                    i += 1
            else:
                out.append(f"{name[:-1]},{x}")

        flatten(self)
        return out

    def to_csv(self, outname=None):
        lines = self._flatten_dict()
        string = ""
        for line in lines:
            string += f"{line}\n"
        string = string.strip()
        if outname is None:
            return string
        else:
            with open(outname, "w") as outfile:
                outfile.write(string)
            return string

