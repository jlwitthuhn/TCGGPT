import argparse
import random


def print_random_card_from_file(path: str, count: int):
    try:
        with open(path, "r") as file:
            lines = file.readlines()
            if len(lines) == 0:
                print("The file is empty.")
                return
            for _ in range(count):
                this_card = random.choice(lines).strip()
                this_card = this_card.replace("<NewCard> ", "--------\n")
                this_card = this_card.replace("<Type> ", "<Type>\n")
                this_card = this_card.replace("<ManaCost> ", "\n<ManaCost>\n")
                this_card = this_card.replace("<Stats> ", "\n<Stats>\n")
                this_card = this_card.replace("<Text> ", "\n<Text>\n")
                this_card = this_card.replace("| ", "\n")
                print(this_card)
    except FileNotFoundError:
        print(f"File '{path}' not found.")
    except Exception as e:
        print(f"Caught exception: {e}")


def main():
    arg_parser = argparse.ArgumentParser(
        description="Display some amount of random card from training data",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    arg_parser.add_argument("path", help="Path to the training data file")
    arg_parser.add_argument(
        "--count",
        default=3,
        type=int,
        help="Number of random cards to read",
    )
    args = arg_parser.parse_args()
    print_random_card_from_file(args.path, args.count)


if __name__ == "__main__":
    main()
