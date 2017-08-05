drop view if exists {0}_mid ;
create view {0}_mid as 
    select (
        select count(*)+1
        from hiscore as hi2
        where hi2.score > hi1.score
        and game="{1}"
    ) as rank,
    subid,score,
    players.badgeid as badgeid,
    players.name as name
    from hiscore as hi1 inner join players
    on players.badgeid = hi1.badgeid
    where game="{1}"
    order by score desc;

drop view if exists {0};
create view {0} as 
    select rp.rank as rank, badgeid, {0}_mid.name as name, score, rp
    from rp inner join {0}_mid on rp.rank = {0}_mid.rank;