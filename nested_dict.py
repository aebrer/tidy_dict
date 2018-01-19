class NestedDict(dict):
    def __missing__(self, key):
        """
        recurse forever
        :param key:
        :return:
        """
        self[key] = NestedDict()
        return self[key]

    def build_from_tuple(self, key, value, d=None):
        """
        Build a dictionary from a tuple object directly. Useful if you don't know how long the combinations might be.
        :param key:
        :param value:
        :param end:
        :return:
        """
        # first pass
        if d is None:
            if not (isinstance(key, list) or isinstance(key, tuple)):
                key = [key]
            key_list = list(key)
            depth = len(key_list)

            if depth == 1:
                self[key_list[0]]["."] = value

            else:
                temp_dict = NestedDict()
                temp_dict[key_list[0]] = temp_dict.build_from_tuple(key_list[1:], value, temp_dict)
                all_pairs = list()
                for keyi in self[key_list[0]]:
                    all_pairs.append((keyi, self[key_list[0]][keyi]))
                for keyi in temp_dict:
                    all_pairs.append((keyi, temp_dict[keyi]))
                for keyi, value in all_pairs:
                    self[key_list[0]][keyi] = value

        else:

            key_list = list(key)
            depth = len(key_list)

            if depth == 1:
                d[key_list[0]]["."] = value

            else:
                temp_dict = NestedDict()
                temp_dict[key_list[0]] = NestedDict()
                temp_dict[key_list[0]].build_from_tuple(key_list[1:], value, temp_dict)
                all_pairs = list()
                for keyi in d[key_list[0]]:
                    all_pairs.append((keyi, d[key_list[0]][keyi]))
                for keyi in temp_dict:
                    all_pairs.append((keyi, temp_dict[keyi]))
                for keyi, value in all_pairs:
                    d[key_list[0]][keyi] = value

    def get_from_tuple(self, key):
        """
        Given a tuple as a key, get the values at that nested position. Returns None if invalid.
        :param key:
        :return:
        """
        try:
            res = None
            while res is None:
                res = next(self.get_from_tuple_iter(key))
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


test = NestedDict()
test.build_from_tuple((1),[1424])
print test
test.build_from_tuple((1,2,2),[1424])
print test

test.build_from_tuple((1,4,2),[1424])

print test