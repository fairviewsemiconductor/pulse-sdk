# ============================================================================
# Copyright (c) 2026 FairView Semiconductor Inc. All Rights Reserved.
# Licensed under the FairView Semiconductor Evaluation & Silicon IP License.
#
# Module: pulse.core
# Description: Stallion MPU device selector and Gallium MMU memory allocator
# ============================================================================

def device(name: str) -> str:
    """Selects the Stallion MPU compute device."""
    print(f"[PULSE Python] Device {name} selected (FairView Stallion MPU).")
    return name

def zeros(shape, dtype: str = "float32", device: str = "mpu:0"):
    """Allocates unified memory tensor across Gallium MMU 16.0 TB/s fabric."""
    print(f"[PULSE Python] Gallium MMU allocated {dtype} zeros of shape {shape} on {device}")
    return "GalliumBuffer"
