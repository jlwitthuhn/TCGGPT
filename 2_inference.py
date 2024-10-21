import argparse
import sys

from cardgen.card_model import CardModel
from cardgen.tokenizer import CardTokenizer


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Run inference for a cardgen model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    arg_parser.add_argument("model_path", help="Path to model safetensors file")
    arg_parser.add_argument("--count", default=3, type=int, help="Number of cards to generate")
    args = arg_parser.parse_args()

    model_path: str = args.model_path
    model: CardModel = CardModel.load_file(model_path)
    tokenizer_path = model_path.replace(".safetensors", ".tokenizer")
    tokenizer: CardTokenizer = CardTokenizer.load_file(tokenizer_path)

    for _ in range(args.count):
        start = tokenizer.encode_token("<NewCard>")
        output = model.generate_card(start)
        output_strs: list[str] = []
        for token in output[0]:
            output_strs.append(tokenizer.decode_token(token.item()))
        print(" ".join(output_strs))
