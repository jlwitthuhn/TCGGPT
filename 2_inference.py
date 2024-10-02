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

    model_path: str = sys.argv[1]
    model: CardModel = CardModel.load_file(model_path)
    tokenizer_path = model_path.replace(".safetensors", ".tokenizer")
    tokenizer: CardTokenizer = CardTokenizer.load_file(tokenizer_path)

    for _ in range(int(sys.argv[2])):
        start = tokenizer.encode_token("<NewCard>")
        output = model.generate_card(start)
        output_strs: list[str] = []
        for token in output[0]:
            output_strs.append(tokenizer.decode_token(token.item()))
        print(" ".join(output_strs))
