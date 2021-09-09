import json
import time
import random
import requests
import os


with open('tournament_entry_ids.json', 'r', encoding='utf-8') as file:
  entries_str = file.read()

entries_data = json.loads(entries_str)
if not os.path.isdir('round_data'):
  os.mkdir('round_data')

for tournament_id in entries_data:
  if not os.path.isdir(f'round_data/tournament_{tournament_id}/'):
    os.mkdir(f'round_data/tournament_{tournament_id}/')
  for entry_id in entries_data[tournament_id]:
    print(str(round(100 * entries_data[tournament_id].index(entry_id) / len(entries_data[tournament_id]), 1)) + '%, Tournament ' + str(list(entries_data).index(tournament_id) + 1) + ' of ' + str(len(entries_data)))
    # print(entry_id)
    if os.path.isfile(f'round_data/tournament_{tournament_id}/entry_{entry_id}.html'):
      # print('yup')
      continue
    url = f'https://www.tabroom.com/index/tourn/postings/entry_record.mhtml?tourn_id={tournament_id}&entry_id={entry_id}'
    print('requesting ' + url)
    page = requests.get(url)
    with open(f'round_data/tournament_{tournament_id}/entry_{entry_id}.html', 'wb') as file:
      file.write(page.content)
    print('sleeping')
    time.sleep(3 + 4*random.random())