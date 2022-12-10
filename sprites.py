#!/usr/bin/env python3
# coding=utf-8

import pickle
import math

from PIL import Image, ImageFont, ImageDraw

def image_to_sprite(image):
	sprite = []
	pages_count = int(math.ceil(float(image.height)/8))
	pixels = image.load()
	rp = range(0, pages_count)
	rx = range(0, char_width)
	ry = range(0, 8)
	for p in rp:
		row = []
		for x in rx:
			byte = 0x00
			for y in ry:
				yy = (p*8)+y
				if yy > font_height-1:
					continue
				pixel = pixels[x,yy]
				if pixel == 1:
					pixel = 0
				else:
					pixel = 1
				byte = byte | (pixel << y)
			row.append(byte)
		sprite.append(row)
	return sprite

# Unicode blocks:
character_ranges = []
character_ranges.append(range(0x20, 0x7F+1)) # Basic Latin (ascii)
#character_ranges.append(range(0xA1, 0xFF+1)) # Latin-1 Supplement
#character_ranges.append(range(0x100, 0x17F+1)) # Latin Extended-A
#character_ranges.append(range(0x180, 0x24F+1)) # Latin Extended-B
#character_ranges.append(range(0x410, 0x44F+1)) # Cyrillic (только русские буквы)
#character_ranges.append([0x2103]) # ℃

weather_character_ranges = []
weather_character_ranges.append(range(0xF000, 0xF0EA+1)) # weather icons

fonts = {
	#'Arial': [ 18, 24 ],
	'NotoSansMono-Regular': [ 18, 24, 32, 38 ],
	'WeatherIcons-Regular': [ 24, 32, 38 ]
}

sprites = {}

for font_name in fonts:
	sizes = fonts[font_name]
	for size in sizes:
		key = font_name+'-'+str(size)
		print('*******************')
		print(key)
		font = ImageFont.truetype(font_name+".ttf", size, layout_engine=ImageFont.LAYOUT_RAQM)
		font_metrics = font.getmetrics()
		font_height = font_metrics[0]+font_metrics[1]
		sprites[key] = {}
		ch_ranges = weather_character_ranges if font_name == 'WeatherIcons-Regular' else character_ranges
		for character_range in ch_ranges:
			for char_code in character_range:
				char = chr(char_code)
				print(char, end=' ')
				char_width = font.getsize(char)[0]
				image = Image.new('1', (char_width, font_height), 1)
				draw = ImageDraw.Draw(image)
				draw.text((0, 0), char, font=font)
				sprite = image_to_sprite(image)
				sprites[key][char] = sprite
		print('\n')

with open('sprites.pickle', 'wb') as f:
	pickle.dump(sprites, f, protocol=2)
