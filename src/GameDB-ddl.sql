# Drops all tables.
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Game;
DROP TABLE IF EXISTS Tag;
DROP TABLE IF EXISTS Engine;
DROP TABLE IF EXISTS Devices;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Developer;
DROP TABLE IF EXISTS Publisher;
DROP Table IF EXISTS Final;
SET FOREIGN_KEY_CHECKS = 1;
##########################################################
# Game Relation Table
CREATE TABLE Game (
  Game_ID int not null,
  Game_name varchar(255) not null,
  Game_age_rating varchar(255),
  Game_release_date date,
  Game_DLC varchar(255),
  primary key (Game_ID)
);
CREATE TABLE Tag (
  Tag_ID int not NULL,
  Tag_name varchar(255) not Null,
  primary key (Tag_ID)
);
##########################################################
# Systems Relation Table
CREATE TABLE Engine (
  Engine_ID int not NULL,
  Engine_Name varchar(255) not NULL,
  primary key (Engine_ID)
);
CREATE TABLE Devices (
  Devices_ID int not NULL,
  Devices_Name varchar(255) not NULL,
  Devices_Type VARCHAR(255),
  primary key (Devices_ID)
);
##########################################################
# Review Relation Table
CREATE TABLE Review (
  Review_ID int not null,
  Review_title varchar(255) not null,
  Review_ReviewerName varchar(255) not null,
  Review_Comment varchar(255),
  primary key (Review_ID)
);
##########################################################
# Creator Relation Table
CREATE TABLE Developer (
  Developer_ID int not null,
  Developer_name varchar(255) not null,
  primary key (Developer_ID)
);
CREATE TABLE Publisher (
  Publisher_ID int not null,
  Publisher_name VARCHAR(255) not null,
  primary key (Publisher_ID)
);
###########################################################
Create TABLE Final (
  Final_ID int AUTO_INCREMENT not null,
  Game_ID int not null,
  Final_GameName varchar(255),
  Tag_ID int not null,
  Devices_ID int not null,
  Engine_ID int not null,
  Review_ID int not null,
  Developer_ID int not null,
  Publisher_ID int not null,
  primary key (Final_ID),
  foreign key (Game_ID) references Game(Game_ID),
  foreign key (Tag_ID) references Tag(Tag_ID),
  foreign key (Devices_ID) references Devices(Devices_ID),
  foreign key (Engine_ID) references Engine(Engine_ID),
  foreign key (Review_ID) references Review(Review_ID),
  foreign key (Developer_ID) references Developer(Developer_ID),
  foreign key (Publisher_ID) references Publisher(Publisher_ID)
);