import sys

from cardgen.card_model import CardModel
from cardgen.tokenizer import CardTokenizer


def print_help():
    print(
        "Usage: python3 2_inference.py [path to model.safetensors] [generation count]"
    )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_help()
        sys.exit(0)

    tokenizer: CardTokenizer = CardTokenizer("./data/full.txt")
    model: CardModel = CardModel.load_file(sys.argv[1])

    for _ in range(int(sys.argv[2])):
        start = tokenizer.encode_token("<NewCard>")
        output = model.generate_card(start)
        output_strs: list[str] = []
        for token in output[0]:
            output_strs.append(tokenizer.decode_token(token.item()))
        print(" ".join(output_strs))
