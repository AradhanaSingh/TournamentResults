-- To drop database tournament
DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament

-- player table
-- serial r big serial creates a sequence behind the scenes and increments at insert time
CREATE TABLE player(name text, player_id SERIAL PRIMARY KEY);
                 
-- match table
CREATE TABLE match(
                   winner INTEGER REFERENCES player(player_id),
                   loser INTEGER REFERENCES player(player_id)
                  );
                  
-- creating VIEW standing
CREATE VIEW standing 
AS SELECT player_id,name,(select count(*) FROM match WHERE player.player_id=match.winner) AS wins 
FROM player ORDER BY wins DESC;