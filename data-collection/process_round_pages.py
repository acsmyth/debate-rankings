from collections import defaultdict
import os
import json
import re
import sys
import copy
import sqlite3
from lxml import html
from elo import EloSystem

start = '2021-08-01'
end = '2022-08-01'

args = copy.deepcopy(sys.argv[1:])
for arg in args:
  parts = arg.split('=')
  key = parts[0]
  value = parts[1]
  if key == 'start':
    start = value
  elif key == 'end':
    end = value

with open(f'tabroom/tournament_entry_ids_{start}___{end}.json', 'r', encoding='utf-8') as file:
  entries_str = file.read()

with open(f'tabroom/bid_tournament_ids_{start}___{end}.json', 'r', encoding='utf-8') as file:
  tournament_data_str = file.read()
tournament_data = json.loads(tournament_data_str)


def convert_code_for_20873(code):
  name_parts = code.split(' ')[-2 :]
  letter_code = ''.join(w[0] for w in name_parts)

  name = ' '.join(name_parts)
  school = code[ : code.index(name)].strip()

  return school + ' ' + letter_code

results_data = []
debater_info_by_name = defaultdict(set)

entries_data = json.loads(entries_str)

tournament_ids_ordered = list(entries_data.keys())

# Put last because of weird debater code formats
tournament_ids_ordered.remove('20873')
tournament_ids_ordered.append('20873')

tournament_ids_ordered.remove('20714')
tournament_ids_ordered.append('20714')

tournament_ids_ordered.remove('20436')
tournament_ids_ordered.append('20436')


for tournament_id in tournament_ids_ordered:
  date = next(e['date'] for e in tournament_data if e['id'] == int(tournament_id))
  name = next(e['name'] for e in tournament_data if e['id'] == int(tournament_id))
  for entry_id in entries_data[tournament_id]:
    if not os.path.exists(f'round_data/{start}___{end}/tournament_{tournament_id}/entry_{entry_id}.html'):
      continue
    with open(f'round_data/{start}___{end}/tournament_{tournament_id}/entry_{entry_id}.html', 'rb') as file:
      page_str = file.read().decode('utf-8')
    tree = html.fromstring(page_str)
    
    debater_code = tree.xpath('//div[@class="main"]/div/span/h6/text()')[0].strip()
    debater_code = debater_code.replace('\n', '').replace('\t', '').replace('  ', ' ')
    if ':' in debater_code:
      debater_code = debater_code.split(':')[-1]
      letter_code = debater_code.split(' ')[-1]
      if len(letter_code) == 3 and (letter_code[0] + letter_code[1]).isupper() and letter_code[2].islower():
        debater_code = debater_code[ : debater_code.rindex(' ')] + ' ' + letter_code[ : 2]

    debater_name = tree.xpath('//div[@class="main"]/div/span/h4/text()')[0].strip()
    debater_name = re.sub('\s+', ' ', debater_name)

    debater_school = debater_code[ : debater_code.rindex(' ')]
    if tournament_id == '20873':
      debater_initials = ''.join(w[0] for w in debater_name.split(' '))
      debater_school = debater_code[ : debater_code.index(debater_name)].strip()
      debater_code = debater_school + ' ' + debater_initials
    elif tournament_id == '20436':
      if debater_name in debater_info_by_name and len(debater_info_by_name[debater_name]) == 1:
        debater_code, debater_school = next(iter(debater_info_by_name[debater_name]))
      elif debater_name in debater_info_by_name:
        manual_translations = {
          'Ansh Sheth': ('Harker AS', 'Harker'),
          'Max Perin': ('Sage MP', 'Sage'),
          'Muzzi Khan': ('Muzzi Khan', 'Harker'),
          'Sofia Shah': ('Harker SS', 'Harker'),
          'Rahul Mulpuri': ('Harker RM', 'Harker'),
        }
        debater_code, debater_school = manual_translations[debater_name]
      else:
        # Do nothing, since this is their first tournament so the code will be whatever it is
        pass

    # 2018-2019 format
    # debater_school = tree.xpath('//div[@class="main"]/div/span/h6/text()')[0].strip()
    # debater_name = tree.xpath('//div[@class="main"]/div/span/h4/text()')[0].strip()
    # debater_code = tree.xpath('//div[@class="main"]/h2/text()')[0].strip()

    debater_info_by_name[debater_name].add((debater_code, debater_school))


    round_rows = tree.xpath('//div[@class="main"]/div[contains(@class, "row")]')
    rounds = []
    for row in reversed(round_rows):
      # chronological order
      if len(row[3]) == 0:
        continue
      elif len(row[3]) == 1:
        opponent_code = row[2][0].text.strip()[3:]
        if tournament_id == '20873':
          opponent_code = convert_code_for_20873(opponent_code)

        rounds.append({
          'round': row[0].text.strip(),
          'side': row[1].text.strip(),
          'opponent_code': opponent_code,
          'opponent_id': int(row[2][0].get('href')[row[2][0].get('href').index('&entry_id=')+10:]),
          'judge': row[3][0][0][0].text.strip(),
          'result': row[3][0][1].text.strip(),
          'speaker_points': float(row[3][0][2][0][0].text.strip()) if len(row[3][0]) > 2 and len(row[3][0][2]) > 0 else -1
        })
      else:
        opponent_code = row[2][0].text.strip()[3:]
        if tournament_id == '20873':
          opponent_code = convert_code_for_20873(opponent_code)

        result = [row[3][i][1].text.strip() for i in range(len(row[3]))]
        speaker_points  =float(row[3][0][2][0][0].text.strip()) if len(row[3][0]) > 2 and len(row[3][0][2]) > 0 else -1

        if 'W' not in result and 'L' not in result:
          if row[1].text.strip() == 'Bye':
            result = 'Bye'
          else:
            result = 'Bye (Loss)'

        rounds.append({
          'round': row[0].text.strip(),
          'side': row[1].text.strip(),
          'opponent_code': opponent_code,
          'opponent_id': int(row[2][0].get('href')[row[2][0].get('href').index('&entry_id=')+10:]),
          'judge': [row[3][i][0][0].text.strip() for i in range(len(row[3]))],
          'result': result,
          'speaker_points': speaker_points,
        })

    debater_tournament_results = {
      'debater_code': debater_code,
      'debater_name': debater_name,
      'debater_school': debater_school,
      'tournament_id': tournament_id,
      'tournament_name': name,
      'date': date,
      'entry_id': entry_id,
      'rounds': rounds
    }
    results_data.append(debater_tournament_results)


def confidence(num_rounds):
  if num_rounds >= 35:
    return 'high'
  elif num_rounds >= 15:
    return 'medium'
  else:
    return 'low'
  
elo_system = EloSystem()
elo_system.run(results_data)
tierlist = elo_system.get_ratings()

tierlist = sorted([(e, tierlist[e].name, tierlist[e].school, round(tierlist[e].rating), tierlist[e].rounds, confidence(tierlist[e].rounds), tierlist[e].get_winrate()) for e in tierlist], key=lambda tup: tup[3], reverse=True)
tierlist_str = str(tierlist)
tierlist_str = tierlist_str[1:-1]

rounds = elo_system.get_rounds()
for r in rounds:
  if isinstance(r['result'], list):
    r['result'] = str(r['result']).replace('\'', '"')
rounds_str = str([tuple(r.values()) for r in rounds])
rounds_str = rounds_str[1:-1]


def table_exists(table, cur):
  return [e for e in cur.execute(f'''SELECT count(*) FROM sqlite_master
                                    WHERE type='table'
                                    AND name='{table}';''')][0][0] == 1

con = sqlite3.connect('debate.db')
cur = con.cursor()

# store rankings
if table_exists('rankings', cur):
  if table_exists('rankings_backup', cur):
    cur.execute('DELETE FROM rankings_backup')
  else:
    cur.execute('''CREATE TABLE rankings_backup
                   (code, name, school, elo, num_rounds, confidence, winrate)''')
  cur.execute('INSERT INTO rankings_backup SELECT * FROM rankings')
  cur.execute('DELETE FROM rankings')
else:
  cur.execute('''CREATE TABLE rankings
                 (code, name, school, elo, num_rounds, confidence, winrate)''')
cur.execute(f'INSERT INTO rankings VALUES {tierlist_str}')
con.commit()

# store round info
if table_exists('rounds', cur):
  if table_exists('rounds_backup', cur):
    cur.execute('DELETE FROM rounds_backup')
  else:
    cur.execute('''CREATE TABLE rounds_backup
                   (round, debater_a_code, debater_a_name, debater_a_school, debater_b_code, result, tournament_id, tournament_name, date, debater_a_elo_change, debater_b_elo_change)''')
  cur.execute('INSERT INTO rounds_backup SELECT * FROM rounds')
  cur.execute('DELETE FROM rounds')
else:
  cur.execute('''CREATE TABLE rounds
                 (round, debater_a_code, debater_a_name, debater_a_school, debater_b_code, result, tournament_id, tournament_name, date, debater_a_elo_change, debater_b_elo_change)''')
cur.execute(f'INSERT INTO rounds VALUES {rounds_str}')

con.commit()
con.close()
