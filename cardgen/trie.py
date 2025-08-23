class Trie:
    children: dict[str, "Trie"]
    terminal: bool

    def __init__(self):
        self.children = {}
        self.terminal = False

    def add(self, the_string: str) -> None:
        if len(the_string) == 0:
            self.terminal = True
            return
        the_char = the_string[0]
        if the_char not in self.children:
            self.children[the_char] = Trie()
        self.children[the_char].add(the_string[1:])

    def check(self, the_string: str) -> bool:
        if len(the_string) == 0:
            return self.terminal
        the_char = the_string[0]
        if the_char not in self.children:
            return False
        return self.children[the_char].check(the_string[1:])

    def accumulate_set(self, prefix: str, output_set: set[str]):
        if self.terminal:
            output_set.add(prefix)
        for this_char, this_child in self.children.items():
            this_child.accumulate_set(prefix + this_char, output_set)

    def to_set(self) -> set[str]:
        result = set()
        self.accumulate_set("", result)
        return result
