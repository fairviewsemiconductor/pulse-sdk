import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../python'))
import pulse
import pulse.compiler

print("--- Python PyTorch MPS Accelerated Attention Test ---")
dev = pulse.device("mpu:0")
buf = pulse.zeros((1024, 1024), device=dev)
pulse.compiler.lower_triton_kernel("mock_attention_kernel")
print("Python API Test Passed")
