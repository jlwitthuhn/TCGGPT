# TCGGPT

TCGGPT is a series of python scripts that can be used to train and run inference with a ~1-million parameter transformer-based model capable of generating the mechanically-relevant portions of Magic: The Gathering cards.

TCGGPT is built on MLX and will only run on Macs with an Apple Silicon processor.

This repo does not contain the model or training data, just the scripts needed to build and run the model. A standard training run takes 25 minutes and a full training run takes 1 hour and 15 minutes on my M4 Max MBP.

## Example Output

The character `|` represents a new line in the rules text.

```
<Type> artifact
<ManaCost> {4}
<Text> {1} , {t} , sacrifice ~ : target attacking creature get - 4 / - 4 until end of turn .
```

```
<Type> instant
<ManaCost> {1} {u}
<Text> replicate {2} {u} | counter target spell unless its controller pays {1} . 
```

```
<Type> creature - - beast beast
<ManaCost> {4} {g}
<Stats> 3 / 3
<Text> {u} : ~ gains hexproof until end of turn .
```

It also frequently produces nonsense.
```
<Type> enchantment
<ManaCost> {2} {r}
<Text> whenever you cast a spell that targets a creature or that shares a creature type with at the end step , ~ deals 2 damage to any target .
```

## Running the Scripts

### Running a pre-built model

Pre-trained models are available on the [Releases](https://github.com/jlwitthuhn/TCGGPT/releases) page. When you are using a pre-trained model, be sure that you are also using the inference script from the git tag attached to that release. Sometimes backwards-incompatible changes will be made to the model architecture.

First, download the latest release `models.zip` as well as the source code. The zip file will just contain two files, a model and a tokenizer. These two files must both exist in the same directory and have the same name (before extension). You can just drop both of them into the repository root.

When the model files are in place, you can run `python 2_inference.py ./model_full.safetensors`.

### Building and running the model

Before beginning, you will need the raw data to train the network. You can download a json file in the appropriate format from [Scryfall's Bulk Data page](https://scryfall.com/docs/api/bulk-data). The best set for training is 'Oracle Cards' because it is de-duplicated by card name.

For this section, I will assume you have downloaded the oracle json file and placed it on the path `./data/raw/oracle-cards.json`.

1. Create a new virtualenv and install the python dependencies.
    * `pip install -r ./requirements.txt`
2. Run the preprocess script to extract the data from the oracle json file. This will produce a few files in `./data/`.
    * `python ./0_preprocess.py ./data/raw/oracle-cards.json`
3. Run the training script to train the network with default configuration. This will produce a model file at `./model/model.safetensors` and a tokenizer definition at `./model/model.tokenizer`. It will also write some details about the training run to `./train_log/default/`.
    * `python ./1_train_model.py`
    * By default this will do a 'fast' training run which will result in a slightly lower quality model that will train 3x faster. You can use the argument `--full` to do a full length training run instead.
4. Run the inference script to generate any number of cards. Cards are delimited by the string `<NewCard>`.
    * `python ./2_inference.py ./model/model.safetensors --count 5`
    * This will automatically locate the tokenizer definition by replacing `.safetensors` with `.tokenizer` in the model path.
    * Run `python ./2_inference.py --help` to see available inference options.

## Architecture

The architecture of this model is largely a copy of Andrej Karpathy's [nanoGPT](https://github.com/karpathy/nanoGPT), which itself it based on GPT-2, with some minor modifications and re-tuned hyperparameters. It has also been extended to support some more modern features including SwiGLU feed-forward blocks and RoPE.

Because this is a very small model at around 1 million paramaters, it has no chance of being trained as a general purpose language model capable of outputting coherent natural language. Instead, it is designed around the fact that Magic: The Gathering cards are written in a very strict subset of English with many common words and phrases being repeated on thousands of different cards.

This model is broadly capable of outputting cards that make sense with respect to:
* Effects cards can have
* How multiple effects can be composed into one card
* Permanents having static/triggered/activatable effects and instants/sorceries having immediate effects.
* Which effects correlate with which card types and mana types (blue for card draw, red for direct damage, etc).

It struggles to ensure that a card's 'strength' is proportional to its mana cost.

### Tokenization

This model uses whole-word tokenization because we only want it to output words that are found in the training data set and it does not need to understand unseen words as input. Tokenization is case-insensitive.

### Input Data

To facilitate letting the model learn all of the above information, we want to make sure we feed it only data that is directly relevant to how a card functions in the game. For now, this means that we only care about:
* Type line
* Mana cost
* Rules text
* Stats (creatures only)

Things like card name and flavor text do not follow MTG's strict templating rules and use unique words and phrases that are rarely repeated in the training data, so the model will only be made less effective by their presence.

#### Cleaning the Data

The raw data from scryfall is cleaned in a way to help the model learn meaningful associations between different tokens. This is accomplished by replacing rare tokens with more generic tokens as described below, as well as decomposing nouns and verbs.

1. Anywhere a card references itself in rules text, its name is replaced by `~`.
2. Anywhere a card references another card by name, the name is replaced by `$named_card$`.
3. Flavor ability words are replaced by `$flavor_ability_word$`.
4. Any time a card creates a permanent, the permanent's name is replaced by `$named_permanent$`.
5. When any counter is created by two or fewer cards, the counter's name is replaced by `$unique_counter$`.
6. Any planeswalker type that appears on two or fewer cards is replaced with `$unique_planeswalker_type$`.
7. Some plural words are decomposed into the singular version of the word followed by `*s`. (ex: `creatures` -> `creature *s`)
8. Some verbs are decomposed into a base verb followed by a suffix. (ex: `tapped` -> ``tap `ed``)

## Training Loss

A graph of the training loss across train and test sets when trained on the scryfall oracle dump from July 3, 2024:
![Training Loss](./img/loss.png)
