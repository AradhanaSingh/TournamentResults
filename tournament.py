#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament
import psycopg2


def execute_query(query, variables=(), fetch=False, commit=False):
    conn = connect()
    curr = conn.cursor()
    curr.execute(query, variables)
    if fetch:
        out = curr.fetchall()
    else:
        out = None
    if commit:
        conn.commit()
    conn.close()
    return out


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DELETE_MATCHES = "DELETE FROM match"
    execute_query(DELETE_MATCHES, None, False, True)


def deletePlayers():
    """Remove all the player records from the database."""
    DELETE_PLAYERS = "DELETE FROM player"
    execute_query(DELETE_PLAYERS, None, False, True)


def countPlayers():
    """Returns the number of players currently registered."""
    COUNT_PLAYERS = "SELECT COUNT(*) FROM player"
    output = execute_query(COUNT_PLAYERS, None, True, False)
    no_of_players = output[0][0]
    return no_of_players


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    INSERT_PLAYER = "INSERT INTO player(name) values(%s)"
    DATA = (name, )
    execute_query(INSERT_PLAYER, DATA, False, True)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, \
    or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    GET_PLAYER_STANDINGS = ("SELECT player_id, name, (select"
                            " count(*) FROM match"
                            " WHERE player.player_id=match.winner) AS wins, "
                            " (SELECT count(*) FROM  match"
                            " WHERE player.player_id = winner"
                            " or player.player_id = loser) AS MATCHES"
                            " FROM player ORDER BY wins DESC")

    data = execute_query(GET_PLAYER_STANDINGS, None, True, False)
    return data


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    INSERT_MATCH = "INSERT INTO match VALUES(%s,%s)"
    # winner, loser
    DATA = (winner, loser,)
    execute_query(INSERT_MATCH, DATA, False, True)


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
   Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # to get player id and name from VIEW
    GET_PAIRS = "SELECT player_id,name from standing"
    data = execute_query(GET_PAIRS, None, True, False)
    swissPair = []
    length = len(data)
    # assuming even number of players
    # adding information is swissPair list
    for i in range(0, length, 2):
        pair = []
        # added player 1 id
        pair.append(data[i][0])
        pair.append(data[i][1])
        pair.append(data[i+1][0])
        pair.append(data[i+1][1])
        swissPair.append(pair)
    # print swissPair
    return swissPair
