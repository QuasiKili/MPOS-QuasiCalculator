#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

# Create a 64x64 image with transparent background
img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw calculator body (rounded rectangle)
draw.rounded_rectangle([(8, 8), (56, 56)], radius=4, fill='#2C3E50', outline='#34495E', width=2)

# Draw display area (smaller rounded rectangle at top)
draw.rounded_rectangle([(12, 12), (52, 22)], radius=2, fill='#7F8C8D')

# Draw calculator buttons (grid)
button_positions = [
    # Row 1
    (14, 26), (26, 26), (38, 26),
    # Row 2
    (14, 34), (26, 34), (38, 34),
    # Row 3
    (14, 42), (26, 42), (38, 42),
]

for x, y in button_positions:
    draw.rectangle([(x, y), (x+8, y+6)], fill='#95A5A6', outline='#BDC3C7', width=1)

# Save with optimization
img.save('icon_64x64.png', 'PNG', optimize=True)
print("Icon saved as icon_64x64.png")
