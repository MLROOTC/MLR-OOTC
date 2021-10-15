import db_controller as db
import sheets_reader as sheets
import datetime

table = 'PALogs'
sheet_id = '1ALnFVxBOuk7Tp-K_Gv8t0hwrtPujYgRgsrHVnZhubDw'
mlr_pages = ['MLR S2', 'MLR S3', 'MiLR S3', 'MLR S4', 'MiLR S4', 'MLR S5', 'MiLR S5', 'MLR S6', 'MiLR S6']
sql_pa_data = 'PALogs.league, PALogs.season, PALogs.session, PALogs.gameID, PALogs.inning, PALogs.inningID, PALogs.outs, PALogs.obc, PALogs.awayScore, PALogs.homeScore, PALogs.pitcherTeam, PALogs.pitcherName, PALogs.pitcherID, PALogs.hitterTeam, PALogs.hitterName, PALogs.hitterID, PALogs.pitch, PALogs.swing, PALogs.diff, PALogs.exactResult, PALogs.oldResult, PALogs.resultAtNeutral, PALogs.resultAllNeutral, PALogs.rbi, PALogs.run, PALogs.batterWPA, PALogs.pitcherWPA, PALogs.pr3B, PALogs.pr2B, PALogs.pr1B, PALogs.prAB'
column_names = ['league', 'season', 'session', 'gameID', 'inning', 'inningID', 'outs', 'obc', 'awayScore', 'homeScore', 'pitcherTeam', 'pitcherName', 'pitcherID', 'hitterTeam', 'hitterName', 'hitterID', 'pitch', 'swing', 'diff', 'exactResult', 'oldResult', 'resultAtNeutral', 'resultAllNeutral', 'rbi', 'run', 'batterWPA', 'pitcherWPA', 'pr3B', 'pr2B', 'pr1B', 'prAB']
sql_pa_data_where = sql_pa_data.replace(',', ' = %s AND')
sql_pa_data_where += ' = %s'
sql_add_pa = '''INSERT INTO %s (%s) ''' % (table, sql_pa_data)
sql_add_pa += 'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'


def create_table():
    sql = '''CREATE TABLE `MLR-Dev`.PALogs (
  paID int(11) DEFAULT NULL,
  league varchar(255) DEFAULT NULL,
  season int(11) DEFAULT NULL,
  session int(11) DEFAULT NULL,
  gameID int(11) DEFAULT NULL,
  inning varchar(255) DEFAULT NULL,
  inningID int(11) DEFAULT NULL,
  playNumber int(11) DEFAULT NULL,
  outs int(11) DEFAULT NULL,
  obc int(11) DEFAULT NULL,
  awayScore int(11) DEFAULT NULL,
  homeScore int(11) DEFAULT NULL,
  pitcherTeam varchar(255) DEFAULT NULL,
  pitcherName varchar(255) DEFAULT NULL,
  pitcherID int(11) DEFAULT NULL,
  hitterTeam varchar(255) DEFAULT NULL,
  hitterName varchar(255) DEFAULT NULL,
  hitterID int(11) DEFAULT NULL,
  pitch int(11) DEFAULT NULL,
  swing int(11) DEFAULT NULL,
  diff int(11) DEFAULT NULL,
  exactResult varchar(255) DEFAULT NULL,
  oldResult varchar(255) DEFAULT NULL,
  resultAtNeutral varchar(255) DEFAULT NULL,
  resultAllNeutral varchar(255) DEFAULT NULL,
  rbi int(11) DEFAULT NULL,
  run tinyint(1) DEFAULT NULL,
  batterWPA varchar(255) DEFAULT NULL,
  pitcherWPA varchar(255) DEFAULT NULL,
  pr3B int(11) DEFAULT NULL,
  pr2B int(11) DEFAULT NULL,
  pr1B int(11) DEFAULT NULL,
  prAB int(11) DEFAULT NULL
)
ENGINE = INNODB,
CHARACTER SET latin1,
COLLATE latin1_swedish_ci;'''
    db.update_database(sql, ())


def update_all_pa_logs():
    for page in mlr_pages:
        game_log = sheets.read_sheet(sheet_id, page)
        season = int(page[-1])
        if 'MLR' in page:
            league = 'mlr'
        elif 'MiLR' in page:
            league = 'milr'
        else:
            league = None
        if season == 5:
            scores_column_offset = 1
        else:
            scores_column_offset = 0
        for pa_in_sheet in game_log:
            if not pa_in_sheet[0] == 'Hitter':
                hitter_name = pa_in_sheet[0]
                hitter_id = pa_in_sheet[1]
                if pa_in_sheet[2] == '':
                    swing = None
                else:
                    swing = int(pa_in_sheet[2])
                pitcher_name = pa_in_sheet[3]
                pitcher_id = pa_in_sheet[4]
                if pa_in_sheet[5] == '':
                    pitch = None
                else:
                    pitch = int(pa_in_sheet[5])
                old_result = pa_in_sheet[6]
                if pa_in_sheet[7] == '' or not pa_in_sheet[7].isdigit():
                    diff = None
                else:
                    diff = int(pa_in_sheet[7])
                inning = pa_in_sheet[8]
                outs = int(pa_in_sheet[9])
                obc = int(pa_in_sheet[10])
                if pa_in_sheet[11] == '':
                    home_score = None
                else:
                    home_score = int(pa_in_sheet[11])
                if pa_in_sheet[12] == '':
                    away_score = None
                else:
                    away_score = int(pa_in_sheet[12])
                batter_wpa = pa_in_sheet[13]
                pitcher_wpa = pa_in_sheet[14]
                rbi = int(pa_in_sheet[15])
                run = int(pa_in_sheet[16])
                inning_id = int(pa_in_sheet[17 + scores_column_offset])
                game_id = int(pa_in_sheet[18 + scores_column_offset])
                session = int(pa_in_sheet[19 + scores_column_offset])
                batter_team = pa_in_sheet[20 + scores_column_offset]
                pitcher_team = pa_in_sheet[21 + scores_column_offset]
                if len(pa_in_sheet) > 22 + scores_column_offset:
                    exact_result = pa_in_sheet[22 + scores_column_offset]
                else:
                    exact_result = None
                if len(pa_in_sheet) > 23 + scores_column_offset:
                    result_at_neutral = pa_in_sheet[23 + scores_column_offset]
                else:
                    result_at_neutral = None
                if len(pa_in_sheet) > 24 + scores_column_offset:
                    result_all_neutral = pa_in_sheet[24 + scores_column_offset]
                else:
                    result_all_neutral = None
                if len(pa_in_sheet) > 25 + scores_column_offset:
                    if pa_in_sheet[25 + scores_column_offset] == '':
                        pr_runner3B = None
                    else:
                        pr_runner3B = int(pa_in_sheet[25 + scores_column_offset])
                else:
                    pr_runner3B = None
                if len(pa_in_sheet) > 26 + scores_column_offset:
                    if pa_in_sheet[26 + scores_column_offset] == '':
                        pr_runner2B = None
                    else:
                        pr_runner2B = int(pa_in_sheet[26 + scores_column_offset])
                else:
                    pr_runner2B = None
                if len(pa_in_sheet) > 27 + scores_column_offset:
                    if pa_in_sheet[27 + scores_column_offset] == '':
                        pr_runner1B = None
                    else:
                        pr_runner1B = int(pa_in_sheet[27 + scores_column_offset])
                else:
                    pr_runner1B = None
                if len(pa_in_sheet) > 28 + scores_column_offset:
                    if pa_in_sheet[28 + scores_column_offset] == '':
                        pr_runnerAB = None
                    else:
                        pr_runnerAB = int(pa_in_sheet[28 + scores_column_offset])
                else:
                    pr_runnerAB = None
                if hitter_id == '':
                    hitter_id = None
                else:
                    hitter_id = int(hitter_id)
                if pitcher_id == '':
                    pitcher_id = None
                else:
                    pitcher_id = int(pitcher_id)
                pa = (league, season, session, game_id, inning, inning_id, outs, obc, away_score, home_score, pitcher_team,pitcher_name, pitcher_id, batter_team, hitter_name, hitter_id, pitch, swing, diff, exact_result, old_result, result_at_neutral, result_all_neutral, rbi, run, batter_wpa, pitcher_wpa, pr_runner3B, pr_runner2B, pr_runner1B, pr_runnerAB)
                sql_select = 'SELECT'
                sql_where = ' FROM PALogs WHERE'
                print(pa)
                for i in range(len(pa)):
                    sql_select += ' PALogs.%s' % column_names[i]
                    sql_where += ' PALogs.%s' % column_names[i]
                    if pa[i] == None:
                        sql_where += ' is %s'
                    else:
                        sql_where += ' = %s'
                    if i != len(pa)-1:
                        sql_select += ','
                        sql_where += ' AND'
                sql_get_pa = sql_select + sql_where
                pa_in_db = db.fetch_data(sql_get_pa, pa)
                if not pa_in_db:
                    db.update_database(sql_add_pa, pa)


def add_play_numbers():
    leagues = ['mlr', 'milr']
    seasons = db.fetch_data('''SELECT MAX(season) FROM %s''' % table, ())
    games = db.fetch_data('''SELECT MAX(gameID) FROM %s''' % table, ())
    if seasons:
        seasons = seasons[0][0]
    if games:
        games = games[0][0]

    for league in leagues:
        for season in range(seasons):
            for game in range(games):
                sql = '''SELECT PALogs.playNumber, %s FROM PALogs ''' % sql_pa_data
                sql += 'WHERE PALogs.league=%s AND PALogs.season =%s AND PALogs.gameID=%s'
                pa_log = db.fetch_data(sql, (league, season + 1, game + 1))
                if pa_log:
                    for i in range(len(pa_log)):
                        pa = pa_log[i]
                        if not pa[0]:
                            sql = '''UPDATE PALogs SET PALogs.playNumber=%s WHERE '''
                            for j in range(len(pa)):
                                sql += ' PALogs.%s' % column_names[j]
                                item = pa[j+1]
                                if item == None:
                                    sql += ' is %s'
                                else:
                                    sql += ' = %s'
                                if j != len(pa) - 2:
                                    sql += ' AND'
                                else:
                                    break
                            pa = list(pa)
                            pa[0] = i + 1
                            db.update_database(sql, tuple(pa))


def generate_pa_id():
    pa_log = db.fetch_data('''SELECT paID, playNumber, %s FROM PALogs''' % sql_pa_data, ())
    for pa in pa_log:
        if not pa[0]:
            new_pa = ['']
            if pa[2] == 'mlr':
                new_pa[0] = '1'
            elif pa[2] == 'milr':
                new_pa[0] = '2'
            else:
                new_pa[0] = 'X'
            new_pa[0] += '%s%s%s%s' % (
                str(pa[3]).zfill(2), str(pa[4]).zfill(2), str(pa[5]).zfill(3), str(pa[1]).zfill(3))
            new_pa = new_pa + list(pa[1:])
            sql = '''UPDATE PALogs SET PALogs.paID=%s WHERE PALogs.playNumber=%s AND'''
            for i in range(len(column_names)):
                sql += ' PALogs.%s' % column_names[i]
                item = pa[i+2]
                if item == None:
                    sql += ' is %s'
                else:
                    sql += ' = %s'
                if i != len(column_names) - 1:
                    sql += ' AND'
            db.update_database(sql, (tuple(new_pa)))


startTime = datetime.datetime.now()
print('Start time: ', startTime)
print('Creating table %s' % table)
# create_table()
print('%s created.' % table)
print('Scraping PA log master sheet...')
# update_all_pa_logs()
print('Fetched PA data.')
print('Calculating play numbers...')
add_play_numbers()
print('Play numbers set.')
print('Generating PA IDs...')
generate_pa_id()
print('PA IDs added.')
print('%s complete.' % table)
endTime = datetime.datetime.now()
print('End time:', endTime)
print('Elapsed time:', endTime-startTime)