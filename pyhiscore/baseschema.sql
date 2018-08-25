drop table if exists status;
create table status (
  key text not null,
  value int not null
);

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

drop table if exists rp_list;
create table rp_list (
    rank integer,
    rp integer);

insert into rp_list values
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

drop view if exists game_ranking;
create view game_ranking as select
    subid,score,game,badgeid,
    (
        select count(*)+1
        from hiscore as hi2
        where hi2.score > hi1.score
        and hi2.game = hi1.game
    ) as rank
    from hiscore as hi1 
    order by game asc, score desc;
    
drop view if exists game_rp;
create view game_rp as 
    select game_ranking.*, rp 
    from rp_list inner join game_ranking on rp_list.rank = game_ranking.rank
    order by game asc, score desc;

drop view if exists total_rp;
create view total_rp as 
    select players.badgeid as badgeid, players.name as name, sum(rp) as total_rp
    from game_rp inner join players on players.badgeid = game_rp.badgeid
    group by players.badgeid
    order by total_rp desc;

drop view if exists total_ranking;
create view total_ranking as select
    (
        select count(*)+1
        from total_rp as t2
        where t2.total_rp > t1.total_rp
    ) as rank, t1.*
    from total_rp as t1
    order by rank;