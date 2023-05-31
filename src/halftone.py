from PIL import Image, ImageDraw, ImageStat
import io


def transform_image(image):
    # Open the image
    im = Image.open(image)

    # Convert the image to CMYK
    cmyk = im.convert('CMYK')

    # Apply Gray Component Replacement (GCR)
    cmyk = gcr(cmyk, 0)

    # Generate halftone images
    dots = halftone(cmyk, 10, 1)

    # Merge halftone images into a single CMYK image
    merged_image = Image.merge('CMYK', dots)

    # Convert the transformed image to bytes
    image_bytes = io.BytesIO()
    merged_image.convert('RGB').save(image_bytes, format='JPEG')
    image_bytes.seek(0)

    return image_bytes


def transform(input_image_path, output_image_path, gcr_percentage=0, sample_size=10, scale_factor=1, show=False):
    # Open the input image
    im = Image.open(input_image_path).convert('CMYK')

    # Apply Gray Component Replacement (GCR)
    cmyk = gcr(im, gcr_percentage)

    # Generate halftone images
    dots = halftone(cmyk, sample_size, scale_factor)

    # Merge halftone images into a single CMYK image
    merged_image = Image.merge('CMYK', dots)

    # Save the output image
    merged_image.save(output_image_path)

    # Display the original and transformed images
    if show:
        im.show(title="Original Image")
        merged_image.show(title="Halftone CMYK Image")


def gcr(im, percentage):
    """Apply Gray Component Replacement (GCR) to the input CMYK image.
       Removes the specified percentage of gray component from CMY channels and puts it in the K channel.
    """
    cmyk_im = im.split()
    if not percentage:
        return Image.merge('CMYK', cmyk_im)
    cmyk = []
    for channel in cmyk_im:
        cmyk.append(channel.load())
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            gray = min(cmyk[0][x, y], cmyk[1][x, y], cmyk[2][x, y]) * percentage / 100
            for i in range(3):
                cmyk[i][x, y] -= gray
            cmyk[3][x, y] = gray
    return Image.merge('CMYK', cmyk_im)


def halftone(im, sample, scale):
    """Generate a list of half-tone images for the input CMYK image.
       The sample determines the sample box size, and the scale determines the dot size.
    """
    cmyk = im.split()
    dots = []
    angle = 0
    for channel in cmyk:
        channel = channel.rotate(angle, expand=1)
        size = channel.size[0] * scale, channel.size[1] * scale
        half_tone = Image.new('L', size)
        draw = ImageDraw.Draw(half_tone)
        for x in range(0, channel.size[0], sample):
            for y in range(0, channel.size[1], sample):
                box = channel.crop((x, y, x + sample, y + sample))
                diameter = (ImageStat.Stat(box).mean[0] / 255) ** 0.5
                edge = 0.5 * (1 - diameter)
                x_pos, y_pos = (x + edge) * scale, (y + edge) * scale
                box_edge = sample * diameter * scale
                draw.ellipse((x_pos, y_pos, x_pos + box_edge, y_pos + box_edge), fill=255)
        half_tone = half_tone.rotate(-angle, expand=1)
        width_half, height_half = half_tone.size
        xx = (width_half - im.size[0] * scale) // 2
        yy = (height_half - im.size[1] * scale) // 2
        half_tone = half_tone.crop((xx, yy, xx + im.size[0] * scale, yy + im.size[1] * scale))
        dots.append(half_tone)
        angle += 15
    return dots


if __name__ == '__main__':
    input_image_path = "../images/tree.jpg"
    output_image_path = "../images/halftone_tree.jpg"
    gcr_percentage = 0
    sample_size = 10
    scale_factor = 1

    transform(input_image_path, output_image_path, gcr_percentage, sample_size, scale_factor)

