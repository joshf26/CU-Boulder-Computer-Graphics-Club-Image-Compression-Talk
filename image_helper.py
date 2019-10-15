import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

# Note: This was only tested on Ubuntu 18.04. You may have to modify this to
#       point to an existing font file.
FONT_PATH = '/usr/share/gazebo-9/media/fonts/arial.ttf'
FONT = PIL.ImageFont.truetype(FONT_PATH, 32)


def convert_to_image(path):
    """ Given a path to an jpeg, png, or any other format that PIL supports,
        return an instance of the Image class defined below that stores that
        image.
    """

    image = PIL.Image.open(path)
    pixels = image.load()
    result = Image(image.size)

    for x in range(image.size[0]):
        for y in range(image.size[1]):
            result[x][y].r = pixels[x, y][0]
            result[x][y].g = pixels[x, y][1]
            result[x][y].b = pixels[x, y][2]

    return result


class Size:
    """ Stores an width and height, which is easier than having to access
        indexes of a tuple.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def as_tuple(self):
        return self.width, self.height


class Pixel:
    """ Stores RGB values representing a pixel, which is easier than having to
        access indexes of a tuple.
    """

    def __init__(self, r_or_iter, g=None, b=None):
        # The first parameter can optionally be an iterable holding all three
        # values.
        if isinstance(r_or_iter, int):
            self.r = r_or_iter
            self.g = g
            self.b = b
        else:
            self.r = r_or_iter[0]
            self.g = r_or_iter[1]
            self.b = r_or_iter[2]

    @property
    def as_tuple(self):
        return self.r, self.g, self.b


class Image:
    """ The main wrapper class around PIL's Image class. Accessing pixels is
        much easier since you can subscript an instance.
    """

    def __init__(self, path_or_size=(500, 500)):
        # If the parameter is a path, open the file and read in the pixels.
        if isinstance(path_or_size, str):
            with open(path_or_size) as file:
                self.pixels = [[Pixel(list(map(int, pixel.split(','))))
                                for pixel in line.strip().split('|')]
                               for line in file]

        # If the parameter is a `Size`, create a black image of that size.
        elif isinstance(path_or_size, Size):
            self.pixels = [[Pixel(0, 0, 0) for _ in range(path_or_size.width)]
                           for _ in range(path_or_size.height)]

        # Else, assume it is an iterable containing size information, and create
        # a black image of that size.
        else:
            self.pixels = [[Pixel(0, 0, 0) for _ in range(path_or_size[0])]
                           for _ in range(path_or_size[1])]

        if len(self.pixels) == 0 or len(self.pixels[0]) == 0:
            raise Exception('Cannot create an image with width or height 0.')

    def __getitem__(self, index):
        return self.pixels[index]

    def __str__(self):
        return str(self.pixels)

    @property
    def size(self):
        return Size(len(self.pixels), len(self.pixels[0]))

    def show(self, title, scale=1):
        """ Displays the image in a popup window. """

        # Convert the image to a PIL Image.
        image = PIL.Image.new('RGB', self.size.as_tuple)
        pixels = image.load()

        for x in range(self.size.width):
            for y in range(self.size.height):
                pixels[x, y] = self.pixels[x][y].as_tuple

        # Scale the image.
        image = image.resize((
            self.size.width * scale,
            self.size.height * scale,
        ))

        # Add the title text.
        draw = PIL.ImageDraw.Draw(image)
        draw.text((15, 15), title, (255, 0, 0), font=FONT)

        # Call PIL to display the image.
        image.show()

    def save(self, path):
        """ Save the image as a `.image` file (plaintext). """

        # Convert the data to a string.
        data = ''
        for x in range(self.size.width):
            for y in range(self.size.height):
                data += ','.join(map(str, self.pixels[x][y].as_tuple))
                if not y == self.size.height - 1:
                    data += '|'

            if not x == self.size.width - 1:
                data += '\n'

        # Write the string to the file.
        with open(path, 'w') as file:
            file.write(data)
