# PULSE SDK — Pre-silicon host runtime

PULSE is Fairview's host-side programming interface for Stallion / Gallium
pre-silicon bring-up: ISA word packing, language bindings, and numeric goldens
on CPU or Apple MPS.

This repository is the software tree. RTL, PDK layouts, and the nine-TB
simulation gate live in a separate private engineering tree.

## Scope of this release

Supported in-tree:
- Host ISA packers for opcodes A1 (DMA) and B1 (MMA)
- PyTorch / C / C++ / Rust / Go bindings and wrapper tests
- GRID=4 host golden (16 PEs); optional wider host sim is a parameter only

Not in this tree (product roadmap, not this release):
- Device driver for production silicon
- Foundry GDS or a JEDEC HBM PHY
- torch.compile / Triton / MLIR production compiler
- Kubernetes device plugin as a supported deploy artifact

Current hardware instance used for bring-up: 1 engine, GRID=4, PHY=none,
on-chip SRAM stand-in. Larger published scale figures are roadmap sizing,
not capabilities of this SDK drop.

## Layout

pulse-sdk/
  SDK/compiler/     host packers and drafts (not a production MLIR JIT)
  SDK/core/         host golden / memory model (default GRID=4)
  SDK/pulse/        C, C++, Python, Rust, Go bindings and wrapper tests

## Tests

SDK/pulse/run_all_tests.sh runs host wrapper smoke tests.
It does not run RTL or OpenLane.

## License

See LICENSE.
