drop view if exists {0};
create view {0} as
    select 
        game_rp.rank as rank,
        players.badgeid as badgeid, 
        players.name as name, 
        game_rp.score as score, 
        game_rp.rp as rp
    from game_rp inner join players on players.badgeid = game_rp.badgeid
    where game = "{1}"
    order by rp desc; 