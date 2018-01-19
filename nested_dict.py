class NestedDict(dict):
    def __missing__(self, key):
        """
        recurse forever
        :param key:
        :return:
        """
        self[key] = NestedDict()
        return self[key]

    def __str__(self):
        """
        Print nicely-ish.
        :return:
        """
        string = "\nNestedDict::{"
        for key in self.keys():
            if type(self[key]) == NestedDict:
                string = string + "\n\n\t" + str(key) + ":"
                string = string + "\n\t" + str(self[key])
            else:
                string = string + "\n\t" + str(key) + ":"
                string = string + "\t\t" + str(self[key])
        return string + "}"

    def build_from_tuple(self, key, value=list(), end=True):
        """
        Build a dictionary from a tuple object directly. Useful if you don't know how long the combinations might be.
        :param key:
        :param value:
        :param end:
        :return:
        """
        if isinstance(key, tuple):
            if len(key) >= 2:
                if key[0] not in self:
                    self[key[0]] = NestedDict()
                return self.build_from_tuple(key[0], value, end=False).build_from_tuple(key[1:], value, end=False)
            if len(key) == 1:
                return self.build_from_tuple(key[0], value, end=True)
        else:

            if isinstance(self[key], NestedDict):
                if end:
                    self[key]["."] = value
                return self[key]
            else:
                self[key] = NestedDict()
                if end:
                    self[key]["."] = value
                return self[key]

    def get_from_tuple(self, key):
        """
        Given a tuple as a key, get the values at that nested position. Returns None if invalid.
        :param key:
        :return:
        """
        if key not in self:
            if isinstance(key, tuple):
                if len(key) >= 2:
                    root = self.get_from_tuple(key[0])
                    if isinstance(root, NestedDict):
                        return root.get_from_tuple(key[1:])
                    else:
                        return None
                if len(key) == 1:
                    return self.get_from_tuple(key[0])
        else:
            return self[key]["."]

    def is_tuple_in(self, key):
        """
        True if a given tuple has a value stored in this dictionary.
        :param key:
        :return:
        """
        return self.get_from_tuple(key) is not None


