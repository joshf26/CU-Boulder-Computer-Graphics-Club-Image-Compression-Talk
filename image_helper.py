import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

ARIAL_FONT_PATH = '/usr/share/gazebo-9/media/fonts/arial.ttf'


def convert_to_image(path):
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
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def as_tuple(self):
        return self.x, self.y


class Pixel:
    def __init__(self, r_or_iter, g=None, b=None):
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
    def __init__(self, path_or_size=(500, 500)):
        if isinstance(path_or_size, str):
            with open(path_or_size) as file:
                self.pixels = [[Pixel(list(map(int, pixel.split(',')))) for pixel in line.strip().split('|')] for line in file]
        elif isinstance(path_or_size, Size):
            self.pixels = [[Pixel(0, 0, 0) for _ in range(path_or_size.x)] for _ in range(path_or_size.y)]
        else:
            self.pixels = [[Pixel(0, 0, 0) for _ in range(path_or_size[0])] for _ in range(path_or_size[1])]

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
        image = PIL.Image.new('RGB', self.size.as_tuple)
        pixels = image.load()

        for x in range(self.size.x):
            for y in range(self.size.y):
                pixels[x, y] = self.pixels[x][y].as_tuple

        image = image.resize((self.size.x * scale, self.size.y * scale))
        draw = PIL.ImageDraw.Draw(image)
        font = PIL.ImageFont.truetype(ARIAL_FONT_PATH, 32)
        draw.text((15, 15), title, (255, 0, 0), font=font)
        image.show()

    def save(self, path):
        data = ''
        for x in range(self.size.x):
            for y in range(self.size.y):
                data += ','.join(map(str, self.pixels[x][y].as_tuple))
                if not y == self.size.y - 1:
                    data += '|'

            if not x == self.size.x - 1:
                data += '\n'

        with open(path, 'w') as file:
            file.write(data)
