"""HOST MODEL. Not JEDEC HBM4. Not 512 GB PHY."""

# SIM_ONLY product-scale numbers for host arithmetic. Not this INSTANCE (SRAM 32-bit, PHY=NONE).
FORMULA_SCALE_CAPACITY_GB = 512
FORMULA_SCALE_TB_S = 16.0
FORMULA_SCALE_BUS_BITS = 16384
SIM_WIDTH_WORDS = 256
SIM_WIDTH_BITS = 32


class GalliumMMU:
    def __init__(self, words: int = SIM_WIDTH_WORDS):
        self.mem = [0] * words
        self.bytes_transferred = 0
        self.capacity_gb = None  # not FORMULA_SCALE_CAPACITY_GB PHY
        self.stacks = None
        self.pseudo_channels = None
        self.bus_width_bits = SIM_WIDTH_BITS
        self.latency_ns = None
        self.ecc_errors_detected = 0
        self.moe_expert_swaps = 0
        self.kv_pages_allocated = 0

    def write(self, addr: int, data: int) -> None:
        self.mem[addr % len(self.mem)] = data & 0xFFFFFFFF

    def read(self, addr: int) -> int:
        return self.mem[addr % len(self.mem)]

    def allocate(self, size_bytes: int):
        """Host model no-op. Not a 512 GB PHY allocator."""
        pass

    def transfer(self, size_bytes: int) -> None:
        self.bytes_transferred += int(size_bytes)

    def swap_expert_cucu(self, expert_id: int, size_bytes: int = 64 * 1024 * 1024) -> float:
        """Host arithmetic using FORMULA_SCALE_TB_S (SIM_ONLY). Not Cu-Cu silicon."""
        self.bytes_transferred += size_bytes
        self.moe_expert_swaps += 1
        transfer_us = (size_bytes / (FORMULA_SCALE_TB_S * 1e12)) * 1e6
        return transfer_us

    def allocate_paged_attention_block(self, block_size_tokens: int = 16, num_blocks: int = 1024):
        """Host counter. Not in-silicon PagedAttention."""
        self.kv_pages_allocated += num_blocks

    def ecc_check(self) -> bool:
        return self.ecc_errors_detected == 0
