import json
import os


with open('constants.json', 'r') as f:
  CONSTANTS = json.loads(f.read())

def scp(local_path, remote_path, recursive=False):
  os.system(f'scp -i {CONSTANTS["ssh_key_location"]} {"-r" if recursive else ""}\
              {local_path} {CONSTANTS["server_address"]}:{remote_path}')

def run_commands_over_ssh(*commands):
  os.system(f'ssh -i {CONSTANTS["ssh_key_location"]} {CONSTANTS["server_address"]} "{"; ".join(commands)}"')
