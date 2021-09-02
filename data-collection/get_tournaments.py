import os
import json
from lxml import html

tournaments_data = []

base_path = 'data-collection/webpages_2018/'
for filename in os.listdir(base_path):
  with open(base_path + filename, 'r', encoding='utf-8') as file:
    text = file.read()
    tree = html.fromstring(text)
    res = tree.xpath('//td[@class="nospace"]/a')
    for ele in res:
      url = ele.get('href').strip()
      id_index = url.index('tourn_id=')
      id = url[id_index+9:]
      tournament_data = {
        'id': id,
        'name': ele.text.strip(),
      }
      if tournament_data['id'] not in [e['id'] for e in tournaments_data]:
        tournaments_data.append(tournament_data)

ids_list = [ele['id'] for ele in tournaments_data]
ids_json = json.dumps(ids_list)
with open('data-collection/tournament_ids.json', 'w', encoding='utf-8') as file:
  file.write(ids_json)
