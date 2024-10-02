import json

from typing import Dict, Union

from cardgen.valid_words import VALID_WORDS

SPLIT_CHARS = [".", ",", "/", '"', ":", ";", "-", "+", "'", "[", "]", "{", "}"]
DIGIT_CHARS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


def find_first_split(the_string: str) -> int:
    result: int = -1
    for split_char in SPLIT_CHARS:
        idx = the_string.find(split_char)
        if idx >= 0:
            if result == -1:
                result = idx
            else:
                result = min(result, idx)
    return result


def consume_next_token(the_string: str) -> tuple[str, str]:
    the_string = the_string.strip()

    if len(the_string) == 0:
        return None, ""

    if the_string[0] in SPLIT_CHARS or the_string[0] in DIGIT_CHARS:
        return the_string[0], the_string[1:]

    idx_space = the_string.find(" ")
    # Delimit by spaces
    if idx_space >= 0:
        maybe_token = the_string[:idx_space]
        maybe_remaining = the_string[idx_space + 1 :]

        # Also split on special characters if they are in the output token
        idx_split = find_first_split(maybe_token)

        if idx_split == -1:
            return maybe_token, maybe_remaining
        else:
            return (
                maybe_token[:idx_split],
                maybe_token[idx_split:] + " " + maybe_remaining,
            )
    else:
        # Also split on special characters if they are in the output token
        idx_split = find_first_split(the_string)
        if idx_split == -1:
            return the_string, ""
        else:
            return the_string[:idx_split], the_string[idx_split:]


class CardTokenizer:
    _id_to_string = {}
    _string_to_id = {}
    _vocab_size = 0
    _token_counts = {}

    def save_file(self, path: str):
        out_file = open(path, 'w')
        json.dump(self._string_to_id, out_file)

    def load_file(path: str):
        in_file = open(path, "r")
        loaded_dict = json.loads(in_file.read())
        assert(isinstance(loaded_dict, dict))
        return CardTokenizer(loaded_dict)

    def __init__(self, path_or_dict: Union[str, Dict[str, int]]):
        assert(path_or_dict != None)

        # Special case to load a pre-made tokenizer dict
        if isinstance(path_or_dict, dict):
            tokens_dict: dict = path_or_dict
            self._id_to_string = {id: string for string, id in tokens_dict.items()}
            self._string_to_id = {string: id for id, string in self._id_to_string.items()}
            assert(len(self._id_to_string) == len(self._string_to_id))
            self._vocab_size = len(self._id_to_string)
            return

        path: str = path_or_dict
        with open(path, "r") as file:
            cards = file.read().splitlines()

        for card in cards:
            if "<Text>" not in card:
                print(card)
                print("Card without text found")
                exit()
            remaining = card
            while True:
                token, remaining = consume_next_token(remaining)
                if token in self._token_counts:
                    self._token_counts[token] += 1
                else:
                    self._token_counts[token] = 1
                if len(remaining) == 0:
                    break

        self._vocab_size = len(self._token_counts)

        for id, token in enumerate(sorted(self._token_counts.keys())):
            self._id_to_string[id] = token
            self._string_to_id[token] = id

    def write_stats(self, path: str, exclude_valid_words: bool = False):
        with open(path, "w") as out_file:
            for token in reversed(
                sorted(self._token_counts, key=self._token_counts.get)
            ):
                if (exclude_valid_words == False) or (token not in VALID_WORDS):
                    out_file.write(f"<{token}>: {self._token_counts[token]}\n")

    def decode_token(self, token_id: int) -> str:
        assert token_id in self._id_to_string
        return self._id_to_string[token_id]

    def encode(self, strings: list[str]) -> list[list[int]]:
        result = []

        for this_string in strings:
            result.append(self._encode_single(this_string))

        return result

    def encode_token(self, token: str) -> int:
        assert token in self._string_to_id
        return self._string_to_id[token]

    def get_vocab_size(self) -> int:
        return self._vocab_size

    def _encode_single(self, the_string):
        to_encode = the_string
        this_encoded = []
        while len(to_encode.strip()) > 0:
            token, to_encode = consume_next_token(to_encode)
            assert token in self._string_to_id
            this_encoded += [self._string_to_id[token]]
        return this_encoded
