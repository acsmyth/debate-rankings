from collections import defaultdict
import os
import json
import re
import sys
import copy
import sqlite3
from lxml import html
from elo import EloSystem


start = '2022-08-01'
end = '2023-08-01'

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


def move_to_end(x, l):
  l.remove(x)
  l.append(x)

def manual_code_translation(debater_code):
  manual_translations = {
    'Southlake Carroll Shetty': 'Southlake Carroll AS',
    'Oak Ridge INDEPENDENT AH': 'Oak Ridge AH',
    'Oak Ridge INDEPENDENT AA': 'Oak Ridge AA', 
    'Central Jersey Senior AS': 'Princeton AS',
    'Princeton Independent AS': 'Princeton AS',
    'Central Jersey Senior SS': 'Princeton SS',
    'East Independent PG': 'Plano East PG',
    'Troy Independent AP': 'Troy AP',
    'Athenian Independent EY': 'Athenian EY',
    'BASIS Independent School Silicon Valley JK': 'BASIS Independent Silicon Valley JK',
    'Damien HS and St. Lucy’s Priory AM': 'Damien AM',
    'South Eugene Independent KS': 'South Eugene KS',
    'Strake MM': 'Strake Jesuit MM',
    'Easter LW': 'Eastern LW',
    'Ridge RDa': 'Ridge RD',
    'Basis Idep SiVal Idep SK': 'BASIS Independent Silicon Valley Independent SK',
    'Independent Hamilton AL': 'Hamilton AL',
    'Independent Hamilton GB': 'Hamilton GB',
    'Ridge SNa': 'Ridge SN',
    'Lexington MLe': 'Lexington ML',
    'William P. Clements Independent KK': 'William P. Clements KK',
    'Dripping Springs CD': 'Dripping Springs CDLS',
    'NorChr JH': 'Northland Christian JH',
    'Northland Christian Hao': 'Northland Christian JH',
    'Height AW': 'Heights AW',
    'CleSpr EG': 'Clear Springs EG',
    'Lexton ARa': 'Lexington AR',

    # old season
    'Lexington AMa': 'Lexington AM',
    'Acton-Boxborough ALi': 'Acton-Boxborough AL',
    'BASIS Independent Silicon Valley SK': 'BASIS Independent Silicon Valley Independent SK',
    'Lake Highland Prep ArVe': 'Lake Highland Prep AV',
    'Lake Highland Prep AVe': 'Lake Highland Prep AV',
    'Southlake Carroll EP': 'Southlake Carroll EP',
    'Harker RMu': 'Harker RM',
    'Westwood VLo': 'Westwood VL',
    'Princeton Independent VC': 'Princeton VC',
    'Evergreen Valley Independent SS': 'Evergreen Valley SS',
    'Princeton Independent JG': 'Princeton JG',
    'OA Independent VD': 'Oxford VD',
    'OA Independent VD': 'Oxford VM',
    'Harker ASh': 'Harker AS',
    'Harker SSh': 'Harker SS',
    'Sage Hill MP': 'Sage MP',
    'Plano Independent NG': 'Plano East NG',
    'Sidwell Independent SW': 'Sidewell SW',
    'Millard North Independents NL': 'Millard North NL',
    'Sammamish Independent LW': 'Sammamish LW',
    'Samammish LW': 'Sammamish LW',
    'St Croix Prep ADe': 'St Croix Prep AD',
    'William P. Clements Independent MM': 'William P. Clements MM',
    'Westwood DLi': 'Westwood DL',
    'Muzzi Khan': 'Harker MK',
  }
  if debater_code in manual_translations:
    return manual_translations[debater_code]
  return debater_code

def manual_school_translation(debater_school):
  manual_translations = {
    'Muzzi': 'Harker',
  }
  if debater_school in manual_translations:
    return manual_translations[debater_school]
  return debater_school

results_data = []
debater_info_by_name = defaultdict(set)
debater_info_by_code = defaultdict(set)
debater_code_alias_mappings = {}

entries_data = json.loads(entries_str)

tournament_ids_ordered = list(entries_data.keys())



# Should be unnecessary since repeats what the alias mapping does
# def convert_code_for_weird_format_tournaments(code, tournament_id):
#   if 'BrxSci' in code:
#     return code.replace('BrxSci', 'Bronx Science')

#   if tournament_id == '22938':
#     if code == '0': return code
#     school = code[ : code.rindex(' ')].strip()
#     last_name = code[code.rindex(' ') + 1 : ].strip()
    
#     # Try to pattern match with known data
#     matched_code = None
#     for name, debater_infos in debater_info_by_name.items():
#       for debater_info in debater_infos:
#         if last_name in name and (debater_info[0].startswith(school) \
#             or school.startswith(debater_info[0].split(' ')[0])) \
#             and debater_info[0].endswith(last_name[0]):
#           matched_code = debater_info[0]
#           break
#       if matched_code:
#         break
    
#     # Some manual fixes
#     if code in ('Cinco Ranch Muralidharan', 'Barbers Hill Conner', 'Cinco Ranch Barazi',
#                 'Northland Christian Hao', 'L C Anderson Hiller', 'Stephen F Austin Goodgame',
#                 'Langham Creek White', 'Langham Creek White', 'Claudia Taylor Johnson Abrams',
#                 'Westwood Premkumar'):
#       matched_code = code

#     # If still no match, let it be what it was before
#     if matched_code is None:
#       raise Exception('bad', code)

#     return matched_code
#   elif tournament_id == '24359':
#     # print(code)
#     parts = code.split(' ')
#     name_parts = parts[-2 : ]
#     name = ' '.join(name_parts).strip()
#     school = ' '.join(parts[ : -2]).strip()

#     maybe_code = school + ' ' + ''.join(w[0].upper() for w in name_parts)

#     if name in debater_info_by_name and len(debater_info_by_name[name]) == 1:
#       debater_code, debater_school = next(iter(debater_info_by_name[name]))
#       if debater_school == school:
#         # Valid, checks out, since name and school matches
#         return debater_code
#       else:
#         raise Exception()
#     elif name in debater_info_by_name:
#       for possible_match in debater_info_by_name[name]:
#         if possible_match[0] == maybe_code or possible_match[1] == school:
#           # Name AND code (i.e. school) matches, so valid, checks out
#           return maybe_code
#       # No match - weird
#       raise Exception(name)
#     else:
#       if maybe_code == 'Dripping Springs Colton De LS': return 'Dripping Springs CDLS'
#       raise Exception('need manual fix')
#   elif tournament_id == '24641':
#     replacements = {
#       'NewSmi': 'Newman Smith',
#     }
#     for repl in replacements:
#       if repl in code:
#         return code.replace(repl, replacements[repl])

#   return code


# Put last because of weird debater code formats
move_to_end('24641', tournament_ids_ordered)
move_to_end('22938', tournament_ids_ordered)
move_to_end('24359', tournament_ids_ordered)


for tournament_id in tournament_ids_ordered:
  date = next(e['date'] for e in tournament_data if e['id'] == int(tournament_id))
  name = next(e['name'] for e in tournament_data if e['id'] == int(tournament_id))

  # First, get load all entry pages and get debater code / name / school
  all_entry_data = []
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

    # Hardcode fix for siblings
    if entry_id == '4358428':
      debater_code = 'Lamar RM'
      debater_name = 'Rohan Mahendru'
    if entry_id == '4358430':
      debater_code = 'Lamar AM'
      debater_name = 'Aarav Mahendru'
    if entry_id == '4409247':
      debater_code  = 'Garland AGi'
      debater_name = 'Amrik Gill'
    if entry_id == '4440120':
      debater_code = 'Garland NG'
      debater_name = 'Noorpreet Gill'


    debater_name = tree.xpath('//div[@class="main"]/div/span/h4/text()')[0].strip()
    debater_name = re.sub('\s+', ' ', debater_name)
    
    # Override duplicate codes
    if debater_name == 'Amrik Gill':
      debater_code = 'Garland AGi'
    if debater_name == 'Aditi Rajvanshi':
      debater_code = 'Lexington ARaj'
    if debater_name == 'Aarush Sathu':
      debater_code = 'Southlake Carroll ASa'
    if debater_code == 'Southlake Carroll ASh':
      debater_code = 'Southlake Carroll AS'
    
    debater_school = debater_code[ : debater_code.rindex(' ')]




    original_debater_code = debater_code

    # Manual interventions
    if 'BrxSci' in debater_code:
      debater_code = debater_code.replace('BrxSci', 'Bronx Science')
      debater_school = 'Bronx Science'

    if debater_code == 'Southlake Carroll AS':
      debater_name = 'Aditya Shetty'

    if tournament_id == '24359':
      if debater_code not in ('Lexington ARaj', 'Southlake Carroll ASa'):
        debater_initials = ''.join(w[0] for w in debater_name.split(' '))
        debater_school = debater_code[ : debater_code.index(debater_name)].strip()
        debater_code = debater_school + ' ' + debater_initials
    elif tournament_id in ('24641', '22938', '25264'):
      if debater_name in debater_info_by_name and len(debater_info_by_name[debater_name]) == 1:
        debater_code, debater_school = next(iter(debater_info_by_name[debater_name]))
      elif debater_name in debater_info_by_name:
        manual_translations = {
          'Michael Meng': {
            'Strake': ('Strake Jesuit MM', 'Strake Jesuit'),
          },
          'Aditya Shetty': {
            'Southlake Carroll': ('Southlake Carroll AS', 'Southlake Carroll'),
          },
          'Shruti Narayanabhatla': {
            'Ridge': ('Ridge SN', 'Ridge'),
          },
          'Lula Wang': {
            'Easter': ('Eastern LW', 'Eastern'),
          }
        }
        debater_code, debater_school = manual_translations[debater_name][debater_school]
      else:
        # Do nothing, since first time seeing them

        # Unless this tournament, then just use the initials
        if tournament_id == '22938':
          debater_school = debater_code[ : debater_code.rindex(' ')]
          initials = ''.join(w[0] for w in debater_name.split(' '))
          debater_code = debater_school + ' ' + initials

        else:
          # print(debater_code)
          pass

    # Override duplicate
    if debater_name == 'Amrik Gill':
      debater_code = 'Garland AGi'
    if debater_name == 'Aditi Rajvanshi':
      debater_code = 'Lexington ARaj'
    if debater_name == 'Aarush Sathu':
      debater_code = 'Southlake Carroll ASa'
    
    # Make sure no excess spaces anywhere
    debater_code = re.sub('\s+', ' ', debater_code)
    debater_name = re.sub('\s+', ' ', debater_name)
    debater_school = re.sub('\s+', ' ', debater_school)

    debater_code = manual_code_translation(debater_code)
    debater_school = manual_school_translation(debater_school)

    if original_debater_code != debater_code:
      if original_debater_code in debater_code_alias_mappings and debater_code_alias_mappings[original_debater_code] != debater_code:
        raise Exception('Unexpected', original_debater_code, debater_code, debater_code_alias_mappings[original_debater_code], tournament_id)
      
      debater_code_alias_mappings[original_debater_code] = debater_code


    # 2018-2019 format
    # debater_school = tree.xpath('//div[@class="main"]/div/span/h6/text()')[0].strip()
    # debater_name = tree.xpath('//div[@class="main"]/div/span/h4/text()')[0].strip()
    # debater_code = tree.xpath('//div[@class="main"]/h2/text()')[0].strip()

    debater_info_by_name[debater_name].add((debater_code, debater_school))
    debater_info_by_code[debater_code].add((debater_name, debater_school))

    all_entry_data.append((entry_id, tree, debater_code, debater_name, debater_school))



  def fix_siblings_issues(opponent_code, row):
    # Manual fixes for weird siblings / other scenarios
    if opponent_code == 'Garland Gill':
      opponent_entry_id = row[2][0].get('href').split('=')[-1]
      if opponent_entry_id == '4409247':
        opponent_code = 'Garland AGi'
      elif opponent_entry_id == '4440120':
        opponent_code = 'Garland NG'
    elif opponent_code == 'Lamar Mahendru':
      opponent_entry_id = row[2][0].get('href').split('=')[-1]
      if opponent_entry_id == '4358428':
        opponent_code = 'Lamar RM'
      elif opponent_entry_id == '4358430':
        opponent_code = 'Lamar AM'
    elif opponent_code == 'Lexington AR':
      opponent_entry_id = row[2][0].get('href').split('=')[-1]
      if opponent_entry_id in ('4250762', '4322257'):
        opponent_code = 'Lexington ARaj'
    elif opponent_code == 'Southlake Carroll AS':
      opponent_entry_id = row[2][0].get('href').split('=')[-1]
      if opponent_entry_id == '4219491':
        opponent_code = 'Southlake Carroll ASa'
    elif opponent_code == 'Southlake Carroll ASh':
      opponent_code = 'Southlake Carroll AS'
    
    return opponent_code

  for entry_id, tree, debater_code, debater_name, debater_school in all_entry_data:
    round_rows = tree.xpath('//div[@class="main"]/div[contains(@class, "row")]')
    rounds = []
    for row in reversed(round_rows):
      # chronological order
      if len(row[3]) == 0:
        continue
      elif len(row[3]) == 1:
        opponent_code = row[2][0].text.strip()[3:]
        opponent_code = re.sub('\s+', ' ', opponent_code)
        # opponent_code = convert_code_for_weird_format_tournaments(opponent_code, tournament_id)
        opponent_code = manual_code_translation(opponent_code)
        
        if opponent_code in debater_code_alias_mappings:
          opponent_code = debater_code_alias_mappings[opponent_code]
        opponent_code = fix_siblings_issues(opponent_code, row)


        result = row[3][0][1].text.strip()
        if result not in ('W', 'L'):
          if row[1].text.strip() == 'Bye':
            result = 'Bye'
          else:
            result = 'Bye (Loss)'

        if len(debater_info_by_code[opponent_code]) > 1:
          # Do nothing, since don't know which one they are
          pass
        elif len(debater_info_by_code[opponent_code]) == 1:
          opponent_name, opponent_school = next(iter(debater_info_by_code[opponent_code]))
        else:
          opponent_name, opponent_school = '', ''

        rounds.append({
          'round': row[0].text.strip(),
          'side': row[1].text.strip(),
          'opponent_code': opponent_code,
          'opponent_name': opponent_name,
          'opponent_school': opponent_school,
          'judge': row[3][0][0][0].text.strip(),
          'result': result,
          'speaker_points': float(row[3][0][2][0][0].text.strip()) if len(row[3][0]) > 2 and len(row[3][0][2]) > 0 else -1
        })
      else:
        opponent_code = row[2][0].text.strip()[3:]
        opponent_code = re.sub('\s+', ' ', opponent_code)
        # opponent_code = convert_code_for_weird_format_tournaments(opponent_code, tournament_id)
        opponent_code = manual_code_translation(opponent_code)

        if opponent_code in debater_code_alias_mappings:
          opponent_code = debater_code_alias_mappings[opponent_code]
        opponent_code = fix_siblings_issues(opponent_code, row)

        result = [row[3][i][1].text.strip() for i in range(len(row[3]))]
        speaker_points = float(row[3][0][2][0][0].text.strip()) if len(row[3][0]) > 2 and len(row[3][0][2]) > 0 else -1

        if 'W' not in result and 'L' not in result:
          if row[1].text.strip() == 'Bye':
            result = 'Bye'
          else:
            result = 'Bye (Loss)'
        
        if len(debater_info_by_code[opponent_code]) > 1:
          # Do nothing, since don't know which one they are
          pass
        elif len(debater_info_by_code[opponent_code]) == 1:
          opponent_name, opponent_school = next(iter(debater_info_by_code[opponent_code]))
        else:
          opponent_name, opponent_school = '', ''

        rounds.append({
          'round': row[0].text.strip(),
          'side': row[1].text.strip(),
          'opponent_code': opponent_code,
          'opponent_name': opponent_name,
          'opponent_school': opponent_school,
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
