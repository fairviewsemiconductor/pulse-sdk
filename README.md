# PULSE SDK — Pre-silicon host runtime

PULSE is the **host-side programming interface** for Fairview pre-silicon bring-up.
It is not CUDA, not a device driver, and not connected to a foundry GDS.

**INSTANCE:** GRID=4 (16 PEs), 1 engine, PHY=NONE, SRAM 32-bit.

This repository does not contain RTL, Sky130 GDS, or `fv_chip_top`.
Nine RTL testbenches live in a separate private tree. This SDK does not drive silicon.

Stallion/Gallium product-scale numbers (144 MEU, 576 engines, 16 TB/s HBM4, 4.72 PFLOPS, 2 nm, 350W, sub-8 ns, CUDA/ROCm-class) are FORMULA, not this drop.

## What runs here

- PyTorch CPU/MPS matmul helpers and a small integer GEMM golden
- Language wrappers (C, C++, Python, Rust, Go)
- Host ISA word packer for opcodes A1 (DMA) and B1 (MMA) — does not execute on a device

## What does not run

- HBM4, JEDEC PHY, 16 TB/s, 512 GB
- Kubernetes DevicePlugin as production
- Triton → Stallion ISA compiler / torch.compile Inductor backend
- 144 MEU silicon
- FreeToken as UC Berkeley hardware

## Hardware evidence

Fairview pre-silicon pack (**RTL repo**), not this README.

## Gate (this repo)

`SDK/pulse/run_all_tests.sh` compiles and runs C, C++, Python, Rust, and Go **wrapper smoke tests**.
It does not run RTL TBs, OpenLane, STA, or a device.

---

# WITHDRAWN DRAFT

> **WITHDRAWN** — product-scale claims below are not implemented.
> See README INSTANCE above. Do not cite 16 TB/s, 4.72 PFLOPS, CUDA-equivalent, or 144-MEU hardware.

## ⚡ Executive Overview

**FairView Semiconductor** is pioneering purpose-built, high-efficiency AI compute by unifying deterministic systolic matrix processors with ultra-wide 16.0 TB/s high-bandwidth memory (HBM4) across high-density 3Dx3D heterogeneous packaging (CoWoS / UCIe).

The **Parallel Unified Low-latency Streaming Engine (PULSE™)** is Fairview's CUDA/ROCm-equivalent software platform. PULSE delivers a high-performance, polyglot developer interface enabling deep-learning frameworks (PyTorch, Triton, JAX) to saturate physical hardware execution pipelines with **zero graph breaks, sub-8ns hardware synchronization, and deterministic 350W air-cooled TCO**.

```
+-----------------------------------------------------------------------------------+
|                        AI Applications & Framework Layer                          |
|       (PyTorch 2.x  |  Triton MLIR  |  HuggingFace  |  vLLM  |  Kubernetes)       |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                        PULSE™ Compiler & Lowering Layer                           |
|       • Triton MLIR Lowering Passes        • 2:4 Structured Sparsity Optimizer    |
|       • FreeToken Elastic MoE Scheduler   • Paged Attention DMA Dispatch          |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                     PULSE™ Unified Polyglot Client Bindings                       |
|   • Python (pulse-py)       • Rust (pulse-rs)       • Go (pulse-go)               |
|   • C++20 (pulse.hpp)       • Pure C ABI (pulse.h)                                |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                     PULSE™ Pre-Silicon Runtime Engine                             |
|   • Device Queue Dispatch   • 32-Channel Memory Pool Virtualizer (Gallium MMU)    |
|   • Local Emulation Layer (Apple Silicon Metal MPS / Linux x86_64 AVX-512)        |
+-----------------------------------------------------------------------------------+
```

---

## 🌟 Key Architecture & Capabilities

### 1. Zero-Friction PyTorch 2.x Integration (`torch.compile`)
PULSE integrates directly into PyTorch's `Inductor` backend. Existing models run with zero code refactoring:
```python
import torch
import pulse

# Seamless 1-line compilation targeting Fairview Stallion MPU
model = MyTransformerModel()
opt_model = torch.compile(model, backend="pulse")
```

### 2. Triton JIT & MLIR Lowering
Custom Triton kernels compile directly into Stallion MPU systolic instruction packets, bypassing host CPU overhead and intermediate CUDA translation layers.

### 3. UC Berkeley FreeToken Elastic MoE Engine
Implements bandwidth-adaptive token routing and non-blocking asynchronous memory offloading across the 16.0 TB/s Gallium interconnect, eliminating CPU synchronization stalls on large Mixture-of-Experts (MoE) workloads.

### 4. Cloud-Native Kubernetes Device Plugin (`fairview.com/mpu`)
Provides production-grade Kubernetes resource allocation, multi-tenant isolation, health telemetry, and Prometheus export metrics for enterprise on-premise clusters.

### 5. Local Pre-Silicon Hardware Emulation
Enables developers to develop, test, and benchmark PULSE applications today on developer workstations (Apple Silicon Metal Performance Shaders or Linux x86_64) prior to physical silicon deployment.

---

## 📁 Repository Structure

```
pulse-sdk/
├── SDK/                                    # PULSE™ Polyglot Driver & Pre-Silicon Emulation Engine
│   ├── compiler/                           # Compiler Infrastructure (Triton MLIR -> Stallion ISA)
│   │   ├── __init__.py
│   │   └── triton_lowering.py              # MLIR JIT Lowering Passes
│   ├── core/                               # Pre-Silicon Architecture Simulators
│   │   ├── stallion_mpu.py                 # 144-MEU FP8/FP4 Sparse Math Modeling Engine
│   │   └── gallium_mmu.py                  # 512 GB 32-Channel Memory Pool Virtualizer
│   ├── pulse/                              # 5-Language Polyglot Driver Ecosystem
│   │   ├── include/                        # C ABI (pulse.h) & C++20 RAII Wrappers (pulse.hpp)
│   │   ├── src/                            # Native Driver Implementations (pulse_c_api.c, pulse_cpp_api.cpp)
│   │   ├── python/                         # PyTorch 2.x Integration & MoE Schedulers (pulse-py)
│   │   ├── rust/                           # Memory-Safe Tokio Async Drivers (pulse-rs)
│   │   ├── go/                             # CGO Bindings & Kubernetes Device Plugin (pulse-go)
│   │   ├── tests/                          # Polyglot Multi-Language Validation Test Suite
│   │   └── run_all_tests.sh                # Turnkey Verification Script
│   └── tests/                              # End-to-End Compiler & Execution Pipeline Tests
├── CONTRIBUTING.md                         # Engineering Standards & Pull Request Guidelines
├── LICENSE                                 # FairView Evaluation License
├── RELEASE_NOTES_v0.8.4-alpha.md           # SDK Release Changelog & Feature Matrix
└── SECURITY.md                             # Vulnerability Disclosure & Bug Bounty Policy
```

---

## 🚀 Polyglot Quickstart Guides

### 1. Run Complete Test Suite (All 5 Languages)
```bash
cd SDK/pulse
./run_all_tests.sh
```

### 2. Python / PyTorch Integration
```python
import torch
import pulse

# Select Stallion MPU device
device = pulse.device(0)

# Allocate memory in Gallium 16.0 TB/s unified memory pool
x = torch.randn(4096, 4096, dtype=torch.float8_e4m3fn)
y = torch.randn(4096, 4096, dtype=torch.float8_e4m3fn)

# Deterministic systolic execution with 2:4 structured sparsity
z = pulse.matmul(x, y, sparsity="2:4")
```

### 3. C++20 RAII Stream Execution
```cpp
#include <pulse/pulse.hpp>

int main() {
    // RAII Initialization
    pulse::Device device(0);
    pulse::Stream stream = device.createStream();

    // Allocate 16 TB/s Gallium High-Bandwidth Memory
    pulse::Buffer<float> d_matrix = stream.allocate<float>(4096 * 4096);
    
    // Launch asynchronous systolic kernel
    stream.launchMEU(d_matrix, 4096, 4096);
    stream.synchronize(); // Sub-8ns hardware barrier
    return 0;
}
```

### 4. Rust (Memory-Safe Tokio Async Runtime)
```rust
use pulse::{Device, Stream};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let device = Device::new(0)?;
    let stream = device.create_stream()?;
    
    let buffer = stream.allocate::<f32>(1024).await?;
    stream.synchronize().await?;
    Ok(())
}
```

### 5. Go & Kubernetes Device Plugin
```go
package main

import (
    "fmt"
    "fairviewsemi.com/pulse"
)

func main() {
    dev, err := pulse.NewDevice(0)
    if err != nil {
        panic(err)
    }
    defer dev.Close()

    memSlice := dev.AllocateSlice(1024)
    fmt.Printf("Allocated CXL memory slice on %s\n", dev.Name())
}
```

---

## 🏢 Enterprise & Microvertical Solutions

Fairview's hardware and software stack is optimized for mission-critical enterprise microverticals:
* **BFSI & Algorithmic Trading**: Ultra-low deterministic latency, zero jitter, and air-gapped on-premise risk LLM inference.
* **Defense & Critical Infrastructure**: Turnkey sovereign data residency with hardware-root-of-trust security enclaves.
* **Telecommunications & Edge AI**: 350W air-cooled architecture dropping directly into standard 15kW enterprise racks with zero liquid plumbing retrofits.

---

## 🔒 Security & Proprietary IP Disclosure

This repository contains the **open developer runtime and compiler toolchains**. 

For foundry partners, commercial Tier-1 banking pilot access, or government evaluation panels requiring access to proprietary silicon design files (synthesizeable SystemVerilog RTL, OpenLane configurations, GDSII layout masks, and SDC timing sign-off collateral under NDA), please contact:

* **Executive Inquiries:** [srikanth@fairviewsemi.com](mailto:srikanth@fairviewsemi.com)
* **Security & Vulnerability Disclosure:** [security@fairviewsemi.com](mailto:security@fairviewsemi.com)

---

<div align="center">
  <sub>© 2026 FairView Semiconductor Inc. All rights reserved. PULSE™ is a trademark of FairView Semiconductor Inc.</sub>
</div>
