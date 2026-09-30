#include "../include/pulse.hpp"
#include <iostream>

int main() {
    std::cout << "--- C++ Stream & Matrix Test ---\n";
    pulse::Device dev(0);
    pulse::Stream stream = dev.createStream();
    pulse::GalliumBuffer<float> buffer(1024);
    stream.synchronize();
    std::cout << "C++ API Test Passed\n";
    return 0;
}
