from PIL import Image

# Function to encode the secret message into the image
def encode_image(image_path, message, output_path):
    # Open the image
    img = Image.open(image_path)
    pixels = img.load()
    
    # Convert the message to binary format
    binary_message = ''.join(format(ord(c), '08b') for c in message)  # Convert each char to binary
    message_len = len(binary_message)
    
    # Add a delimiter to the message to mark the end
    binary_message += '1111111111111110'  # Delimiter to mark the end of the message
    
    # Check if the image can hold the message
    width, height = img.size
    if message_len > width * height * 3:
        raise ValueError("Message is too large to hide in this image.")
    
    # Encode the binary message into the image pixels
    idx = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # Modify the least significant bit of each channel
            if idx < message_len:
                r = (r & 0xFE) | int(binary_message[idx])  # Set the LSB of red
                idx += 1
            if idx < message_len:
                g = (g & 0xFE) | int(binary_message[idx])  # Set the LSB of green
                idx += 1
            if idx < message_len:
                b = (b & 0xFE) | int(binary_message[idx])  # Set the LSB of blue
                idx += 1
                
            pixels[x, y] = (r, g, b)

    # Save the image with hidden message
    img.save(output_path)
    print(f"Message encoded in {output_path}.")

# Function to decode the hidden message from the image
def decode_image(image_path):
    # Open the image
    img = Image.open(image_path)
    pixels = img.load()

    binary_message = ""
    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            # Extract the LSB from each channel
            binary_message += str(r & 1)  # Get the LSB of red
            binary_message += str(g & 1)  # Get the LSB of green
            binary_message += str(b & 1)  # Get the LSB of blue

    # Split the binary message into 8-bit chunks and convert to characters
    byte_size = 8
    binary_message = binary_message[:binary_message.find('1111111111111110')]  # Remove the delimiter
    decoded_message = ''.join(chr(int(binary_message[i:i+byte_size], 2)) for i in range(0, len(binary_message), byte_size))
    return decoded_message

# Usage example
encode_image('input_image.png', 'Hello, this is a secret message!', 'output_image.png')
hidden_message = decode_image('output_image.png')
print("Hidden message:", hidden_message)
