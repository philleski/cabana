var express = require('express');
var expressFavicon = require('express-favicon');
var fs = require('fs');

var app = express();

app.set('views', './views');
app.set('view engine', 'pug');
app.use(expressFavicon('./public/favicon.ico'));
app.use(express.static('./public'));

fs.readFile('./games/metadata.txt', {encoding: 'utf-8'}, function(err, results) {
	if(err) {
		console.error(err);
		process.exit(1);
	}
	var metadata = results
		.split('\n')
		.filter(function(line) {
			return !!line;
		})
		.map(function(line) {
			var fields = line.split('\t');
			return {
				move: fields[0],
				count: fields[1]
			};
		});
		
	fs.readFile('openings.json', {encoding: 'utf-8'}, function(err, results) {
		if(err) {
			console.error(err);
			process.exit(1);
		}
		var openings = null;
		try {
			openings = JSON.parse(results);
		} catch(e) {
			console.error(e);
			process.exit(1);
		}
	
		app.get('/', function(req, res) {
			res.render('chess_openings.pug', {metadata: metadata, openings: openings});
		});
		
		var getNextMoves = function(prefix, callback) {
			var nextMoves = [];
			var found = false;
			metadata.forEach(function(move) {
				if(prefix === '' || move.move.indexOf(prefix + '_') === 0) {
					found = true;
				}
			});
			if(found) {
				if(prefix.length) {
					prefix += '_';
				}
				metadata.forEach(function(move) {
					if(move.move.indexOf(prefix) !== 0) {
						return;
					}
					var moveSuffix = move.move.substring(prefix.length);
					if(moveSuffix.indexOf('_') === -1) {
						nextMoves.push({
							move: moveSuffix,
							count: move.count
						});
					}
				});
				nextMoves.sort(function(a, b) {
					if(parseInt(a.count) > parseInt(b.count)) {
						return -1;
					}
					if(parseInt(a.count) < parseInt(b.count)) {
						return 1;
					}
					return 0;
				});
				return callback(null, nextMoves);
			} else {
				var prefixMoves = prefix.split('_');
				var lastSubPrefixFound = null;
				for(var i = 1; i <= prefixMoves.length; i++) {
					var subPrefix = prefixMoves.slice(0, i).join('_');
					metadata.forEach(function(move) {
						if(move.move === subPrefix) {
							lastSubPrefixFound = subPrefix;
						}
					});
				}
				var filename = './games/' + lastSubPrefixFound + '.pgn';
				fs.stat(filename, function(err, results) {
					if(err) {
						return callback('Could not find file: ' + filename);
					}
					fs.readFile(filename, {encoding: 'utf-8'}, function(err, results) {
						if(err) {
							return callback('Could not read file: ' + filename);
						}
						var games = results
							.split('\n')
							.filter(function(line) {
								return !!line;
							})
							.map(function(line) {
								return line.split(' ').join('_');
							});
						games = games.filter(function(game) {
							return game.indexOf(prefix) === 0;
						});
						var nextMoveCounts = {};
						games.forEach(function(game) {
							var nextMove = game.substring(prefix.length + 1).split('_')[0];
							if(!nextMoveCounts[nextMove]) {
								nextMoveCounts[nextMove] = 0;
							}
							nextMoveCounts[nextMove]++;
						});
						var nextMoves = [];
						Object.keys(nextMoveCounts).forEach(function(nextMove) {
							nextMoves.push({
								move: nextMove,
								count: nextMoveCounts[nextMove]
							});
						});
						nextMoves.sort(function(a, b) {
							if(parseInt(a.count) > parseInt(b.count)) {
								return -1;
							}
							if(parseInt(a.count) < parseInt(b.count)) {
								return 1;
							}
							return 0;
						});
						return callback(null, nextMoves);
					});
				});
			}
		};
		
		app.get('/next_move/', function(req, res) {
			getNextMoves('', function(err, results) {
				if(err) {
					return res.status(400).send({error: err});
				}
				return res.status(200).send(results);
			});
		});
		
		app.get('/next_move/:prefix', function(req, res) {
			getNextMoves(req.params.prefix, function(err, results) {
				if(err) {
					return res.status(400).send({error: err});
				}
				return res.status(200).send(results);
			});
		});

		app.listen(3000, function() {
		});
	});
});
