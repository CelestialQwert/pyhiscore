drop view if exists scoreboard;
create view scoreboard as select 
	players.badgeid, players.name, 
	galaga.rp as galaga, 
	ghosts.rp as ghosts,
	pengo.rp as pengo,
	pinball.rp as pinball,
	skeeball.rp as skeeball,
	coalesce(galaga.rp,0) + coalesce(ghosts.rp,0) + coalesce(pengo.rp,0) + 
	coalesce(pinball.rp,0) + coalesce(skeeball.rp,0) as total 
	from players 
	left outer join galaga on players.badgeid = galaga.badgeid
	left outer join ghosts on players.badgeid = ghosts.badgeid 
	left outer join pengo on players.badgeid = pengo.badgeid 
	left outer join pinball on players.badgeid = pinball.badgeid 
	left outer join skeeball on players.badgeid = skeeball.badgeid 
	order by total desc;