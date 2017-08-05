import sqlite3
from random import randint

names = ['Arlene','Bret','Cindy','Don','Emily','Franklin','Gert','Harvey','Irma','Jose','Katia','Lee','Maria','Nate','Ophelia','Philippe','Rina','Sean','Tammy','Vince','Whitney']
gameNames = ['Galaga', "Ghosts 'n Goblins",'Pengo','Pinball','Skee-Ball']

with sqlite3.connect('hiscores.db') as db:
	for i in range(200):
		badgeid = randint(1,21)
		name = names[badgeid-1]
		game = gameNames[randint(0,4)]
		score = randint(20,500)*100
		db.execute('INSERT INTO submissions (badgeid, name, game, score, staffname) VALUES (?,?,?,?,?)', [badgeid, name, game, score, 'BOT'])
	db.commit()