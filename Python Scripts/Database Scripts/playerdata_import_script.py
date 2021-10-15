import db_controller as db
import sheets_reader as sheets

sheet_id = '1uBhS7LKsthvimuDFrF4BtMW5bNrrwugGGviPT5McRAc'
page_name = 'Player List'

rows = sheets.read_sheet(sheet_id, page_name)
for row in rows:
    if row[0] != 'Player ID':
        player_id = int(row[0])
        player_name = row[1]
        team = row[2]
        batting_type = row[3]
        pitching_type = row[4]
        pitching_bonus = row[5]
        hand = row[6]
        pos1 = row[7]
        pos2 = row[8]
        pos3 = row[9]
        reddit_name = row[10]
        discord_name = row[11]
        status = int(row[13])
        player_in_sheet = (player_name, team, batting_type, pitching_type, pitching_bonus, hand, pos1, pos2, pos3, reddit_name, discord_name, status, player_id)

        sql = '''SELECT playerName, Team, batType, pitchType, pitchBonus, hand, priPos, secPos, tertPos, redditName, discordName, Status, playerID FROM playerData WHERE playerID = %s'''
        player_in_db = db.fetch_data(sql, (player_id,))
        if player_in_db:
            player_in_db = player_in_db[0]
        else:
            sql = '''INSERT INTO playerData (playerName, Team, batType, pitchType, pitchBonus, hand, priPos, secPos, tertPos, redditName, discordName, Status, playerID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            db.update_database(sql, player_in_sheet)
            continue
        if player_in_db != player_in_sheet:
            sql = '''UPDATE playerData SET playerName=%s, Team=%s, batType=%s, pitchType=%s, pitchBonus=%s, hand=%s, priPos=%s, secPos=%s, tertPos=%s, redditName=%s, discordName=%s, Status=%s WHERE playerID=%s'''
            db.update_database(sql, player_in_sheet)
