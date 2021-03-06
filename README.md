# Cabana

This is a site where you can practice chess openings. You select an opening from the list and then attempt to play it on the board. You are supposed to always respond with the most commonly played continuation. If you do not the move will be taken back and you try again. See the site here: http://cabanachess.com/

## Prep

First download the latest version of KingBase in PGN ZIP format here: http://www.kingbase-chess.net/

Unzip the file and rename the folder as KingBase/ in the project directory. Then run `prep/treeify_games.py`. If successful it should generate a games/ directory.

Next download the opening name PGN file from here: http://www.chessfiles.com/download-openings.html

Copy the file ecoe.pgn to the project directory and run `prep/build_openings.py`. If successful it should generate an openings.json file.

Finally, run `prep/logo.py` to create the logo and favicon.

## Running

Install node modules: `npm install`

Install forever: `npm install -g forever`

Then run: `forever start app.js`

By default the site will be accessible at http://localhost:3000/
