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
        try:
            res = None
            while res is None:
                res = self.get_from_tuple_iter(key).next()
            return res
        except:
            return None

    def get_from_tuple_iter(self, key, d=None):
        # first pass
        if d is None:
            if not (isinstance(key, list) or isinstance(key, tuple)):
                key = [key]
            key_list = list(key)
            depth = len(key_list)
            if key_list[0] in self.keys() or "." in self.keys():
                if depth == 1:
                    for i in self.values():
                        if isinstance(i, NestedDict):
                            yield i["."]
                else:
                    for v in self.values():
                        if isinstance(v, NestedDict):
                            for i in self.get_from_tuple_iter(key_list[1:], v):
                                yield i
        else:
            key_list = list(key)
            depth = len(key_list)

            if key_list[0] in d.keys() or "." in d.keys():
                if depth == 1:
                    if key_list[0] in d.keys():
                        for i in d.values():
                            if isinstance(i, NestedDict):
                                yield i["."]
                else:
                    for v in d.values():
                        if isinstance(v, NestedDict):
                            for i in d.get_from_tuple_iter(key_list[1:], v):
                                yield i
