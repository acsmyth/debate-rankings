import sqlite3


con = sqlite3.connect('debate.db')
cur = con.cursor()

rows = [*cur.execute('SELECT * FROM rounds')]

# Get all debaters
debater_codes = set()
for row in rows:
  round, debater_a_code, debater_a_name, debater_a_school, debater_b_code, result, tournament_id, tournament_name, date, _, _ = row
  debater_codes.update([debater_a_code, debater_b_code])

# Look for people with same name but different codes
same_found = set()
for row1 in rows:
  for row2 in rows:
    if row1 == row2: continue
    if row1[2] == row2[2] and row1[1] != row2[1]:
      same_found.add((row1[2], row1[1], row2[1]))

# Exclude known ones that are valid
same_found = set([e for e in same_found if e[0] not in ('Andrew Park', 'Lula Wang', 'Michael Meng')])
for ele in same_found:
  print(ele)
if len(same_found) == 0:
  print('No duplicate codes found!')

# Look for duplicate rounds
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
  print('No duplicate rounds found!')


con.close()
