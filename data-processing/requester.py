import requests
import time
import random

class Requester:
  time_can_request = time.time()
  
  @staticmethod
  def get(url=None, params=None):
    cur_time = time.time()
    if cur_time < Requester.time_can_request:
      time.sleep(Requester.time_can_request - cur_time)
    response = requests.get(url=url, params=params)
    Requester.time_can_request = time.time() + Requester.__time_to_wait()
    return response
  
  def __time_to_wait():
    return 2 + random.random()
