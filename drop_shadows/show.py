import Image
import os

def paint(left, top, image, mask):
    background.paste(image, (left, top), mask)


background = Image.open("wood.png");

titlebar = 78
left = 83
top = 133
size = 192

index = 0

for file in os.listdir('images/'):
    x1 = index % 3
    x2 = x1 * 2 + 1
    y1 = index / 3
    y2 = y1 * 2 + 1
    #print x1, y1, x2, y2
    x = left * x2 + size * x1
    y = top * y2 + size * y1 + titlebar
    icon = Image.open('images/' + file)
    black = Image.new("RGB", (192, 192), "black")
    white = Image.new("RGB", (192, 192), "white")
    shadow = Image.blend(black, white, 0.15)
    paint(x, y + 10, shadow, icon)
    paint(x, y, icon, icon)
    index = index + 1


#background.paste(foreground, (left, top + titlebar), foreground)
background.save('export.png', 'png')
