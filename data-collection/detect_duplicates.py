import sqlite3


con = sqlite3.connect('debate.db')
cur = con.cursor()

rows = [*cur.execute('SELECT * FROM rounds')]

# Get all debaters
debater_codes = set()
for row in rows:
  round, debater_a_code, debater_a_name, debater_a_school, debater_b_code, result, tournament_id, tournament_name, date, _, _ = row
  debater_codes.update([debater_a_code, debater_b_code])

found_duplicate = False
for code in debater_codes:
  debater_a_rows = [row for row in rows if row[1] == code]
  debater_b_rows = [row for row in rows if row[4] == code]
  for row1 in debater_a_rows:
    for row2 in debater_b_rows:
      if row1[0] == row2[0] and row1[6] == row2[6]:
        print(row1[1], '   <--->   ', row1[4])
        found_duplicate = True

if not found_duplicate:
  print('No duplicates found!')


con.close()
