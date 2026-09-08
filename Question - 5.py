import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


# 1. LOAD IMAGE AND CONVERT TO GRAYSCALE

image = np.array(Image.open("oceanCapture.jpg"))

# Mean over RGB channels as specified in the assignment
gray = image.mean(axis=2)

print("Original image shape:", image.shape)
print("Grayscale image shape:", gray.shape)


# 2. FOURIER TRANSFORM

F = np.fft.fft2(gray)

# Magnitude of Fourier transform
magnitude = np.abs(F)

# Logarithmic magnitude
log_magnitude = 20 * np.log10(magnitude + 1e-12)


# 3. FIND THE 85001st LARGEST COMPONENT

# Sort all Fourier magnitudes in descending order
sorted_values = np.sort(log_magnitude.flatten())[::-1]

# 85001st largest component
threshold = sorted_values[85000]

print("\nThreshold =", threshold)


# 4. KEEP THE LARGEST 85000 COMPONENTS

# Assignment says to keep components within 10^-6
# of the threshold as well.
keep = log_magnitude >= (threshold - 1e-6)

F_compressed = np.where(keep, F, 0)

print("Number of Fourier components kept:", np.sum(keep))
print("Total Fourier components:", F.size)
print("Percentage kept:", 100 * np.sum(keep) / F.size)


# 5. RECONSTRUCT COMPRESSED IMAGE

compressed_image = np.real(np.fft.ifft2(F_compressed))

# Display compressed image
plt.figure(figsize=(8, 6))
plt.imshow(compressed_image, cmap="gray")
plt.title("Compressed Ocean Image")
plt.axis("off")
plt.show()


# 6. SECRET MESSAGE

message = "PNS Ghazi is sunk near Vishakhapatanam at 17°40'59''N 83°21'4''E"

print("\nSecret message:")
print(message)

print("\nASCII / Unicode values:")
print([ord(character) for character in message])


# 7. ENCODE MESSAGE IN 425th ROW

F_encoded = F_compressed.copy()

# Python uses 0-based indexing.
# Therefore 425th row = index 424.
row = 424

for i, character in enumerate(message):

    # Start from 2nd column
    column = i + 1

    # Convert character to numerical value
    value = ord(character)

    # Normalize by 200
    normalized_value = value / 200

    # Convert to logarithmic scale
    log_value = normalized_value * threshold

    # Convert back to normal Fourier magnitude
    encoded_magnitude = 10 ** (log_value / 20)

    # Keep the original phase
    phase = np.angle(F_compressed[row, column])

    # Store encoded value
    F_encoded[row, column] = (
        encoded_magnitude * np.exp(1j * phase)
    )


# 8. RECONSTRUCT IMAGE WITH HIDDEN MESSAGE

encoded_image = np.real(np.fft.ifft2(F_encoded))

plt.figure(figsize=(8, 6))
plt.imshow(encoded_image, cmap="gray")
plt.title("Image After Steganography")
plt.axis("off")
plt.show()


# 9. DECODE THE SECRET MESSAGE

decoded_message = ""

for i in range(len(message)):

    column = i + 1

    # Get Fourier coefficient
    coefficient = F_encoded[row, column]

    # Get magnitude
    encoded_magnitude = np.abs(coefficient)

    # Convert magnitude back to logarithmic scale
    log_value = 20 * np.log10(encoded_magnitude)

    # Reverse normalization
    value = round((log_value / threshold) * 200)

    # Convert number back to character
    decoded_message += chr(value)


# 10. DISPLAY DECODED MESSAGE

print("\nDecoded message:")
print(decoded_message)


# 11. VERIFY

if decoded_message == message:
    print("\nSUCCESS: Message decoded correctly!")
else:
    print("\nMessage decoding failed.")
