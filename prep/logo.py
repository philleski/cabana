#!/usr/bin/python

from PIL import Image

SIZE = 256
PLANK_WIDTH = 40
COUCH_HEIGHT = 50
COUCH_LIP_HEIGHT = 30
COUCH_LIP_WIDTH = 50
DRAPE_WIDTH = 30
DRAPE_HEIGHT = 216

COLOR_WOOD = (165, 107, 53)
COLOR_COUCH = (252, 183, 131)
COLOR_SKY = (198, 254, 255)
COLOR_DRAPE = (252, 183, 131)

image = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))
		
# Sky
for x in range(SIZE):
	for y in range(SIZE):
		image.putpixel((x, y), COLOR_SKY)

# Left plank
for x in range(PLANK_WIDTH):
	for y in range(SIZE):
		image.putpixel((x, y), COLOR_WOOD)
		
# Right plank
for x in range(SIZE - PLANK_WIDTH, SIZE):
	for y in range(SIZE):
		image.putpixel((x, y), COLOR_WOOD)
		
# Bottom plank
for x in range(SIZE):
	for y in range(SIZE - PLANK_WIDTH, SIZE):
		image.putpixel((x, y), COLOR_WOOD)
		
# Top plank
for x in range(SIZE):
	for y in range(PLANK_WIDTH):
		image.putpixel((x, y), COLOR_WOOD)

# Couch base
for x in range(PLANK_WIDTH, SIZE - PLANK_WIDTH):
	for y in range(SIZE - PLANK_WIDTH - COUCH_HEIGHT, SIZE - PLANK_WIDTH):
		image.putpixel((x, y), COLOR_COUCH)
		
# Left couch lip
for x in range(PLANK_WIDTH, PLANK_WIDTH + COUCH_LIP_WIDTH):
	for y in range(SIZE - PLANK_WIDTH - COUCH_HEIGHT - COUCH_LIP_HEIGHT, SIZE - PLANK_WIDTH - COUCH_HEIGHT):
		x_frac = float(x - PLANK_WIDTH) / COUCH_LIP_WIDTH
		y_frac = float(y - (SIZE - PLANK_WIDTH - COUCH_HEIGHT - COUCH_LIP_HEIGHT)) / COUCH_LIP_HEIGHT
		if x_frac <= y_frac:
			image.putpixel((x, y), COLOR_COUCH)
			
# Right couch lip
for x in range(SIZE - PLANK_WIDTH - COUCH_LIP_WIDTH, SIZE - PLANK_WIDTH):
	for y in range(SIZE - PLANK_WIDTH - COUCH_HEIGHT - COUCH_LIP_HEIGHT, SIZE - PLANK_WIDTH - COUCH_HEIGHT):
		x_frac = float(x - (SIZE - PLANK_WIDTH - COUCH_LIP_WIDTH)) / COUCH_LIP_WIDTH
		y_frac = float(y - (SIZE - PLANK_WIDTH - COUCH_HEIGHT - COUCH_LIP_HEIGHT)) / COUCH_LIP_HEIGHT
		if x_frac >= 1 - y_frac:
			image.putpixel((x, y), COLOR_COUCH)
			
# Left drape
for x in range(PLANK_WIDTH, PLANK_WIDTH + DRAPE_WIDTH):
	for y in range(PLANK_WIDTH, PLANK_WIDTH + DRAPE_HEIGHT):
		x_frac = float(x - PLANK_WIDTH) / DRAPE_WIDTH
		y_frac = float(y - PLANK_WIDTH) / DRAPE_HEIGHT
		if x_frac <= 1 - y_frac:
			image.putpixel((x, y), COLOR_DRAPE)
			
# Right drape
for x in range(SIZE - PLANK_WIDTH - DRAPE_WIDTH, SIZE - PLANK_WIDTH):
	for y in range(PLANK_WIDTH, PLANK_WIDTH + DRAPE_HEIGHT):
		x_frac = float(x - (SIZE - PLANK_WIDTH - DRAPE_WIDTH)) / DRAPE_WIDTH
		y_frac = float(y - PLANK_WIDTH) / DRAPE_HEIGHT
		if x_frac >= y_frac:
			image.putpixel((x, y), COLOR_DRAPE)

image.save('favicon.ico')
image.save('public/img/logo.png')

