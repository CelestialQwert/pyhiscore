drop view if exists scoreboard;
create view scoreboard as  
    with s_mid as (
        select 
        players.badgeid, players.name,
        {game_rp_as_game}
        {coalesce_game_rp_0} as total 
        from players 
        {left_outer_join}
        order by total desc
    )
    select s1.*,
    (
        select count(*)+1
        from s_mid as s2
        where cast(s2.total as integer) > cast(s1.total as integer)
    ) as rank
    from s_mid as s1
    order by total desc;