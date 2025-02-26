from PIL import Image

# Step 1: Convert the secret message to binary
def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

# Step 2: Hide the message in the image
def encode_image(image_path, secret_data, output_path):
    # Open the image
    image = Image.open(image_path)
    encoded_image = image.copy()
    pixels = encoded_image.load()  # Get the pixel data

    # Convert the secret message to binary
    binary_data = text_to_bin(secret_data)
    data_len = len(binary_data)
    data_index = 0
    
    # Loop through each pixel and replace LSB with binary data
    for i in range(image.height):
        for j in range(image.width):
            pixel = list(pixels[j, i])  # Get RGB value of pixel
            
            for n in range(3):  # Iterate through R, G, B channels
                if data_index < data_len:
                    pixel[n] = pixel[n] & 0xFE | int(binary_data[data_index])  # Replace LSB
                    data_index += 1
            
            pixels[j, i] = tuple(pixel)  # Update pixel with new value

    # Save the image with the hidden message
    encoded_image.save(output_path)

# Step 3: Extract the hidden message from the image
def decode_image(image_path):
    image = Image.open(image_path)
    pixels = image.load()

    binary_data = ""
    
    # Loop through each pixel and extract LSB
    for i in range(image.height):
        for j in range(image.width):
            pixel = pixels[j, i]
            for n in range(3):  # RGB channels
                binary_data += str(pixel[n] & 1)  # Extract LSB

    # Convert binary data back to text
    secret_message = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        secret_message += chr(int(byte, 2))  # Convert binary to ASCII character
    
    return secret_message

# Example usage
secret_message = "Hello, this is a secret!"
image_path = 'input_image.png'  # Your image file
encoded_image_path = 'encoded_image.png'  # Path to save the image with hidden data

# Step 4: Encode the message into the image
encode_image(image_path, secret_message, encoded_image_path)

# Step 5: Decode the message from the image
retrieved_message = decode_image(encoded_image_path)
print("Decoded message:", retrieved_message)
