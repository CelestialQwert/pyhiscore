drop view if exists scoreboard;
create view scoreboard as 
    select 
        total_ranking.rank as rank,
        players.badgeid as badgeid, 
        players.name as name,
        {game_rp_as_game}
        total_ranking.total_rp as total_rp
    from players 
        {left_outer_join}
        left outer join total_ranking on players.badgeid = total_ranking.badgeid
    order by rank, badgeid;


--        galaga.rp as galaga,
--        pengo.rp as pengo,

--        left outer join galaga on players.badgeid = galaga.badgeid
--        left outer join pengo on players.badgeid = pengo.badgeid
