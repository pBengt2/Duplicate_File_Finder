# Import the tkinter and PIL modules
import tkinter as tk
from tkinter import filedialog
from PIL import Image

# Create the tkinter window
root = tk.Tk()


# Create a function to open the file dialog
def open_file_dialog():
    # Create a function to map pixel values to characters
    def map_pixel_to_character(pixel):
        # Create a lookup table of characters
        characters = [
            " ", " ", ".", "^", ",",
            ":", ";", "I", "l", "!",
            "i", "~", "+", "-", "?",
            "[", "]", "{", "}", "1",
            "(", ")", "|", "\\", "/",
            "t", "f", "j", "r", "x",
            "n", "u", "v", "c", "z",
            "X", "Y", "U", "J", "C",
            "L", "Q", "0", "O", "Z",
            "m", "w", "q", "p", "d",
            "b", "k", "h", "a", "o",
            "*", "#", "M", "W", "&",
            "8", "%", "B", "@", "$"
        ]

        # Get the length of the lookup table
        num_characters = len(characters)

        # Calculate the index of the character to use
        index = 0
        min_distance = float("inf")
        for i in range(num_characters):
            character = characters[i]
            character_pixel = get_character_pixel_value(character)
            distance = get_pixel_distance(pixel, character_pixel)
            if distance < min_distance:
                index = i
                min_distance = distance

        # Return the character at the calculated index
        return characters[index]

    # Create a function to get the pixel value for a character
    def get_character_pixel_value(character):
        # Create a lookup table of character pixel values
        character_pixels = {
            " ": (0, 0, 0),
            ".": (255, 255, 255),
            "^": (128, 128, 128),
            ",": (0, 0, 128),
            ":": (0, 128, 0),
            ";": (0, 128, 128),
            "I": (128, 0, 0),
            "l": (128, 0, 128),
            "!": (128, 128, 0),
            "i": (192, 192, 192),
            "~": (128, 128, 192),
            "+": (0, 0, 192),
            "-": (0, 192, 0),
            "?": (0, 192, 192),
            "[": (192, 0, 0),
            "]": (192, 0, 192),
            "{": (192, 192, 0),
            "}": (192, 192, 128),
            "1": (0, 0, 64),
            "(": (0, 128, 64),
            ")": (128, 0, 64),
            "|": (128, 128, 64),
            "\\": (192, 0, 64),
            "/": (192, 128, 64),
            "t": (0, 64, 0),
            "f": (0, 64, 128),
            "j": (128, 64, 0),
            "r": (128, 64, 128),
            "x": (64, 0, 0),
            "n": (64, 0, 128),
            "u": (64, 128, 0),
            "v": (64, 128, 128),
            "c": (0, 64, 64),
            "z": (128, 64, 64),
            "X": (64, 0, 64),
            "Y": (64, 64, 0),
            "U": (64, 64, 128),
            "J": (0, 64, 192),
            "C": (128, 64, 192),
            "L": (64, 64, 64),
            "Q": (64, 192, 0),
            "0": (64, 192, 128),
            "O": (0, 192, 64),
            "Z": (128, 192, 64),
            "m": (192, 0, 64),
            "w": (192, 128, 64),
            "q": (64, 64, 192),
            "p": (0, 128, 192),
            "d": (128, 128, 192),
            "b": (192, 64, 0),
            "k": (192, 64, 128),
            "h": (192, 192, 64),
            "a": (64, 192, 192), #,
            "o": (-1, -1, -1),
            "*": (-1, -1, -1),
            "#": (-1, -1, -1),
            "M": (-1, -1, -1),
            "W": (-1, -1, -1),
            "&": (-1, -1, -1),
            "8": (-1, -1, -1),
            "%": (-1, -1, -1),
            "B": (-1, -1, -1),
            "@": (-1, -1, -1),
            "$": (-1, -1, -1)
        }

        return character_pixels[character]

    # Create a function to get the pixel distance between two pixels
    def get_pixel_distance(pixel1, pixel2):
        # Calculate the difference between the pixel values
        red_diff = pixel1[0] - pixel2[0]
        green_diff = pixel1[1] - pixel2[1]
        blue_diff = pixel1[2] - pixel2[2]

        # Calculate the distance between the two pixels
        distance = (red_diff ** 2 + green_diff ** 2 + blue_diff ** 2) ** 0.5

        # Return the distance
        return distance

    # Create a function to convert the image to ASCII art
    def convert_image_to_ascii(image, width, height, pixels):
        # Initialize the output string
        output_string = ""

        # Loop over the pixels in the image
        for y in range(0, height, 15):
            for x in range(0, width, 5):
                # Get the pixel at the current position
                pixel = image.getpixel((x, y))

                # Map the pixel to a character
                character = map_pixel_to_character(pixel)

                # Append the character to the output string
                output_string += character

            # Append a newline character to the output string
            output_string += "\n"

        # Return the output string
        return output_string

    # Open the file dialog
    file_path = filedialog.askopenfilename()

    # Open the selected image file
    image = Image.open(file_path)

    # Get the image width and height
    width, height = image.size

    # Get the pixel data for the image
    pixels = image.getdata()

    # Convert the image to ASCII art
    ascii_art = convert_image_to_ascii(image, width, height, pixels)

    # Print the ASCII art to the console
    print(ascii_art)

    exit(0)

# Create the file dialog button
button = tk.Button(root, text="Select Image File", command=open_file_dialog)
button.pack()

# Run the tkinter event loop
root.mainloop()