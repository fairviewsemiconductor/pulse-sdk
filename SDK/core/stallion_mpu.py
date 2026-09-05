"""Host PyTorch / integer GEMM golden. Not silicon.

DEFAULT instance to document is GRID=4; wide meu_count is a host sim parameter, not silicon.
"""

from typing import List

# SIM_ONLY product-scale host sim, not this drop and not 2 nm / HBM hardware.
FORMULA_SCALE_MEU = 144
FORMULA_SCALE_TILES = 576
SIM_WIDTH_GRID4 = 16  # GRID=4 → 16 PEs (INSTANCE)


class StallionMPU:
    def __init__(self, grid: int = 4, meu_count: int = SIM_WIDTH_GRID4):
        # meu_count=16 is GRID=4 INSTANCE. Pass meu_count=FORMULA_SCALE_MEU (144, SIM_ONLY) for wide host sim.
        self.grid = grid
        self.meu_count = meu_count
        self.systolic_tiles = FORMULA_SCALE_TILES if meu_count == FORMULA_SCALE_MEU else meu_count
        try:
            import torch
            self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        except ImportError:
            self.device = "cpu"

    @staticmethod
    def signed8(x: int) -> int:
        x = x & 0xFF
        return x - 256 if x >= 128 else x

    def gemm_int8(self, a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
        """Host golden: C = A @ B with signed 8-bit elements and 32-bit wrap, GRID x K x GRID."""
        n = self.grid
        k_dim = len(a[0])
        c = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                acc = 0
                for k in range(k_dim):
                    acc += self.signed8(a[i][k]) * self.signed8(b[k][j])
                acc &= 0xFFFFFFFF
                if acc >= 2**31:
                    acc -= 2**32
                c[i][j] = acc
        return c

    def execute_fp8_sparse_mma(self, a, b):
        """Host proxy (torch.matmul). Not a device kernel."""
        import torch
        a_device = a.to(self.device)
        b_device = b.to(self.device)
        mask = torch.ones_like(a_device)
        mask[:, :, 2::4] = 0
        mask[:, :, 3::4] = 0
        a_sparse = a_device * mask
        return torch.matmul(a_sparse, b_device)

    def execute_moe_expert_mma(self, tokens, expert_weights, routing_weights):
        """Host proxy (torch.matmul). SIM_ONLY width; not 144-MEU silicon."""
        import torch
        tokens_dev = tokens.to(self.device)
        weights_dev = expert_weights.to(self.device)
        routes_dev = routing_weights.to(self.device)
        mask = torch.ones_like(weights_dev)
        mask[:, :, 2::4] = 0
        mask[:, :, 3::4] = 0
        weights_sparse = weights_dev * mask
        expert_outputs = torch.matmul(tokens_dev, weights_sparse[0])
        scaled_output = expert_outputs * routes_dev.unsqueeze(-1).mean()
        return scaled_output
