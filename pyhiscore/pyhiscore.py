# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, \
    url_for, abort, render_template, flash
from wtforms import Form, StringField, IntegerField, \
    SelectField, validators
from random import randint
from shutil import copy
from time import strftime

app = Flask(__name__) # create the application instance :)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'hiscores.db'),
    SECRET_KEY='Sunny is a very nice kitty.',
    DEBUG = True,
    GAMES = [ #sql table name, full name
        ('galaga', "Galaga"),
        ('ghosts', "Ghosts 'n Goblins"),
        ('pengo', 'Pengo'),
        ('pinball', "Pinball"),
        ('skeeball', "Skee-Ball")
    ]
))

class SubmitForm(Form):
    badgeid = IntegerField('Badge ID', [validators.required()])
    name = StringField('Name', [validators.required()])
    game = SelectField('Game', [validators.required()], choices=[
        (g[1],g[1]) for g in app.config['GAMES']])
    score =IntegerField('Score', [validators.required()])
    staffname = StringField('Referee Name', [validators.optional()])

def connect_db():
    """Connects to the specific database."""
    con = sqlite3.connect(app.config['DATABASE'])
    return con

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    try:
        copy(app.config['DATABASE'],app.config['DATABASE'][:-3]+strftime('-%Y%m%d-%H%M%S')+'.db')
    except FileNotFoundError:
        print('old db not found, not backing up')
    db = get_db()
    with open(os.path.join(app.root_path, 'baseschema.sql'),'r') as schema:
        db.executescript(schema.read())
    with open(os.path.join(app.root_path, 'gameschema.sql'),'r') as schema:
        sch = schema.read()  
        for g,n in app.config['GAMES']:
            db.executescript(sch.format(g,n))
    with open(os.path.join(app.root_path, 'scoreboardschema.sql'),'r') as schema:
        db.executescript(schema.read())
    db.commit()

def populate_db():
    names = ['Arlene','Bret','Cindy','Don','Emily','Franklin','Gert',
            'Harvey','Irma','Jose','Katia','Lee','Maria','Nate','Ophelia',
            'Philippe','Rina','Sean','Tammy','Vince','Whitney']
    gameNames = [g[1] for g in app.config['GAMES']]

    db = get_db()
    for i in range(25):
        badgeid = randint(1,21)
        name = names[badgeid-1]
        game = gameNames[randint(0,4)]
        score = int(randint(20,500)*(1+badgeid*.1))*100
        db.execute('INSERT INTO submissions (badgeid, name, game, score, staffname) VALUES (?,?,?,?,?)',
            [badgeid, name, game, score, 'BOT'])
        print(badgeid, name)
        db.execute('DELETE FROM players WHERE badgeid = ?', [badgeid])
        db.execute('INSERT INTO players (badgeid, name) VALUES (?,?)', [badgeid,name])
    db.commit()

@app.cli.command('initdb')
#@app.route('/initdb-9000')
def initdb_command():
    """Initializes the database."""
    init_db()
    populate_db()
    print('Initialized the database with fake scores.')
    return('Initialized the database with fake scores.')

@app.cli.command('wipedb')
#@app.route('/wipedb-9000')
def wipedb_command():
    """Initializes the database."""
    init_db()
    print('Wiped the database.')
    return('Wiped the database.')

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def hello():
    return 'Welcome to the high score tracker!'

@app.route('/submit',methods=['GET','POST'])
def submit():
    submitForm = SubmitForm(request.form)
    if request.method == 'POST' and submitForm.validate():
        badgeid = submitForm.badgeid.data
        name = submitForm.name.data
        game = submitForm.game.data
        score = submitForm.score.data
        staffname = submitForm.staffname.data
        db = get_db()
        db.execute('INSERT INTO submissions (badgeid, name, game, score, staffname) VALUES (?,?,?,?,?)',
            [badgeid, name, game, score, staffname])
        db.execute('DELETE FROM players WHERE badgeid = ?', [badgeid])
        db.execute('INSERT INTO players (badgeid, name) VALUES (?,?)', [badgeid,name])
        db.commit()
        flash('Submission successful!')
        global updated
        updated = True
        return redirect(url_for('submit'))
    else:
        return render_template('submission_form.html',form=submitForm)

@app.route('/getname', methods=['POST'])
def getname():
    badgeid = int(request.form['badgeid'])
    print(badgeid)
    db = get_db()
    name = db.execute("SELECT name FROM players WHERE badgeid=?",(badgeid,)).fetchone()
    if name:
        return name
    else:
        return ''

@app.route('/submissions',methods=['GET','POST'])
def view_submissions():
    if request.method == 'POST':
        print(request.form)
        flash('Scores deleted!')
        db = get_db()
        for key in request.form.keys():
            print(key)
            subid = int(key[3:])
            data = list(db.execute('SELECT * FROM submissions WHERE subid=?',(subid,)).fetchone())
            print(data[1:])
            db.execute('INSERT INTO removed (subtime,badgeid, name, game, score, staffname)'+
                'VALUES (?,?,?,?,?,?)',data[1:])
            db.execute('DELETE FROM submissions WHERE subid=?',(subid,))
            db.commit()
            updated = True
        return redirect(url_for('view_submissions'))
    else:
        db = get_db()
        submissions = db.execute('SELECT * FROM submissions ORDER BY subid')
        return render_template('submissions.html',submissions=submissions)

@app.route('/removed')
def view_removed():
    db = get_db()
    removed = db.execute('SELECT * FROM removed ORDER BY subid')
    return render_template('removed.html',removed=removed)

@app.route('/update')
def check_update():
    global updated
    if updated:
        updated = False
        return 'update'
    else:
        return 'nope'

@app.route('/hiscores')
def show_hiscores():
    db = get_db()
    views = [g[0] for g in app.config['GAMES']]
    gameTitles = [g[1] for g in app.config['GAMES']]
    hiScoreData = []
    numentries = []
    for view in views:
        oneGameData = db.execute("SELECT rank,name,score,rp FROM {} LIMIT 10".format(view)).fetchall()
        hiScoreData.append(oneGameData)
        numentries.append(db.execute("SELECT COUNT(*) FROM {} LIMIT 10".format(view)).fetchone()[0])
    gameData = zip(gameTitles,hiScoreData,numentries)
    gameList = ','.join(views)
    scoreboard = db.execute("SELECT name,{},total FROM scoreboard LIMIT 15".format(gameList))
    #scoreboard = db.execute("SELECT name,total FROM scoreboard LIMIT 15")
    numleaderboard = db.execute("SELECT COUNT(*) FROM scoreboard LIMIT 15").fetchone()[0]
    return render_template('hiscores.html',data=list(gameData), scoreboard=scoreboard, numleaderboard=numleaderboard)

if __name__ == '__main__':
    global updated
    updated=False
    app.run(host= '0.0.0.0')