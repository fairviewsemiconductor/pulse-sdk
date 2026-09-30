# FairView Semiconductor — Security & Vulnerability Disclosure Policy

Do not describe this repo as production silicon drivers.

FairView Semiconductor takes the security and integrity of its silicon architectures, RTL engines, memory controllers, and software drivers seriously.

## Reporting a Vulnerability

If you discover a security vulnerability, side-channel attack vector, or hardware flaw within FairView's hardware RTL or software SDK:

1. **Do not disclose publicly.** Please report the issue directly to our Security & Product Engineering team at:  
   📧 **security@fairviewsemi.com** or **engineering@fairviewsemi.com**
2. Include in your report:
   - A detailed description of the vulnerability.
   - Affected hardware RTL modules (e.g. `fv_matrix_execution_unit.sv`, `fv_hbm4_controller_16384.sv`) or SDK drivers.
   - Steps to reproduce or proof-of-concept testbench (`.sv` or `.py`).
   - Impact assessment (e.g. memory leak across CXL boundary, ECC bypass, or DMA corruption).

## Scope & Coverage

- **Silicon RTL**: Memory arbiter starvation, DMA boundary overflows, and SECDED ECC error handling vulnerabilities.
- **PULSE Driver Suite**: Memory safety in C/C++/Rust runtimes, CGO pointer violations in Go, and buffer overruns in tensor lowerings.
- **Cluster Orchestration**: Kubernetes Device Plugin security and isolation guarantees for multi-tenant MPU scheduling.

## Response Timelines

- **Initial Response**: Within 24 hours.
- **Triage & Status Assessment**: Within 72 hours.
- **Remediation & Patch Release**: Coordinated disclosure within 30 days.

---
© 2026 FairView Semiconductor Inc. All Rights Reserved.
