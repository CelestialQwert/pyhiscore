drop table if exists submissions;
create table submissions (
  subid integer primary key autoincrement,
  subtime datetime default current_timestamp,
  badgeid integer not null,
  name text not null,
  game text not null,
  score integer not null,
  staffname text not null
);

drop table if exists removed;
create table removed (
  subid integer primary key,
  subtime datetime,
  badgeid integer not null,
  name text not null,
  game text not null,
  score integer not null,
  staffname text not null,
  removetime datetime default current_timestamp
);

drop view if exists hiscore;
create view hiscore as 
    select subid, subtime, badgeid, 
    game, max(score) as score, staffname 
    from submissions 
    group by badgeid, game 
    order by badgeid, game;

drop table if exists players;
create table players (
  badgeid integer not null,
  name integer not null,
  unique(badgeid)
);

drop table if exists rp;
create table rp (
    rank int,
    rp int);

insert into rp values
    (1,15),
    (2,12),
    (3,10),
    (4,8),
    (5,6),
    (6,5),
    (7,4),
    (8,3),
    (9,2),
    (10,1);