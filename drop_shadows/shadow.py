
from PIL import Image, ImageFilter

def dropShadow(redraw_image, original_image): # background, original_image

  offset = (0, 10)
  redraw_xy = (60, 60)
  original_xy = (360, 92)
  width = 540
  height = 360

  background = (0x3a, 0x3d, 0x3f)
  shadow = (0x00, 0x00, 0x00)
  iterations = 10

  canvas = Image.new('RGBA', (width, height), background)

  canvas.paste(shadow, (redraw_xy[0] + offset[0], redraw_xy[1] + offset[1]), redraw_image)
  canvas.paste(shadow, (original_xy[0] + offset[0], original_xy[1] + offset[1]), original_image)

  for i in range(iterations):
      canvas = canvas.filter(ImageFilter.BLUR)

  canvas.paste(redraw_image, (redraw_xy[0], redraw_xy[1]), redraw_image)
  canvas.paste(original_image, (original_xy[0], original_xy[1]), original_image)

  return canvas

if __name__ == "__main__":
  import sys

  redraw_image = Image.open(sys.argv[1])
  original_image = Image.open(sys.argv[2])
  original_image.thumbnail((128, 128), Image.ANTIALIAS)
  dropShadow(redraw_image, original_image.convert('RGBA')).show()
