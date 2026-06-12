
from PIL import Image, ImageDraw
import math

# Define the dimensions of the image
width = 584
height = 584

# Create a new RGBA image with transparency
image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

x_start = 268
y_start = 268
w = 48
h = 48

circle_center = (584 // 2, 584 // 2)

draw = ImageDraw.Draw(image)

circle_center = (width // 2, height // 2)
circle_radius = 202

line_spacing = 10

num_lines = 39

for i in range(1, num_lines + 1):
    y = circle_center[1] - circle_radius + i * line_spacing
    x1 = circle_center[0] - math.sqrt(circle_radius ** 2 - (y - circle_center[1]) ** 2)
    x2 = circle_center[0] + math.sqrt(circle_radius ** 2 - (y - circle_center[1]) ** 2)
    draw.line((x1, y, x2, y), fill="red")

# Draw parallel lines inside the circle
for i in range(1, num_lines + 1):
    x = circle_center[0] - circle_radius + i * line_spacing
    y1 = circle_center[1] - math.sqrt(circle_radius ** 2 - (x - circle_center[0]) ** 2)
    y2 = circle_center[1] + math.sqrt(circle_radius ** 2 - (x - circle_center[0]) ** 2)
    draw.line((x, y1, x, y2), fill="red")

# Save the image as a PNG file
image.save("static/img/red_x.png")

for i in range(1, num_lines + 1):
    y = circle_center[1] - circle_radius + i * line_spacing
    x1 = circle_center[0] - math.sqrt(circle_radius ** 2 - (y - circle_center[1]) ** 2)
    x2 = circle_center[0] + math.sqrt(circle_radius ** 2 - (y - circle_center[1]) ** 2)
    draw.line((x1, y, x2, y), fill="green")

# Draw parallel lines inside the circle
for i in range(1, num_lines + 1):
    x = circle_center[0] - circle_radius + i * line_spacing
    y1 = circle_center[1] - math.sqrt(circle_radius ** 2 - (x - circle_center[0]) ** 2)
    y2 = circle_center[1] + math.sqrt(circle_radius ** 2 - (x - circle_center[0]) ** 2)
    draw.line((x, y1, x, y2), fill="green")

# Save the image as a PNG file
image.save("static/img/green_x.png")

draw = ImageDraw.Draw(image)

for i in range(1, num_lines + 1):
    y = circle_center[1] - circle_radius + i * line_spacing
    x1 = circle_center[0] - math.sqrt(circle_radius ** 2 - (y - circle_center[1]) ** 2)
    x2 = circle_center[0] + math.sqrt(circle_radius ** 2 - (y - circle_center[1]) ** 2)
    draw.line((x1, y, x2, y), fill="yellow")

# Draw parallel lines inside the circle
for i in range(1, num_lines + 1):
    x = circle_center[0] - circle_radius + i * line_spacing
    y1 = circle_center[1] - math.sqrt(circle_radius ** 2 - (x - circle_center[0]) ** 2)
    y2 = circle_center[1] + math.sqrt(circle_radius ** 2 - (x - circle_center[0]) ** 2)
    draw.line((x, y1, x, y2), fill="yellow")

# Save the image as a PNG file
image.save("static/img/yellow_x.png")
