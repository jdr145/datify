import configparser
from flask import Flask, render_template, request, url_for, redirect, session, escape
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
    error = ''
    return redirect(url_for('login', error=error))

# Login page
@app.route('/login', defaults={'error': None}, methods=['GET', 'POST'])
@app.route('/login/<error>', methods=['GET', 'POST'])
def login(error):
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
    if request.method == 'POST':
        if "library" in request.form:
            return redirect(url_for('library'))
        if "playlists" in request.form:
            return redirect(url_for('playlists'))
        if "friends" in request.form:
            return redirect(url_for('friends'))
    return render_template('homepage.html')

# Song library page
@app.route('/library', methods=['GET', 'POST'])
def library():
    if 'user_id' not in session:
        error = 'You are not logged in.'
        return redirect(url_for('login', error=error))
    data = {}
    if "delete-song" in request.form:
        delete_song_id = int(request.form["delete-song"])
        # sql query for deleting a song in a user's library
        sql = "delete from in_library where user_id={user_id} and song_id={delete_song_id}".format(user_id=session['user_id'], delete_song_id=delete_song_id)
        sql_execute(sql)
    # sql query to return all songs a user has in their library
    sql = "select song.song_id, song.explicit, song.name, song.album_id, album.name, song.plays, song.duration, song.file_loc, artist.name from song, album, in_library, user, artist where artist.artist_id=song.artist_id and song.album_id=album.album_id and user.user_id={user_id} and user.user_id=in_library.user_id and in_library.song_id = song.song_id order by song.name".format(user_id=session['user_id'])
    songs = sql_query(sql)
    data['songs'] = songs
    return render_template('library.html', data=data)

# User's playlists page
@app.route('/playlists', methods=['GET', 'POST'])
def playlists():
    if 'user_id' not in session:
        error = 'You are not logged in.'
        return redirect(url_for('login', error=error))
    data = {}
    # sql query to return playlists of a specific user
    ## wrong current sql query ##
    sql = "select song_id, explicit, song.name, song.album_id, album.name, plays, duration, file_loc from song, album where song.album_id = album.album_id order by song.name"
    songs = sql_query(sql)
    data['songs'] = songs
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
    return render_template('friends.html', data=data)

################# OLD #################
#@app.route('/', methods=['GET', 'POST'])
def template_response_with_data():
    print(request.form)
    data = {}
    if "login" in request.form:
        email = str(request.form["email"])
        password = str(request.form["psw"])
        # sql query to obtain user_id of an email/psw from login attempt
        sql = "select user_id from user where user.email='{email}' and user.password='{password}'".format(email=email, password=password)
        user = sql_query(sql)
        data['user'] = user[0][0]
        # on failed login attempt, return back to the login page, otherwise go to home page
        if not user:
            return render_template('login_page.html')
        return render_template('homepage.html', data=data)
    if "delete-song" in request.form:
        user_id = int(request.form["user"])
        delete_song_id = int(request.form["delete-song"])
        # sql query for deleting a song in a user's library
        sql = "delete from in_library where user_id={user_id} and song_id={delete_song_id}".format(user_id=user_id, delete_song_id=delete_song_id)
        sql_execute(sql)
        sql = "select song.song_id, song.explicit, song.name, song.album_id, album.name, song.plays, song.duration, song.file_loc, artist.name from song, album, in_library, user, artist where artist.artist_id=song.artist_id and song.album_id=album.album_id and user.user_id={user_id} and user.user_id=in_library.user_id and in_library.song_id = song.song_id order by song.name".format(user_id=user_id)
        songs = sql_query(sql)
        data['songs'] = songs
        data['user'] = user_id
        sql
        return render_template('library.html', data=data)
    if "library" in request.form:
        user_id = int(request.form["library"])
        # sql query to return all songs a user has in their library
        ## wrong current sql query ##
        sql = "select song.song_id, song.explicit, song.name, song.album_id, album.name, song.plays, song.duration, song.file_loc, artist.name from song, album, in_library, user, artist where artist.artist_id=song.artist_id and song.album_id=album.album_id and user.user_id={user_id} and user.user_id=in_library.user_id and in_library.song_id = song.song_id order by song.name".format(user_id=user_id)
        songs = sql_query(sql)
        data['songs'] = songs
        data['user'] = user_id
        return render_template('library.html', data=data)
    if "playlists" in request.form:
        user_id = int(request.form["playlists"])
        # sql query to return playlists of a specific user
        ## wrong current sql query ##
        sql = "select song_id, explicit, song.name, song.album_id, album.name, plays, duration, file_loc from song, album where song.album_id = album.album_id order by song.name"
        songs = sql_query(sql)
        data['songs'] = songs
        data['user'] = user_id
        return render_template('playlists.html', data=data)
    if "friends" in request.form:
        user_id = int(request.form["friends"])
        return render_template('friends.html', data=data)
    return render_template('login_page.html')

if __name__ == '__main__':
    app.run(**config['app'])