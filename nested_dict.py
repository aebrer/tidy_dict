def get_nested_dict_class():

    class NestedDict(dict):
        def __missing__(self, key):
            self[key] = NestedDict()
            return self[key]

        def __str__(self):
            string = "NestedDict::"

            for key in self.keys():

                if type(self[key]) == NestedDict:
                    string = string + "\n\n\t" + str(key) + ":"
                    string = string + "\n\t" + str(self[key])
                else:
                    string = string + "\n\t" + str(key) + ":"
                    string = string + "\t\t" + str(self[key])

            return string

    return NestedDict

