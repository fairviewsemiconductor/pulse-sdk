// ============================================================================
// Copyright (c) 2026 FairView Semiconductor Inc. All Rights Reserved.
// Licensed under the FairView Semiconductor Evaluation & Silicon IP License.
//
// File: pulse.h
// Component: PULSE™ (Parallel Unified Low-latency Streaming Engine) Pure C ABI
// Architecture: Stallion MPU & Gallium 16.0 TB/s MMU Unified Driver Interface
// ============================================================================

#ifndef PULSE_H
#define PULSE_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct pulseDevice_t pulseDevice_t;
typedef struct pulseStream_t pulseStream_t;
typedef struct pulseMemoryPool_t pulseMemoryPool_t;

// Device & Memory Management
int pulseInit(void);
int pulseMallocGallium(void** devPtr, size_t size);
int pulseFreeGallium(void* devPtr);
int pulseMemcpyHtoD(void* dst, const void* src, size_t size, pulseStream_t* stream);
int pulseMemcpyDtoH(void* dst, const void* src, size_t size, pulseStream_t* stream);

// Matrix Execution Unit (MEU) Kernel Dispatch
int pulseLaunchMEU(pulseStream_t* stream, void* func, void** args);
int pulseStreamSynchronize(pulseStream_t* stream);

#ifdef __cplusplus
}
#endif

#endif // PULSE_H
