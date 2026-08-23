#ifndef PULSE_HPP
#define PULSE_HPP

#include "pulse.h"
#include <memory>
#include <stdexcept>
#include <iostream>

namespace pulse {

class Stream {
public:
    Stream() {}
    ~Stream() {}
    void synchronize() {
        pulseStreamSynchronize(nullptr);
    }
};

class Device {
public:
    Device(int id) {
        pulseInit();
    }
    Stream createStream() {
        return Stream();
    }
};

template <typename T>
class GalliumBuffer {
    T* ptr;
    size_t sz;
public:
    GalliumBuffer(size_t elements) : sz(elements) {
        pulseMallocGallium((void**)&ptr, elements * sizeof(T));
    }
    ~GalliumBuffer() {
        free(ptr);
    }
    
    GalliumBuffer(GalliumBuffer&& other) noexcept : ptr(other.ptr), sz(other.sz) {
        other.ptr = nullptr;
        other.sz = 0;
    }
    GalliumBuffer& operator=(GalliumBuffer&& other) noexcept {
        if (this != &other) {
            free(ptr);
            ptr = other.ptr;
            sz = other.sz;
            other.ptr = nullptr;
            other.sz = 0;
        }
        return *this;
    }
};

}

#endif // PULSE_HPP
