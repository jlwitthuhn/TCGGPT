import os

import matplotlib.pyplot as plt

from cardgen.card_model import ModelConfig
from cardgen.trainer import train_card_model
from cardgen.trainer import TrainingConfig, TrainingOutput


def write_output(
    series_label: str,
    run_label: str,
    model_config: ModelConfig,
    train_config: TrainingConfig,
    train_out: TrainingOutput,
):
    log_contents = "ModelConfig:\n"
    log_contents += model_config.as_str("-") + "\n\n"
    log_contents += "TrainConfig:\n"
    log_contents += train_config.as_str("-") + "\n\n"
    log_contents += "TrainingOutput:\n"
    log_contents += train_out.as_str("-") + "\n"

    out_dir = f"./train_log/{series_label}"
    os.makedirs(out_dir, exist_ok=True)
    with open(f"{out_dir}/{run_label}.txt", "w") as log_file:
        log_file.write(log_contents)

    te_loss = train_out.test_losses[-1]
    tr_loss = train_out.train_losses[-1]
    bottom_text = f"Te: {te_loss:.4f} Tr: {tr_loss:.4f} Frac: {tr_loss / te_loss :.4f}"

    graph_path = f"{out_dir}/{run_label}.png"
    fig, ax = plt.subplots()
    ax.set_title(f"{run_label}\n{bottom_text}")
    ax.plot(train_out.eval_points, train_out.test_losses, label="test")
    ax.plot(train_out.eval_points, train_out.train_losses, label="train")
    ax.grid(visible=True)
    ax.legend()
    fig.savefig(graph_path)


if __name__ == "__main__":

    # Set all params here, do not rely on defaults so it is all defined in one place
    model_config = ModelConfig()
    model_config.block_size = 160
    model_config.vocab_size = None
    model_config.n_embd = 96
    model_config.n_head = 4
    model_config.n_layer = 8
    model_config.n_ff_inner = model_config.n_embd * 3
    model_config.dropout = 0.31
    model_config.bias = False
    model_config.weight_tying = False

    train_config = TrainingConfig()
    train_config.num_epochs = 75000
    train_config.batch_sizes = [16, 20, 24, 32, 48]
    train_config.weight_decay = 0.08
    train_config.learn_rate_hi = 1.0e-3
    train_config.learn_rate_lo = 1.0e-4
    train_config.warmup_steps = 500
    train_config.eval_interval = 500
    train_config.eval_batch_count = 64

    series = "default"

    label = "model"
    result = train_card_model(label, train_config, model_config)
    write_output(series, label, model_config, train_config, result)
    result.model.save_file(f"./model/{label}.safetensors")
