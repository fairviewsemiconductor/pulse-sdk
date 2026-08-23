// ============================================================================
// Copyright (c) 2026 FairView Semiconductor Inc. All Rights Reserved.
// Licensed under the FairView Semiconductor Evaluation & Silicon IP License.
//
// File: pulse.hpp
// Component: Modern C++20 RAII Wrappers & Stream Pipelines for PULSE™
// Architecture: Stallion MPU & Gallium 16.0 TB/s MMU Unified Driver Interface
// ============================================================================

#ifndef PULSE_HPP
#define PULSE_HPP

#include "pulse.h"
#include <memory>
#include <stdexcept>
#include <iostream>

namespace pulse {

class Stream {
public:
    Stream() = default;
    ~Stream() = default;
    
    void synchronize() {
        pulseStreamSynchronize(nullptr);
    }

    void launchMEU(void* q_matrix, void* k_matrix) {
        pulseLaunchMEU(nullptr, q_matrix, &k_matrix);
    }
};

class Device {
private:
    int device_id;
public:
    explicit Device(int id = 0) : device_id(id) {
        if (pulseInit() != 0) {
            throw std::runtime_error("Failed to initialize FairView Stallion MPU device.");
        }
    }

    Stream createStream() {
        return Stream();
    }
};

template <typename T>
class GalliumBuffer {
private:
    T* ptr = nullptr;
    size_t element_count = 0;

public:
    explicit GalliumBuffer(size_t elements) : element_count(elements) {
        if (pulseMallocGallium(reinterpret_cast<void**>(&ptr), elements * sizeof(T)) != 0) {
            throw std::bad_alloc();
        }
    }

    ~GalliumBuffer() {
        if (ptr) {
            pulseFreeGallium(ptr);
            ptr = nullptr;
        }
    }

    // Move semantics
    GalliumBuffer(GalliumBuffer&& other) noexcept : ptr(other.ptr), element_count(other.element_count) {
        other.ptr = nullptr;
        other.element_count = 0;
    }

    GalliumBuffer& operator=(GalliumBuffer&& other) noexcept {
        if (this != &other) {
            if (ptr) pulseFreeGallium(ptr);
            ptr = other.ptr;
            element_count = other.element_count;
            other.ptr = nullptr;
            other.element_count = 0;
        }
        return *this;
    }

    // Disable copy
    GalliumBuffer(const GalliumBuffer&) = delete;
    GalliumBuffer& operator=(const GalliumBuffer&) = delete;

    T* data() noexcept { return ptr; }
    const T* data() const noexcept { return ptr; }
    size_t size() const noexcept { return element_count; }
};

} // namespace pulse

#endif // PULSE_HPP
