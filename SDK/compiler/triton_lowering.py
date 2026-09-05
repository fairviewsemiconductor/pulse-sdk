"""STUB. Returns example dicts. Not MLIR. Not Stallion ISA.

Host-only opcode packing for A1 (DMA) and B1 (MMA) may appear below.
This module is not a compiler and does not execute on a device.
"""

OP_NOP = 0x00
OP_DMA = 0xA1
OP_MMA = 0xB1
OP_SEM_WAIT = 0xC1
OP_SEM_POST = 0xC2


def pack_mma(k: int, fp8: bool = False, sparse: bool = False) -> int:
    """Host word packer. MMA opcode B1, fp8[119], sparse[118], K[47:32]. Does not run on a device."""
    word = (OP_MMA << 120) | ((1 if fp8 else 0) << 119) | ((1 if sparse else 0) << 118)
    word |= (k & 0xFFFF) << 32
    return word


def pack_dma(src: int, dst: int, length: int, ch: int = 0) -> int:
    """Host word packer. DMA opcode A1, src[95:64], dst[63:32], len[31:16], ch[9:8]. Does not run on a device."""
    word = OP_DMA << 120
    word |= (src & 0xFFFFFFFF) << 64
    word |= (dst & 0xFFFFFFFF) << 32
    word |= (length & 0xFFFF) << 16
    word |= (ch & 0x3) << 8
    return word


class TritonLoweringCompiler:
    """STUB. Returns example dicts. Not MLIR. Not a compiler."""

    def lower_attention_layer(self, q, k, v):
        return [
            {"op": "mma_fp8", "operands": (q, k), "dest": "score"},
            {"op": "softmax", "operands": ("score",), "dest": "attn_weights"},
            {"op": "mma_fp8", "operands": ("attn_weights", v), "dest": "output"},
        ]

    def lower_moe_layer(self, hidden_states, router_logits, active_experts=8):
        return [
            {"op": "moe_topk_gating", "operands": (router_logits,), "k": active_experts, "dest": "expert_mask"},
            {"op": "cucu_expert_prefetch", "operands": ("expert_mask",), "bandwidth": "FORMULA_SCALE", "dest": "meu_weights"},
            {"op": "mma_moe_sparse", "operands": (hidden_states, "meu_weights"), "dest": "moe_output"},
        ]
