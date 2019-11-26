"""
nested dictionary class, with automatic csv printing
"""
import collections


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
        n = len(lines)
        if outname:
            assert isinstance(outname, str)
            with open(outname, "w") as outfile:
                for i, line in enumerate(lines):
                    if i < n-1:
                        outfile.write(f"{line}\n")
                    else:
                        outfile.write(line)
            print(f"Saved csv to: {outname}")
        return lines


def load_csv_to_tidydict(*, csv_in: str, value_type: str = "float"):

    """
    :param csv_in: a string with the location of a tidy CSV, with no header
    :param value_type: a string, either "float", "int", or "str"
    :return: TidyDict
    """
    td = TidyDict()

    def combine_td(td, td_frag):
        for k, v in td_frag.items():
            if (k in td and isinstance(td[k], TidyDict)
                    and isinstance(td_frag[k], collections.Mapping)):
                combine_td(td[k], td_frag[k])
            else:
                td[k] = td_frag[k]

    with open(csv_in, "r") as filein:
        for line in filein:
            split_line = line.strip().split(",")
            n = len(split_line)
            split_line.reverse()
            value = None
            old_td = TidyDict()
            for i, key in enumerate(split_line):
                if i == 0:
                    if value_type == "float":
                        value = float(key)
                    elif value_type == "int":
                        value = int(key)
                    elif value_type == "str":
                        value = str(key)
                elif i == 1:
                    old_td[key] = value
                else:
                    new_td = TidyDict()
                    new_td[key] = old_td
                    old_td = new_td

            combine_td(td, old_td)

    return td

