import dataclasses
import math
import random

import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optimizers

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from tqdm import tqdm

from cardgen.card_model import CardModel, ModelConfig
from cardgen.tokenizer import CardTokenizer


FIRST_EVAL = 2500


@dataclass
class TrainingConfig:
    num_epochs: int = 80000
    batch_sizes: list[int] = field(default_factory=lambda: [48])
    weight_decay: float = 0.08
    learn_rate_hi: float = 1.0e-3
    learn_rate_lo: float = 1.0e-4
    eval_interval: int = 500
    eval_batch_count: int = 64

    def as_str(self, prefix: str = "") -> str:
        result = ""
        for field in dataclasses.fields(self):
            result += f"{prefix}{field.name}: {self.__getattribute__(field.name)}\n"
        return result[:-1]


@dataclass
class TrainingOutput:
    model: CardModel = None
    longest_card: int = 0
    num_params: int = 0
    duration: timedelta = None
    eval_points: list[int] = field(default_factory=lambda: [])
    test_losses: list[int] = field(default_factory=lambda: [])
    train_losses: list[int] = field(default_factory=lambda: [])

    def as_str(self, prefix: str = "") -> str:
        result = ""
        for field in dataclasses.fields(self):
            if field.name != "model":
                result += f"{prefix}{field.name}: {self.__getattribute__(field.name)}\n"
        return result[:-1]


def _load_data(tokenizer: CardTokenizer) -> tuple[list[list[int]], list[list[int]]]:
    data_train_txt = open("./data/train.txt", "r").read().splitlines()
    data_train = tokenizer.encode(data_train_txt)

    data_test_txt = open("./data/test.txt", "r").read().splitlines()
    data_test = tokenizer.encode(data_test_txt)

    random.seed(123456)
    random.shuffle(data_train)
    random.shuffle(data_test)

    return data_train, data_test


def _make_batch(
    batch_size: int, block_size: int, dataset: list[list[int]]
) -> tuple[mx.array, mx.array]:
    # Make sure each example has enough cards to fill the context
    minimum_card_sz = min([len(x) for x in dataset])
    cards_per_example = math.ceil(block_size / minimum_card_sz)
    rand_count = cards_per_example * batch_size
    rand_idx = mx.random.randint(0, len(dataset), (rand_count,))
    in_elements: list[mx.array] = []
    out_elements: list[mx.array] = []
    next_element: list[int] = []
    for i in rand_idx:
        i = i.item()
        next_element += dataset[i]
        if len(next_element) > block_size:
            # We have a full single element ready
            in_array = mx.array(next_element[:block_size])
            in_elements.append(in_array)
            out_array = mx.array(next_element[1 : block_size + 1])
            out_elements.append(out_array)
            next_element = []
        if len(in_elements) >= batch_size:
            break
    X = mx.stack(in_elements)
    Y = mx.stack(out_elements)
    assert X.shape == Y.shape
    assert X.shape == (batch_size, block_size)
    return X, Y


def _measure_loss(
    model: CardModel,
    train_config: TrainingConfig,
    model_config: ModelConfig,
    dataset: list[list[int]],
) -> float:
    BATCH_SIZE = 32
    model.train(False)
    losses: list[float] = []
    for _ in range(train_config.eval_batch_count):
        x, y = _make_batch(BATCH_SIZE, model_config.block_size, dataset)
        this_loss = model.loss_fn(x, y)
        losses.append(this_loss.item())
    return sum(losses) / len(losses)


def _get_batch_size(current: int, end: int, batch_sizes: list[int]):
    step_size = math.floor(end / len(batch_sizes)) + 1
    step = math.floor(current / step_size)
    assert step < len(batch_sizes)
    return batch_sizes[step]


def train_card_model(
    label: str, train_config: TrainingConfig, model_config: ModelConfig
) -> TrainingOutput:
    result = TrainingOutput()

    tokenizer = CardTokenizer("./data/full.txt")
    model_config.vocab_size = tokenizer.get_vocab_size()
    data_train, data_test = _load_data(tokenizer)

    result.longest_card = max([len(card) for card in data_train])

    model = CardModel(123456, model_config)
    result.num_params = model.count_params()
    mx.eval(model.parameters())
    loss_and_grad_fn = nn.value_and_grad(model, CardModel.loss_fn)
    learn_rate = optimizers.cosine_decay(
        train_config.learn_rate_hi, train_config.num_epochs, train_config.learn_rate_lo
    )
    optimizer = optimizers.AdamW(
        learning_rate=learn_rate, weight_decay=train_config.weight_decay
    )

    time_begin = datetime.now()
    for i in tqdm(range(train_config.num_epochs), desc=label):
        model.train(True)
        batch_size = _get_batch_size(
            i, train_config.num_epochs, train_config.batch_sizes
        )
        x, y = _make_batch(batch_size, model_config.block_size, data_train)

        loss, grads = loss_and_grad_fn(model, x, y)
        optimizer.update(model, grads)

        mx.eval(model.parameters(), optimizer.state, loss)

        if (i + 1) % train_config.eval_interval == 0 and (i + 1) >= FIRST_EVAL:
            result.eval_points.append(i + 1)
            loss_test = _measure_loss(model, train_config, model_config, data_test)
            result.test_losses.append(loss_test)
            loss_train = _measure_loss(model, train_config, model_config, data_train)
            result.train_losses.append(loss_train)

    result.duration = datetime.now() - time_begin

    result.model = model
    return result
