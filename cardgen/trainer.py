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


@dataclass
class TrainingConfig:
    num_epochs: int = 80000
    first_eval_epoch: int = 3000
    batch_sizes: list[int] = field(default_factory=lambda: [48])
    weight_decay: float = 0.08
    learn_rate_hi: float = 1.0e-3
    learn_rate_lo: float = 1.0e-4
    warmup_steps: int = 500
    eval_interval: int = 500
    eval_batch_count: int = 20
    eval_batch_size: int = 128

    def as_str(self, prefix: str = "") -> str:
        result = ""
        for field in dataclasses.fields(self):
            result += f"{prefix}{field.name}: {self.__getattribute__(field.name)}\n"
        return result[:-1]


@dataclass
class TrainingOutput:
    model: CardModel = None
    tokenizer: CardTokenizer = None
    longest_card: int = 0
    num_params: int = 0
    duration: timedelta = None
    eval_points: list[int] = field(default_factory=lambda: [])
    test_losses: list[int] = field(default_factory=lambda: [])
    train_losses: list[int] = field(default_factory=lambda: [])

    def as_str(self, prefix: str = "") -> str:
        result = ""
        for field in dataclasses.fields(self):
            if field.name != "model" and field.name != "tokenizer":
                result += f"{prefix}{field.name}: {self.__getattribute__(field.name)}\n"
        return result[:-1]


class _BatchLoader:
    data_test: list[list[int]]
    data_train: list[list[int]]

    remaining_train: list[list[int]]

    cycles_train: int = 0

    def __init__(self, data_train: list[list[int]], data_test: list[list[int]]):
        self.data_test = data_test
        self.data_train = data_train
        self.remaining_train = []

    def gen_batch(
        self,
        batch_size: int,
        block_size: int,
        *,
        use_test: bool = False,
        even_distribution: bool = False,
    ):
        if use_test:
            source_dataset = self.data_test
        else:
            source_dataset = self.data_train

        if even_distribution:
            assert use_test == False

            def get_card() -> list[int]:
                if len(self.remaining_train) == 0:
                    self.remaining_train = source_dataset.copy()
                    random.seed(12345 + self.cycles_train)
                    random.shuffle(self.remaining_train)
                    self.cycles_train += 1
                return self.remaining_train.pop()

        else:

            def get_card() -> list[int]:
                max_index = len(source_dataset)
                index = random.randint(0, max_index - 1)
                return source_dataset[index]

        in_list: list[mx.array] = []
        out_list: list[mx.array] = []
        for _ in range(batch_size):
            this_line: list[int] = []
            while len(this_line) < (block_size + 1):
                this_line.extend(get_card())
            in_array = mx.array(this_line[:block_size])
            in_list.append(in_array)
            out_array = mx.array(this_line[1 : block_size + 1])
            out_list.append(out_array)

        inputs = mx.stack(in_list)
        outputs = mx.stack(out_list)
        assert inputs.shape == outputs.shape
        assert inputs.shape == (batch_size, block_size)
        return inputs, outputs


def _load_data(tokenizer: CardTokenizer) -> tuple[list[list[int]], list[list[int]]]:
    data_train_txt = open("./data/train.txt", "r").read().splitlines()
    data_train = tokenizer.encode(data_train_txt)

    data_test_txt = open("./data/test.txt", "r").read().splitlines()
    data_test = tokenizer.encode(data_test_txt)

    return data_train, data_test


def _measure_loss(
    model: CardModel,
    train_config: TrainingConfig,
    model_config: ModelConfig,
    batch_loader: _BatchLoader,
    use_test: bool,
    batch_count_multiplier: int,
) -> float:
    model.train(False)
    losses: list[float] = []
    for _ in range(train_config.eval_batch_count * batch_count_multiplier):
        x, y = batch_loader.gen_batch(
            train_config.eval_batch_size, model_config.block_size, use_test=use_test
        )
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
    result.tokenizer = tokenizer
    model_config.vocab_size = tokenizer.get_vocab_size()
    data_train, data_test = _load_data(tokenizer)
    batch_loader = _BatchLoader(data_train, data_test)

    result.longest_card = max([len(card) for card in data_train])

    model = CardModel(123456, model_config)
    result.num_params = model.count_params()
    mx.eval(model.parameters())
    loss_and_grad_fn = nn.value_and_grad(model, CardModel.loss_fn)

    normal_steps: int = train_config.num_epochs - train_config.warmup_steps
    decay_lr = optimizers.cosine_decay(
        train_config.learn_rate_hi, normal_steps, train_config.learn_rate_lo
    )
    if train_config.warmup_steps > 0:
        warmup_lr = optimizers.linear_schedule(
            train_config.learn_rate_hi / 100,
            train_config.learn_rate_hi,
            train_config.warmup_steps,
        )
        learn_rate = optimizers.join_schedules(
            [warmup_lr, decay_lr], [train_config.warmup_steps]
        )
    else:
        learn_rate = decay_lr

    optimizer = optimizers.AdamW(
        learning_rate=learn_rate, weight_decay=train_config.weight_decay
    )

    time_begin = datetime.now()
    progress_bar = tqdm(range(train_config.num_epochs), desc=label)
    for i in progress_bar:
        model.train(True)
        batch_size = _get_batch_size(
            i, train_config.num_epochs, train_config.batch_sizes
        )
        x, y = batch_loader.gen_batch(
            batch_size, model_config.block_size, even_distribution=True
        )

        loss, grads = loss_and_grad_fn(model, x, y)
        optimizer.update(model, grads)

        mx.eval(model.parameters(), optimizer.state, loss)

        iter_n: int = i + 1
        if (
            iter_n % train_config.eval_interval == 0
            and iter_n >= train_config.first_eval_epoch
        ):
            if iter_n == train_config.num_epochs:
                batch_multiplier = 2
            else:
                batch_multiplier = 1
            result.eval_points.append(iter_n)
            loss_test = _measure_loss(
                model, train_config, model_config, batch_loader, True, batch_multiplier
            )
            result.test_losses.append(loss_test)
            loss_train = _measure_loss(
                model, train_config, model_config, batch_loader, False, batch_multiplier
            )
            result.train_losses.append(loss_train)
            progress_bar.set_description(
                f"{label} Te:{loss_test:4f} Tr:{loss_train:4f}"
            )

    result.duration = datetime.now() - time_begin

    result.model = model
    return result
