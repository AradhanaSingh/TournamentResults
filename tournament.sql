-- To drop database tournament if it exists
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- connect to tournament database 
\c tournament

-- player table
-- serial r big serial creates a sequence behind the scenes and increments at insert time
CREATE TABLE player(name text, player_id SERIAL PRIMARY KEY);
                 
-- match table
CREATE TABLE match(
                    match_id SERIAL PRIMARY KEY,
                    winner INTEGER REFERENCES player(player_id),
                    loser INTEGER REFERENCES player(player_id),
                    CHECK (winner <> loser)
                  );
                  
-- creating VIEW standing
CREATE VIEW standing 
AS SELECT 
        player_id,
        name,
        (select count(*) FROM match WHERE player.player_id = match.winner) AS wins ,
        (select count(*)
            FROM match 
            WHERE player.player_id = match.winner or player.player_id = match.loser) 
            AS matches
FROM player ORDER BY wins DESC;
