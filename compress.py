from image_helper import Image, Pixel


def average_pixels(pixels):
    """ Returns a pixel representing the average color of the given pixels. """

    reds, greens, blues = [], [], []

    for pixel in pixels:
        reds.append(pixel.r)
        greens.append(pixel.g)
        blues.append(pixel.b)

    return Pixel(
        sum(reds) // len(reds),
        sum(greens) // len(greens),
        sum(blues) // len(blues),
    )


def downscale(image, factor):
    """ Downscales an image by a given factor. """

    if factor <= 0:
        raise ValueError('Downscale factor must be a positive integer.')

    new_image = Image((image.size.width // factor, image.size.height // factor))

    for x in range(new_image.size.width):
        for y in range(new_image.size.height):
            pixels_to_average = []
            for extend_x in range(factor):
                for extend_y in range(factor):
                    pixels_to_average.append(image[x * factor + extend_x][y * factor + extend_y])

            new_image[x][y] = average_pixels(pixels_to_average)

    return new_image


def compress_colors(image, factor):
    """ Compresses colors in an image by a given factor. If factor > 1, the
        function will "uncompress" the image.
    """

    new_image = Image(image.size)

    for x in range(new_image.size.width):
        for y in range(new_image.size.height):
            new_image[x][y].r = int(image[x][y].r * factor)
            new_image[x][y].g = int(image[x][y].g * factor)
            new_image[x][y].b = int(image[x][y].b * factor)

    return new_image


# Example code for testing.
# Assume DS = Downscaled
#        CC = Compressed Colors

DS_FACTOR = 6
CC_FACTOR = 32

lesley = Image('lesley.image')
lesley.show('Uncompressed')

ds_lesley = downscale(lesley, DS_FACTOR)
ds_lesley.show('Downscaled', scale=DS_FACTOR)
ds_lesley.save('lesley-ds.image')

cc_lesley = compress_colors(lesley, 1 / CC_FACTOR)
cc_lesley.save('lesley-cc.image')
uncc_lesley = compress_colors(cc_lesley, CC_FACTOR)
uncc_lesley.show('Compressed Colors')

ds_and_compressed_lesley = compress_colors(
    downscale(lesley, DS_FACTOR),
    1 / CC_FACTOR
)
ds_and_compressed_lesley.save('lesley-ds-cc.image')
ds_and_uncompressed_lesley = compress_colors(
    ds_and_compressed_lesley,
    CC_FACTOR
)
ds_and_uncompressed_lesley.show(
    'Downscaled and Compressed Colors',
    scale=DS_FACTOR
)
