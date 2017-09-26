#!/usr/bin/python

import glob
import os

pgn_glob = 'KingBase/KingBase*.pgn'
pgn_files = glob.glob(pgn_glob)

output_dir = 'games'
try:
    os.stat(output_dir)
except OSError:
    os.mkdir(output_dir)
for filename in glob.glob(output_dir + '/*'):
    os.remove(filename)
output_files = {}

def output_game(game, depth):
    tokens = game.split(' ')
    prefix = '_'.join(tokens[:depth])
    if prefix not in output_files:
        output_files[prefix] = open(output_dir + '/' + prefix + '.pgn', 'w')
    print >>output_files[prefix], game

def close_output_files():
    for output_file in output_files.keys():
        output_files[output_file].close()
        del output_files[output_file]

for filename in pgn_files:
    with open(filename) as fh:
        game = ''
        for line in fh:
            line = line.rstrip('\r\n')
            if not line:
                continue
            if line[:1] == '[':
                continue
            if game and line[:2] == '1.':
                output_game(game, 1)
                game = ''
            game += line
            if game[-1:] != ' ':
                game += ' '
            if game[-4:] == '1-0 ' or game[-4:] == '0-1 ':
                game = game[:-5]
            if game[-8:] == '1/2-1/2 ':
                game = game[:-9]
            game = game.replace('. ', '.')
            game_new = []
            for token in game.split(' '):
                token = token.replace('+', '').replace('#', '')
                game_new.append(token.split('.')[-1])
            game = ' '.join(game_new)
        output_game(game, 1)

close_output_files()

def split_file(filename):
    prefix = filename.split('.')[0]
    depth = len(prefix.split('_'))
    with open(filename) as fh:
        for line in fh:
            line = line.rstrip('\n')
            output_game(line, depth + 1)
    close_output_files()
    os.remove(filename)

filesize_max = 4 * 1024 * 1024
exceeded_max = True
while exceeded_max:
    exceeded_max = False
    for filename in glob.glob(output_dir + '/*'):
        if os.path.getsize(filename) > filesize_max:
            split_file(filename)
            exceeded_max = True

metadata = {}
for filename in glob.glob(output_dir + '/*'):
    with open(filename) as fh:
        num_lines = len(fh.readlines())
        prefix = os.path.basename(filename).split('.')[0]
        tokens = prefix.split('_')
        sub_prefix = ''
        for length in range(1, 1 + len(tokens)):
            sub_prefix = '_'.join(tokens[:length])
            if sub_prefix not in metadata:
                metadata[sub_prefix] = 0
            metadata[sub_prefix] += num_lines

with open(output_dir + '/metadata.txt', 'w') as ofh:
    for prefix in sorted(metadata.keys()):
        print >>ofh, '\t'.join((prefix, str(metadata[prefix])))
