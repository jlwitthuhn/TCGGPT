import dataclasses
import math
import os

import mlx.core as mx

from dataclasses import dataclass

from mlx import nn, utils

BASE_WIDTH = 96


@dataclass
class ModelConfig:
    block_size: int = 160
    vocab_size: int = None
    n_embd: int = BASE_WIDTH
    n_head: int = 4
    n_layer: int = 3
    n_ff_inner: int = BASE_WIDTH * 3
    dropout: float = 0.25
    bias: bool = False
    weight_tying: bool = (
        False  # True uses the same weights for token embeddings and the output linear layer, false uses separate weights
    )
    swiglu: bool = False  # True uses SwiGLU activation, false uses GELU activation
    rope: bool = False  # True uses RoPE, false uses trainable position embeddings
    rope_base: int = 10000

    def as_str(self, prefix: str = "") -> str:
        result = ""
        for field in dataclasses.fields(self):
            result += f"{prefix}{field.name}: {self.__getattribute__(field.name)}\n"
        return result[:-1]


class SelfAttention(nn.Module):

    def __init__(self, config: ModelConfig):
        super().__init__()
        assert config.n_embd % config.n_head == 0

        self.n_embd = config.n_embd
        self.n_head = config.n_head
        self.dropout = config.dropout

        # query, key, value - all concatenated
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd, bias=config.bias)
        # Output projection
        self.c_proj = nn.Linear(config.n_embd, config.n_embd, bias=config.bias)
        # Rope
        self.use_rope = config.rope
        if self.use_rope:
            head_dim = config.n_embd // config.n_head
            self.rope = nn.RoPE(head_dim, base=config.rope_base)
        # Regularization layers
        self.attn_dropout = nn.Dropout(config.dropout)
        self.resid_dropout = nn.Dropout(config.dropout)
        # Mask for -inf values
        self._mask = mx.tri(config.block_size, config.block_size)
        self._mask = self._mask.reshape(1, 1, config.block_size, config.block_size)

    def __call__(self, x: mx.array):
        B, T, C = x.shape

        q, k, v = self.c_attn(x).split((self.n_embd, 2 * self.n_embd), axis=2)

        q = q.reshape(
            (B, T, self.n_head, C // self.n_head)
        )  # Split C dimension evenly between heads -> (B, T, nh, hs)
        q = q.transpose([0, 2, 1, 3])  # Swap T and n_head axes -> (B, nh, T, hs)
        k = k.reshape((B, T, self.n_head, C // self.n_head)).transpose([0, 2, 1, 3])
        v = v.reshape((B, T, self.n_head, C // self.n_head)).transpose([0, 2, 1, 3])

        if self.use_rope:
            q = self.rope(q)
            k = self.rope(k)

        # k is transposed so dimensions are valid for (q @ k) matrix multiply
        # First two dimensions are (batch, n_head) so we don't touch those
        att = (q @ k.transpose([0, 1, 3, 2])) * (1.0 / math.sqrt(k.shape[-1]))
        att = mx.where(self._mask[:, :, :T, :T] == 0, float("-inf"), att)
        att = mx.softmax(att, axis=-1)
        att = self.attn_dropout(att)
        y = att @ v

        # Un-swap T and n_head that we swapped earlier, then combine
        y = y.transpose([0, 2, 1, 3]).reshape(B, T, C)
        y = self.c_proj(y)
        y = self.resid_dropout(y)

        return y


class FeedForward(nn.Module):

    def __init__(self, config: ModelConfig):
        super().__init__()
        self.swiglu = config.swiglu
        if self.swiglu:
            self.linear_in_silu = nn.Linear(
                config.n_embd, config.n_ff_inner, bias=config.bias
            )
            self.silu = nn.SiLU()
            self.linear_in_mult = nn.Linear(
                config.n_embd, config.n_ff_inner, bias=config.bias
            )
            self.linear_out = nn.Linear(
                config.n_ff_inner, config.n_embd, bias=config.bias
            )
        else:
            self.linear_in = nn.Linear(
                config.n_embd, config.n_ff_inner, bias=config.bias
            )
            self.gelu = nn.GELU()
            self.linear_out = nn.Linear(
                config.n_ff_inner, config.n_embd, bias=config.bias
            )
        self.dropout = nn.Dropout(config.dropout)

    def __call__(self, x: mx.array):
        if self.swiglu:
            x = self.silu(self.linear_in_silu(x)) * self.linear_in_mult(x)
            x = self.linear_out(x)
        else:
            x = self.linear_in(x)
            x = self.gelu(x)
            x = self.linear_out(x)
        x = self.dropout(x)
        return x


class Block(nn.Module):

    def __init__(self, config: ModelConfig):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.n_embd, bias=config.bias)
        self.attn = SelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.n_embd, bias=config.bias)
        self.ff = FeedForward(config)

    def __call__(self, x: mx.array):
        x = x + self.attn(self.ln_1(x))
        x = x + self.ff(self.ln_2(x))
        return x


class CardModel(nn.Module):

    def load_file(path: str):
        params = utils.tree_unflatten(list(mx.load(path).items()))
        model_config = ModelConfig()
        model_config.block_size = params["cfg_block_size"].item()
        model_config.vocab_size = params["cfg_vocab_size"].item()
        model_config.n_embd = params["cfg_n_embd"].item()
        model_config.n_head = params["cfg_n_head"].item()
        model_config.n_layer = params["cfg_n_layer"].item()
        model_config.n_ff_inner = params["cfg_n_ff_inner"].item()
        model_config.dropout = params["cfg_dropout"].item()
        model_config.bias = params["cfg_bias"].item()
        model_config.weight_tying = params["cfg_weight_tying"].item()
        model_config.swiglu = params["cfg_swiglu"].item()
        model_config.rope = params["cfg_rope"].item()
        model_config.rope_base = params["cfg_rope_base"].item()

        model = CardModel(None, model_config)
        model.update(params)
        mx.eval(model.parameters())
        return model

    def save_file(self, path: str):
        params = self.parameters()
        params["cfg_block_size"] = mx.array(self.config.block_size)
        params["cfg_vocab_size"] = mx.array(self.config.vocab_size)
        params["cfg_n_embd"] = mx.array(self.config.n_embd)
        params["cfg_n_head"] = mx.array(self.config.n_head)
        params["cfg_n_layer"] = mx.array(self.config.n_layer)
        params["cfg_n_ff_inner"] = mx.array(self.config.n_ff_inner)
        params["cfg_dropout"] = mx.array(self.config.dropout)
        params["cfg_bias"] = mx.array(self.config.bias)
        params["cfg_weight_tying"] = mx.array(self.config.weight_tying)
        params["cfg_swiglu"] = mx.array(self.config.swiglu)
        params["cfg_rope"] = mx.array(self.config.rope)
        params["cfg_rope_base"] = mx.array(self.config.rope_base)

        os.makedirs(os.path.dirname(path), exist_ok=True)
        mx.save_safetensors(path, dict(utils.tree_flatten(params)))

    def __init__(self, seed: int, config: ModelConfig):
        super().__init__()
        assert config.vocab_size is not None
        self.config = config

        if seed != None:
            mx.random.seed(seed)

        # Define layers
        self.transformer = {
            "wte": nn.Embedding(config.vocab_size, config.n_embd),  # Token Embedding
            "drop": nn.Dropout(config.dropout),  # Embedding dropout layer
            "h": [Block(config) for _ in range(config.n_layer)],  # Transformer blocks
            "ln_f": nn.LayerNorm(config.n_embd, bias=config.bias),
        }
        if config.rope == False:
            self.transformer["wpe"] = nn.Embedding(
                config.block_size, config.n_embd
            )  # Learnable position embedding

        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)

        if config.weight_tying:
            self.transformer["wte"].weight = self.lm_head.weight

    def __call__(self, tokens_in: mx.array):
        B, T = tokens_in.shape
        assert T <= self.config.block_size

        x = self.transformer["wte"](tokens_in)

        if self.config.rope == False:
            pos = mx.arange(0, T, 1, dtype=tokens_in.dtype)
            pos_embd = self.transformer["wpe"](pos)
            x = x + pos_embd

        x = self.transformer["drop"](x)
        for block in self.transformer["h"]:
            x = block(x)
        x = self.transformer["ln_f"](x)
        x = self.lm_head(x)

        return x

    def count_params(self, include_embedding=False):
        count_all = sum(p.size for _, p in utils.tree_flatten(self.parameters()))
        if include_embedding:
            return count_all
        count_embedding = 0
        if self.config.rope == False:
            count_embedding += sum(
                p.size
                for _, p in utils.tree_flatten(self.transformer["wpe"].parameters())
            )
        if self.config.weight_tying == False:
            count_embedding += sum(
                p.size
                for _, p in utils.tree_flatten(self.transformer["wte"].parameters())
            )
        return count_all - count_embedding

    def generate_card(self, separator_token: int):
        idx = mx.array([[separator_token]])
        return self.generate(idx, end_token=separator_token)

    def generate(self, idx, *, max_new_tokens=150, end_token=None, temperature=1.0):
        if isinstance(idx, list):
            idx = mx.array(idx)
        for _ in range(max_new_tokens):
            # Clip input if it is greater than context size
            if idx.shape[1] > self.config.block_size:
                idx_clipped = idx[:][-self.config.block_size :]
            else:
                idx_clipped = idx
            logits = self(idx_clipped)
            logits = logits[:, -1, :] / temperature
            ix = mx.random.categorical(logits, num_samples=1)
            assert ix.shape == (1, 1)
            if ix[0][0] == end_token:
                break
            idx = mx.concatenate([idx, ix], axis=-1)
            mx.eval(idx)
        return idx

    def loss_fn(model, x: mx.array, targets: mx.array):
        logits = model(x)
        losses = nn.losses.cross_entropy(
            logits.reshape(-1, logits.shape[-1]), targets.reshape(-1), reduction="mean"
        )
        return losses
