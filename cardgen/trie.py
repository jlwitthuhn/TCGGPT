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

    def replace_longest_match(self, full_string: str, replacement: str) -> (str, bool):
        end_index: int = len(full_string)
        best_index: int = 0
        best_length: int = 0
        for i in range(end_index):
            match_length = self._find_match_beginning(full_string, replacement, i)
            if match_length > best_length:
                best_index = i
                best_length = match_length
        if best_length > 0:
            return (
                full_string[:best_index]
                + replacement
                + full_string[best_index + best_length :],
                True,
            )
        else:
            return full_string, False

    # Returns the length of a match, 0 for no match
    def _find_match_beginning(
        self, full_string: str, replacement: str, index: int
    ) -> int:
        end_index: int = len(full_string)
        match_length: int = 0
        node: Trie = self
        for i in range(index, end_index):
            letter = full_string[i]
            if letter in node.children:
                node = node.children[letter]
                if node.terminal:
                    match_length = (i - index) + 1
            else:
                break
        return match_length
