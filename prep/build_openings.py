#!/usr/bin/python
# Note: ecoe.pgn downloaded from here: http://www.chessfiles.com/openings.html

import json
import re

openings = []

names_found = set()
def list_opening(name, move_str):
	name = ' '.join(word[0].upper() + word[1:] for word in name.split(' ') if len(word) > 0)
	if name in names_found:
		return
	moves = []
	for token in move_str.rstrip(' ').split(' '):
		if re.search(r'^\d+\.$', token):
			continue
		token = token.rstrip('+')
		moves.append(token)
	openings.append({'name': name, 'moves': moves})
	names_found.add(name)

move_str = None
move_str_continuation = False
white_opening_name = None
black_opening_name = None
opening_name = None
with open('ecoe.pgn') as fh:
	for line in fh:
		line = line.rstrip('\r\n')
		white_opening_match = re.search(r'^\[White "(.*)"\]$', line)
		if white_opening_match:
			white_opening_name = white_opening_match.groups(1)[0].rstrip(' ')
			opening_name = white_opening_name
		black_opening_match = re.search(r'^\[Black "(.*)"\]$', line)
		if black_opening_match:
			black_opening_name = black_opening_match.groups(1)[0].rstrip(' ')
			if white_opening_name:
				opening_name = white_opening_name + ', ' + black_opening_name
		if not line:
			move_str_continuation = False
		if move_str_continuation:
			move_str += ' ' + line
		if line[:3] == '1. ':
			move_str = line
			move_str_continuation = True
		if line == '*':
			list_opening(opening_name, move_str)
			move_str = None
			move_str_continuation = False
			white_opening_name = None
			black_opening_name = None
			opening_name = None

def opening_sort(a, b):
	if a['name'] > b['name']:
		return 1
	if a['name'] < b['name']:
		return -1
	return 0

openings.sort(opening_sort)
openings.insert(0, {'name': 'Starting Position', 'moves': []})
			
with open('openings.json', 'w') as ofh:
	print >>ofh, json.dumps(openings)
