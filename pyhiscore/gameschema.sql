drop view if exists ranked ;
create view ranked as 
    select (
        select count(*)+1
        from hiscore as hi2
        where hi2.score > hi1.score
        and hi2.game = hi1.game
    ) as rank,
    subid,score,game,
    players.badgeid as badgeid,
    players.name as name
    from hiscore as hi1 inner join players
    on players.badgeid = hi1.badgeid
    order by game asc ,score desc;