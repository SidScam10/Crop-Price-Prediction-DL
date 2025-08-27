import torch

# Check if a CUDA-enabled GPU is available.
if torch.cuda.is_available():
    # Get the number of available GPUs.
    gpu_count = torch.cuda.device_count()
    print(f"GPU(s) found and configured: {gpu_count}")

    # Iterate through each GPU and print its name.
    for i in range(gpu_count):
        print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")

    # Set the 'device' object to be used for moving tensors and models to the GPU.
    device = torch.device("cuda")

else:
    print("No GPU found. The model will run on the CPU.")
    # Set the 'device' object to CPU.
    device = torch.device("cpu")


# You can then use this 'device' object throughout your script
# to ensure your tensors and models are on the correct hardware.
print(f"\nModel and tensors will be moved to: '{device}'")

# Example of moving a tensor to the selected device:
# my_tensor = torch.randn(2, 2)
# my_tensor = my_tensor.to(device)
# print(f"\nExample tensor is on device: {my_tensor.device}")