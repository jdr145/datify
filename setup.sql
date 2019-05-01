--
-- Example setup file for a web database project.
--

-- create database and user, grant privileges to user
-- create database datify;
-- create user 'mysql_username' identified by 'mysql_password';
-- grant all on datify.* to 'mysql_username';
-- flush privileges;

-- select the database and create tables

use team_8;

create table user(
    user_id int not null auto_increment primary key,
    email varchar(255) not null,
    name varchar(255) not null,
    password varchar(255) not null,
    date_of_birth date
);

create table playlist(
    playlist_id int not null auto_increment primary key,
    user_id int not null, 
    name varchar(255) not null,
    date_created date,
    description varchar(255),
    plays int DEFAULT 0, 
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

create table album(
    album_id int not null auto_increment primary key,
    name varchar(255) not null,
    date_published date,
    image varchar(255),
    description varchar(255)
);

create table artist(
    artist_id int not null auto_increment primary key,
    name varchar(255) not null,
    age int,
    image varchar(255),
    bio varchar(255),
    plays int DEFAULT 0
);

create table song(
    song_id int not null auto_increment primary key,
    name varchar(255) not null,
    plays int DEFAULT 0,
    explicit ENUM('Yes', 'No') not null DEFAULT 'No',
    duration int not null,
    num int not null,
    file_loc varchar(255) not null,
    album_id int not null,
    artist_id int not null,
    FOREIGN KEY (album_id) REFERENCES album(album_id),
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id)
);

create table is_friend(
    follower int not null,
    following int not null,
    PRIMARY KEY (follower,following),
    FOREIGN KEY (follower) REFERENCES user(user_id),
    FOREIGN KEY (following) REFERENCES user(user_id)
);

create table in_library(
    user_id int not null,
    song_id int not null,
    date_added date,
    plays int DEFAULT 0,
    PRIMARY KEY (user_id,song_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (song_id) REFERENCES song(song_id)
);

-- create table has_playlist(
--     user_id int not null,
--     playlist_id int not null,
--     PRIMARY KEY (user_id,playlist_id),
--     FOREIGN KEY (user_id) REFERENCES user(user_id),
--     FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id)
-- );

create table in_playlist(
    playlist_id int not null,
    song_id int not null,
    date_added date,
    added_by int not null,
    PRIMARY KEY (playlist_id,song_id),
    FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id),
    FOREIGN KEY (song_id, added_by) REFERENCES in_library(song_id, user_id) ON DELETE CASCADE,
    FOREIGN KEY (added_by) REFERENCES user(user_id)
);

create table plays(
  user_id int not null,
  current_song_id int not null,
  previous_song_id int, 
  next_song_id int, 
  times datetime not null, 
  PRIMARY KEY (user_id, current_song_id, times), 
  FOREIGN KEY (user_id) REFERENCES user(user_id), 
  FOREIGN KEY (current_song_id) REFERENCES song(song_id), 
  FOREIGN KEY (previous_song_id) REFERENCES song(song_id), 
  FOREIGN KEY (next_song_id) REFERENCES song(song_id)
);

-- insert data into database
insert into album(album_id, name) values
	(1, 'The Click');
insert into album(album_id, name) values
	(2, 'YouTube');
insert into album(album_id, name) values
	(3, '?');

insert into artist(artist_id, name) values
	(1, 'XXXTentacion');
insert into artist(artist_id, name) values
	(2, 'George Washington');
insert into artist(artist_id, name) values
        (3, 'AJR');
    
insert into song(song_id, name, duration, num, file_loc, album_id, artist_id) values 
    (1, 'Sober Up', 218, 4, '/home', 1, 3);
insert into song(song_id, name, duration, num, file_loc, album_id, artist_id) values 
    (2, 'Lament Golden Light', 216, 1, 'Lament_Golden_Light.mp3', 2, 2);
insert into song(song_id, name, duration, num, file_loc, album_id, artist_id) values 
    (3, 'Sky Skating', 216, 2, 'Sky_Skating.mp3', 2, 2);
insert into song(song_id, name, duration, num, file_loc, album_id, artist_id) values 
    (4, 'SAD!', 167, 4, '/home', 3, 1);

insert into user(user_id, email, name, password) values 
    (1, 'abc1@case.edu', 'Alex', 'password');

insert into playlist(playlist_id, name, user_id) values 
    (1, 'Hype Music', 1);
    
insert into in_library(user_id, song_id) values
    (1, 2);
insert into in_library(user_id, song_id) values
    (1, 4);

insert into in_playlist(playlist_id, song_id, added_by) values
    (1, 2, 1);
insert into in_playlist(playlist_id, song_id, added_by) values
    (1, 4, 1);

-- insert into has_playlist(user_id, playlist_id) values 
--     (1, 1);
