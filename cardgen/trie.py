# Like a trie but it doesn't track if intermediate-length strings are included


class AlmostTrie:
    children: dict[str, "AlmostTrie"]

    def __init__(self):
        self.children = {}

    def add(self, the_string: str) -> None:
        if len(the_string) == 0:
            return
        the_char = the_string[0]
        if the_char not in self.children:
            self.children[the_char] = AlmostTrie()
        self.children[the_char].add(the_string[1:])

    def check(self, the_string: str) -> bool:
        if len(the_string) == 0:
            return True
        the_char = the_string[0]
        if the_char not in self.children:
            return False
        return self.children[the_char].check(the_string[1:])

    def accumulate_set(self, prefix: str, output_set: set[str]):
        if len(self.children) == 0:
            output_set.add(prefix)
            return
        for this_char, this_child in self.children.items():
            this_child.accumulate_set(prefix + this_char, output_set)

    def to_set(self) -> set[str]:
        result = set()
        self.accumulate_set("", result)
        return result
