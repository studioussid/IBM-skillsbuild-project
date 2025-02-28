from PIL import Image

def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

def encode_image(image_path, secret_message, output_path):
    image = Image.open(image_path)
    encoded_image = image.copy()
    pixels = encoded_image.load()

    binary_message = text_to_bin(secret_message)
    message_index = 0
    message_length = len(binary_message)

    for i in range(image.height):
        for j in range(image.width):
            pixel = list(pixels[j, i])
            for k in range(3):
                if message_index < message_length:
                    pixel[k] = pixel[k] & 0xFE | int(binary_message[message_index])
                    message_index += 1
            pixels[j, i] = tuple(pixel)

    encoded_image.save(output_path)
    print(f"Message encoded and saved in {output_path}")
