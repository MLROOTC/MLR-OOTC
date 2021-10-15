import db_controller as db
import sheets_reader as sheets

table = 'Win Expectancy'
sheet_id = '1uBhS7LKsthvimuDFrF4BtMW5bNrrwugGGviPT5McRAc'
page_name = 'Win Expectancy'

rows = sheets.read_sheet(sheet_id, page_name)

for row in rows:
    if row[0] and row[0] != 'Line ID':
        row = row[5:]
        for i in range(len(row)):
            if row[i] == 'SS':
                row[i] = None
            elif '%' in row[i]:
                row[i] = row[i].replace('%', '')
                row[i] = float(row[i])
            else:
                row[i] = int(row[i])
        sql = '''INSERT INTO winProbability VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        db.update_database(sql, tuple(row))
