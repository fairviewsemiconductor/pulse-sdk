// ============================================================================
// Copyright (c) 2026 FairView Semiconductor Inc. All Rights Reserved.
// Licensed under the FairView Semiconductor Evaluation & Silicon IP License.
//
// Crate: pulse-rs
// Description: Safe Rust client bindings for FairView Stallion MPU & Gallium MMU
// ============================================================================

pub mod runtime;
pub mod flow;

pub use runtime::{Device, Stream};
pub use flow::GalliumMemoryVirtualizer;

pub fn init() {
    println!("[PULSE Rust] Safe Rust bindings initialized for FairView Stallion MPU.");
}
