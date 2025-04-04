import argparse

from cardgen.card_model import CardModel
from cardgen.clean import unclean_text
from cardgen.tokenizer import CardTokenizer


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Run inference for a cardgen model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    arg_parser.add_argument("model_path", help="Path to model safetensors file")
    arg_parser.add_argument(
        "--count", default=3, type=int, help="Number of cards to generate"
    )
    arg_parser.add_argument(
        "--temp", default=1.0, type=float, help="Sampling temperature"
    )
    arg_parser.add_argument(
        "--topk",
        default=50,
        type=int,
        help="Only select from the top k most likely tokens",
    )
    args = arg_parser.parse_args()

    model_path: str = args.model_path
    model: CardModel = CardModel.load_file(model_path)
    model.eval()
    tokenizer_path = model_path.replace(".safetensors", ".tokenizer")
    tokenizer: CardTokenizer = CardTokenizer.load_file(tokenizer_path)

    for _ in range(args.count):
        start = tokenizer.encode_token("<NewCard>")
        output = model.generate_card(start, temperature=args.temp, topk=args.topk)
        output_str = tokenizer.decode(output[0].tolist())
        output_str = unclean_text(output_str)
        print(output_str)
