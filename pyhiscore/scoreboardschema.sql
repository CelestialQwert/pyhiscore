drop view if exists scoreboard;
create view scoreboard as select 
	players.badgeid, players.name,
	{game_rp_as_game}
	{coalesce_game_rp_0} as total 
	from players 
	{left_outer_join}
	order by total desc;