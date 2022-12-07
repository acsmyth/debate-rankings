import os
import sys
import json
import time
import copy
import random
import requests


args = copy.deepcopy(sys.argv[1:])
for arg in args:
  parts = arg.split('=')
  key = parts[0]
  value = parts[1]
  if key == 'sleep':
    sleep_time = float(value)
  elif key == 'start':
    start = value
  elif key == 'end':
    end = value

with open(f'tabroom/tournament_entry_ids_{start}___{end}.json', 'r', encoding='utf-8') as file:
  entries_str = file.read()

entries_data = json.loads(entries_str)
if not os.path.isdir('round_data'):
  os.mkdir('round_data')

i = 0
print(f'Scraping {len(entries_data)} tournaments')
for tournament_id in entries_data:
  if not os.path.isdir(f'round_data/{start}___{end}/'):
    os.mkdir(f'round_data/{start}___{end}/')
  if not os.path.isdir(f'round_data/{start}___{end}/tournament_{tournament_id}/'):
    os.mkdir(f'round_data/{start}___{end}/tournament_{tournament_id}/')
  for entry_id in entries_data[tournament_id]:
    if os.path.isfile(f'round_data/{start}___{end}/tournament_{tournament_id}/entry_{entry_id}.html'):
      continue
    print(str(round(100 * entries_data[tournament_id].index(entry_id) / len(entries_data[tournament_id]), 1)) + '%, Tournament ' + str(list(entries_data).index(tournament_id) + 1) + '/' + str(len(entries_data)))
    # print(str(round(100 * entries_data[tournament_id].index(entry_id) / len(entries_data[tournament_id]), 1)) + '%, Tournament ' + str(list(entries_data).index(tournament_id) + 1) + ' of ' + str(len(entries_data)))
    url = f'https://www.tabroom.com/index/tourn/postings/entry_record.mhtml?tourn_id={tournament_id}&entry_id={entry_id}'
    print('\tRequesting ' + url)
    page = requests.get(url)
    with open(f'round_data/{start}___{end}/tournament_{tournament_id}/entry_{entry_id}.html', 'wb') as file:
      file.write(page.content)
    print('\tSleeping...', end='', flush=True)
    time.sleep((sleep_time/2) + sleep_time*random.random())
    if i % 10 == 9:
      time.sleep(2*sleep_time)      
    print()
    i += 1

