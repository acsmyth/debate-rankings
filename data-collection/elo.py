import re
from datetime import datetime
import copy


def lerp(x, a, b, c, d):
  return ((d - c) / (b - a)) * (x - a) + c

def time_of_round(r1):
  date_obj = datetime.strptime(r1['date'], '%Y-%m-%d')
  round_order = [
    'Round 1',
    'Round 2',
    'Round 3',
    'Round 4',
    'Round 5',
    'Round 6',
    'Round 7',
    'Round 8',
    'Round 9',
    'Runoff',
    'Run-off',
    'Trip',
    'Triples',
    'LD Triples',
    'Triple',
    'T',
    'Sextodecimals',
    'Sextos',
    'Doubles',
    'Double',
    'Doubleoctos',
    'Doubleoctofinals',
    'Double Octas',
    'Doub',
    'Dubs',
    'Dbl',
    'Partial Dubs',
    'D',
    'WAU',
    'Octos',
    'Octas',
    'Octo',
    'Octs',
    'Octofinals',
    'Octafinals',
    'Octafinal',
    'O',
    'RKR',
    'Quarters',
    'Quarter',
    'Qtrs',
    'Qrtrs',
    'Quar',
    'Quarterfinals',
    'Quarterfinal',
    'Q',
    'PB',
    'Semis',
    'Semi',
    'Semifinals',
    'S',
    'MD',
    'Finals',
    'Final',
    'F',
    'DLM',
  ]
  if r1['round'] not in round_order:
    print(r1)
  return date_obj.timestamp() + round_order.index(r1['round'])

class Debater:
  def __init__(self, code, name='', school='', rating=2500):
    self.code = code
    self.name = name
    self.school = school
    self.rating = rating
    self.debaters = None
    self.rounds = 0
    self.round_datas = []
  
  def set_rating(self, rating):
    self.rating = rating
  
  def add_round(self, round_data=None):
    self.rounds += 1
    self.round_datas.append(round_data)
  
  def get_winrate(self):
    wins = 0
    total = 0
    for rnd in self.round_datas:
      if not isinstance(rnd['result'], list):
        if (rnd['debater_a_code'] == self.code and rnd['result'] == 'W')\
            or (rnd['debater_a_code'] != self.code and rnd['result'] != 'W'):
          wins += 1
      else:
        ballots_won = sum(1 if ballot == 'W' else 0 for ballot in rnd['result'])
        a_won = ballots_won > len(rnd['result']) // 2
        if (rnd['debater_a_code'] == self.code and a_won)\
            or (rnd['debater_a_code'] != self.code and not a_won):
          wins += 1
      total += 1
    return wins/total


class EloSystem:
  def __init__(self):
    self.debaters = None
    self.rounds = None
  
  def run(self, data):
    # flatten data into per-round, remove repeats
    rounds = []
    rounds_added = set()
    for round_data in data:
      for rnd in round_data['rounds']:
        # print(rnd)
        if rnd['round'] + ' | ' + rnd['opponent_code'] + ' | ' + round_data['debater_code'] + ' | ' + round_data['tournament_id'] in rounds_added:
          continue
        round_info = {
          'round': rnd['round'],
          'debater_a_code': round_data['debater_code'],
          'debater_a_name': round_data['debater_name'],
          'debater_a_school': round_data['debater_school'],
          'debater_b_code': rnd['opponent_code'],
          'debater_b_name': rnd['opponent_name'],
          'debater_b_school': rnd['opponent_school'],
          'result': rnd['result'],
          'tournament_id': round_data['tournament_id'],
          'tournament_name': round_data['tournament_name'],
          'date': round_data['date'],
          'debater_a_elo_change': 0.0,
          'debater_b_elo_change': 0.0,
        }
        rounds.append(round_info)
        rounds_added.add(rnd['round'] + ' | ' + round_data['debater_code'] + ' | ' + rnd['opponent_code'] + ' | ' + round_data['tournament_id'])
    
    # sort all round data in chronological order
    rounds = sorted(rounds, key=time_of_round)
    debaters = {} # debater code : elo
    for round_data in rounds:
      if round_data['result'] in ('Bye', 'Bye (Loss)'):
        continue
      # round_data: has result: 'W' or result: 'L'
      code_a = round_data['debater_a_code']
      code_b = round_data['debater_b_code']
      debater_a = debaters[code_a] if code_a in debaters else Debater(round_data['debater_a_code'], round_data['debater_a_name'], round_data['debater_a_school'])
      debater_b = debaters[code_b] if code_b in debaters else Debater(round_data['debater_b_code'])
      # update debater info if was originally a debater b
      if debater_a.name == '':
        debater_a.name = round_data['debater_a_name']
        debater_a.school = round_data['debater_a_school']
      if debater_b.name == '':
        debater_b.name = round_data['debater_b_name']
        debater_b.school = round_data['debater_b_school']
      debaters[code_a] = debater_a
      debaters[code_b] = debater_b
      self.run_round(debater_a, debater_b, round_data)

    # Remove columns that were only used above
    for round_data in rounds:
      del round_data['debater_b_name']
      del round_data['debater_b_school']
    self.debaters = debaters
    self.rounds = rounds
  
  def run_round(self, debater_a, debater_b, round_data):
    debater_a_K = 20
    debater_b_K = 20

    r_a = debater_a.rating
    r_b = debater_b.rating
    expected_a = 1 / (1 + 10**((r_b - r_a) / 400))
    expected_b = 1 / (1 + 10**((r_a - r_b) / 400))
    if isinstance(round_data['result'], list):
      actual_a = sum(1 if ballot == 'W' else 0 for ballot in round_data['result']) / len(round_data['result'])
      actual_b = sum(0 if ballot == 'W' else 1 for ballot in round_data['result']) / len(round_data['result'])
      # Increase K for elim rounds with more judges
      debater_a_K *= 1.5
      debater_b_K *= 1.5
    else:
      actual_a = 1 if round_data['result'] == 'W' else 0
      actual_b = 0 if round_data['result'] == 'W' else 1

    r_a_new = r_a + debater_a_K*(actual_a - expected_a)
    r_b_new = r_b + debater_b_K*(actual_b - expected_b)
    debater_a.set_rating(r_a_new)
    debater_b.set_rating(r_b_new)
    round_data_with_elo_a = copy.copy(round_data)
    round_data_with_elo_b = copy.copy(round_data)
    round_data_with_elo_a['elo_change'] = r_a_new - r_a
    round_data_with_elo_b['elo_change'] = r_b_new - r_b
    
    round_data['debater_a_elo_change'] = r_a_new - r_a
    round_data['debater_b_elo_change'] = r_b_new - r_b

    debater_a.add_round(round_data_with_elo_a)
    debater_b.add_round(round_data_with_elo_b)
  
  def get_ratings(self):
    return copy.copy(self.debaters)
  
  def get_rounds(self):
    return copy.copy(self.rounds)
