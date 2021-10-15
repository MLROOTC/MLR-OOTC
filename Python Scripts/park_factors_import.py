import db_controller as db
import sheets_reader as sheets

table = 'Win Expectancy'
sheet_id = '1uBhS7LKsthvimuDFrF4BtMW5bNrrwugGGviPT5McRAc'
page_name = 'Parks'

rows = sheets.read_sheet(sheet_id, page_name)

for row in rows:
    if row[0] != 'Name':
        park = (row[0], float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), row[1])
        sql = '''UPDATE parkFactors SET parkName=%s, rangeHR=%s, range3B=%s, range2B=%s, range1B=%s, rangeBB=%s WHERE team=%s'''
        db.update_database(sql, park)
