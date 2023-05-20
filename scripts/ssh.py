from deploy_utils import CONSTANTS
import os


os.system(f'ssh -i {CONSTANTS["ssh_key_location"]} {CONSTANTS["server_address"]}')
