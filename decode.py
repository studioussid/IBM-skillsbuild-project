def decode_image(image_path):
    image = Image.open(image_path)
    pixels = image.load()

    binary_message = ""
    for i in range(image.height):
        for j in range(image.width):
            pixel = pixels[j, i]
            for k in range(3):
                binary_message += str(pixel[k] & 1)

    secret_message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        secret_message += chr(int(byte, 2))

    return secret_message
