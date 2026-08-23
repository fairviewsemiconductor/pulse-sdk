def device(name):
    print(f"[PULSE Python] Device {name} selected (Stallion MPU).")
    return name

def zeros(shape, dtype="float32", device="mpu:0"):
    print(f"[PULSE Python] Gallium MMU allocated zeros of shape {shape} on {device}")
    return "GalliumBuffer"
