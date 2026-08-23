# Contributing to FairView Semiconductor

Thank you for your interest in contributing to the **FairView Semiconductor Master Hardware & PULSE SDK Repository**.

## Hardware & RTL Engineering Guidelines

When contributing SystemVerilog RTL modules to the Stallion MPU or Gallium MMU subsystems:

1. **IEEE 1800-2017 SystemVerilog Compliance**: All RTL must be synthesizable using standard open-source tools (Yosys) as well as commercial EDA suites (Synopsys Design Compiler, Cadence Genus).
2. **Clock & Reset Standards**: Use active-low asynchronous reset (`rst_n`) and explicit clock domain crossings (CDC) between the 2.4 GHz MPU core clock and the 4.0 GHz HBM4 PHY clock.
3. **Naming Conventions**:
   - Module names must follow `fv_<subsystem>_<description>.sv`.
   - Testbench files must follow `tb_<subsystem>_<description>.sv`.
4. **Zero-Error Verification Gate**:
   - All contributions must pass `./run_verification_suite.sh` with 0 timing, linting, or assertion errors.

## PULSE SDK Development Guidelines

When contributing to the 5-language PULSE driver suite (`SDK/pulse/`):

1. **Pure C ABI (`pulse.h`)**: The C header is the foundational ABI. No breaking changes without backward compatibility shims.
2. **RAII & Safety**:
   - C++ wrappers (`pulse.hpp`) must employ strict RAII and move semantics.
   - Rust crates (`pulse-rs`) must remain strictly memory safe without unmanaged unsafe pointers.
   - Go packages (`pulse-go`) must pass all race condition checks (`go test -race`).
   - Python packages must maintain compatibility with PyTorch 2.x and Triton MLIR lowering passes.

## Pull Request Checklist

Before submitting a Pull Request:
- [ ] `./run_verification_suite.sh` passes 100% of Icarus Verilog tests and Yosys synthesis.
- [ ] `cd SDK/pulse && ./run_all_tests.sh` executes with 0 errors across C, C++, Python, Rust, and Go.
- [ ] All source files include standard FairView Semiconductor copyright headers.

---
© 2026 FairView Semiconductor Inc. All Rights Reserved.
