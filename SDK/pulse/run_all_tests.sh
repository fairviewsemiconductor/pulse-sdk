#!/bin/bash
set -e
echo "======================================================================="
echo "PULSE DRIVER SUITE - MULTI-LANGUAGE VERIFICATION (C, C++, Python, Rust, Go)"
echo "======================================================================="

# Compile and run C
clang -o tests/test_c_api tests/test_c_api.c src/pulse_c_api.c
./tests/test_c_api
echo ""

# Compile and run C++
clang++ -std=c++20 -o tests/test_cpp_api tests/test_cpp_api.cpp src/pulse_c_api.c
./tests/test_cpp_api
echo ""

# Run Python
python3 tests/test_python_api.py
echo ""

# Compile and run Rust
rustc -o tests/test_rust_api tests/test_rust_api.rs
./tests/test_rust_api
echo ""

# Compile and run Go
cd tests
go build -o test_go_api test_go_api.go
./test_go_api
cd ..

echo ""
echo "======================================================================="
echo "✅ ALL 5 LANGUAGE INTERFACES COMPILED AND EXECUTED WITH 0 ERRORS."
echo "======================================================================="
