import configparser
from flask import Flask, render_template, request, url_for, redirect, session
import mysql.connector

# Read configuration from file.
config = configparser.ConfigParser()
config.read('config.ini')

# Set up application server.
app = Flask(__name__, static_url_path='/static')

# Secret key for unique user sessions
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Create a function for fetching data from the database.
def sql_query(sql):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

# Execute a sql query in the database
def sql_execute(sql):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

# Redirect default URL to the login page
@app.route('/')
def redir():
    error = None
    return redirect(url_for('login', error=error))

# Login page
@app.route('/login', defaults={'error': None}, methods=['GET', 'POST'])
@app.route('/login/<error>', methods=['GET', 'POST'])
def login(error):
    if request.method == 'GET':
        session.clear()
    if request.method == 'POST':
        email = str(request.form["email"])
        password = str(request.form["psw"])
        # sql query to obtain user_id of an email/psw from login attempt
        sql = "select user_id from user where user.email='{email}' and user.password='{password}'".format(email=email, password=password)
        user = sql_query(sql)
        if not user:
            error = 'Invalid credentials. Please try again.'
        else:
            session['user_id'] = user[0][0]
            return redirect(url_for('homepage'))
    return render_template('login_page.html', error=error)

# Home page
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if 'user_id' not in session:
        error = 'You are not logged in.'
        return redirect(url_for('login', error=error))
    data = {}
    # sql query to return all playlists a user has
    sql = "select p.playlist_id, p.name, p.date_created, p.description, p.plays from playlist p, user u, has_playlist hp where hp.user_id={user_id} and hp.playlist_id=p.playlist_id".format(user_id=session['user_id'])
    playlists = sql_query(sql)
    data['playlists'] = playlists
    return render_template('homepage.html', data=data)

# Song library page
@app.route('/library', methods=['GET', 'POST'])
def library():
    if 'user_id' not in session:
        error = 'You are not logged in.'
        return redirect(url_for('login', error=error))
    data = {}
    if "items" in request.form:
        print(request.form["items"].split(','))
        for song_id in request.form["items"].split(','):
            print(song_id)
            sql = "update song set song.plays = song.plays + 1 where song.song_id={song_id}".format(song_id=song_id)
            sql_execute(sql)
    if "delete-song" in request.form:
        delete_song_id = int(request.form["delete-song"])
        # sql query for deleting a song in a user's library
        sql = "delete from in_library where user_id={user_id} and song_id={delete_song_id}".format(user_id=session['user_id'], delete_song_id=delete_song_id)
        sql_execute(sql)
    # sql query to return all songs a user has in their library
    sql = "select song.song_id, song.explicit, song.name, song.album_id, album.name, song.plays, song.duration, song.file_loc, artist.name from song, album, in_library, user, artist where artist.artist_id=song.artist_id and song.album_id=album.album_id and user.user_id={user_id} and user.user_id=in_library.user_id and in_library.song_id = song.song_id order by song.name".format(user_id=session['user_id'])
    songs = sql_query(sql)
    data['songs'] = songs
    # sql query to return all playlists a user has
    sql = "select p.playlist_id, p.name, p.date_created, p.description, p.plays from playlist p, user u, has_playlist hp where hp.user_id={user_id} and hp.playlist_id=p.playlist_id".format(user_id=session['user_id'])
    playlists = sql_query(sql)
    data['playlists'] = playlists
    return render_template('library.html', data=data)

# User's playlists page
#@app.route('/playlists', defaults={'name': None}, methods=['GET', 'POST'])
@app.route('/playlists/<name>', methods=['GET', 'POST'])
def playlists(name):
    if 'user_id' not in session:
        error = 'You are not logged in.'
        return redirect(url_for('login', error=error))
    data = {}
    if 'pname' in request.form:
        # sql query to create a playlist specific to a user with a pname, pdesc, and user_id
        sql = ""
        sql_execute(sql)
    # sql query to return the requested playlist of a specific user
    sql = "select s.song_id, s.explicit, s.name, s.album_id, al.name, s.plays, s.duration, s.file_loc, ar.name from song s, artist ar, album al, playlist p, in_playlist ip where s.artist_id=ar.artist_id and s.album_id=al.album_id and p.playlist_id=ip.playlist_id and p.name='{name}' and s.song_id=ip.song_id".format(name=name)
    songs = sql_query(sql)
    data['songs'] = songs
    # sql query to return all playlists a user has
    sql = "select p.playlist_id, p.name, p.date_created, p.description, p.plays from playlist p, user u, has_playlist hp where hp.user_id={user_id} and hp.playlist_id=p.playlist_id".format(user_id=session['user_id'])
    playlists = sql_query(sql)
    data['playlists'] = playlists
    return render_template('playlists.html', data=data)

# Friends page
@app.route('/friends', methods=['GET', 'POST'])
def friends():
    if 'user_id' not in session:
        error = 'You are not logged in.'
        return redirect(url_for('login', error=error))
    data = {}
    # sql query to return friends of a user
    ## wrong current sql query ##
    sql = "select u.name, u.email from user u, is_friend f where f.follower={user_id}".format(user_id=session['user_id'])
    friends = sql_query(sql)
    data['friends'] = friends
    # sql query to return all playlists a user has
    sql = "select p.playlist_id, p.name, p.date_created, p.description, p.plays from playlist p, user u, has_playlist hp where hp.user_id={user_id} and hp.playlist_id=p.playlist_id".format(user_id=session['user_id'])
    playlists = sql_query(sql)
    data['playlists'] = playlists
    return render_template('friends.html', data=data)

# Search page
@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        error = 'You are not logged in.'
        return redirect(url_for('login', error=error))
    data = {}
    if "items" in request.form:
        for song_id in request.form["items"].split(','):
            print(song_id)
            sql = "update song set song.plays=song.plays+1 where song.song_id={song_id}".format(song_id=song_id)
            sql_execute(sql)
    if "add-song" in request.form:
        add_song_id = int(request.form["add-song"])
        # sql query for adding a song to a user's library
        sql = "insert into in_library(user_id, song_id) values({user_id}, {add_song_id})".format(user_id=session['user_id'], add_song_id=add_song_id)
        sql_execute(sql)
    data['query'] = str(request.form['search'])
    clean_query = string_cleaner(str(request.form['search']))
    print(data['query'])
    # sql query to return search results
    sql = "select song.song_id, song.explicit, song.name, song.album_id, album.name, song.plays, song.duration, song.file_loc, artist.name from song, album, artist where artist.artist_id=song.artist_id and song.album_id=album.album_id and song.name like '%{query}%' order by song.name".format(query=clean_query)
    results = sql_query(sql)
    data['results'] = results
    # sql query to return all playlists a user has
    sql = "select p.playlist_id, p.name, p.date_created, p.description, p.plays from playlist p, user u, has_playlist hp where hp.user_id={user_id} and hp.playlist_id=p.playlist_id".format(user_id=session['user_id'])
    playlists = sql_query(sql)
    data['playlists'] = playlists
    return render_template('search.html', data=data)

def string_cleaner(phrase):
    new = ""
    for i in phrase:
        if i == '\'':
            new = new + "\\\'"
        else:
            new = new + i
    return new

if __name__ == '__main__':
    app.run(**config['app'])