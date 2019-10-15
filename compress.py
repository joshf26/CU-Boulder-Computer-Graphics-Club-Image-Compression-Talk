from image_helper import Image, Pixel


def average_pixels(pixels):
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
    new_image = Image((image.size.x // factor, image.size.y // factor))

    for x in range(new_image.size.x):
        for y in range(new_image.size.y):
            pixels_to_average = []
            for extend_x in range(factor):
                for extend_y in range(factor):
                    pixels_to_average.append(image[x * factor + extend_x][y * factor + extend_y])

            new_image[x][y] = average_pixels(pixels_to_average)

    return new_image


def compress_colors(image, factor):
    new_image = Image(image.size)

    for x in range(new_image.size.x):
        for y in range(new_image.size.y):
            new_image[x][y].r = int(image[x][y].r * factor)
            new_image[x][y].g = int(image[x][y].g * factor)
            new_image[x][y].b = int(image[x][y].b * factor)

    return new_image


DOWNSCALE_FACTOR = 6
COMPRESS_COLORS_FACTOR = 16

lesley = Image('lesley.image')
lesley.show('Uncompressed')

downscaled_lesley = downscale(lesley, DOWNSCALE_FACTOR)
downscaled_lesley.show('Downscaled', scale=DOWNSCALE_FACTOR)
downscaled_lesley.save('lesley-downscaled.image')

compressed_colors_lesley = compress_colors(lesley, 1 / COMPRESS_COLORS_FACTOR)
compressed_colors_lesley.save('lesley-compressed-colors.image')
uncompressed_colors_lesley = compress_colors(compressed_colors_lesley, COMPRESS_COLORS_FACTOR)
uncompressed_colors_lesley.show('Compressed Colors')

downscaled_and_compressed_lesley = compress_colors(downscale(lesley, DOWNSCALE_FACTOR), 1 / COMPRESS_COLORS_FACTOR)
downscaled_and_compressed_lesley.save('lesley-downscaled-compressed-colors.image')
downscaled_and_uncompressed_lesley = compress_colors(downscaled_and_compressed_lesley, COMPRESS_COLORS_FACTOR)
downscaled_and_uncompressed_lesley.show('Downscaled and Compressed', scale=DOWNSCALE_FACTOR)
