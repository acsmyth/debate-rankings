import os

# ssh -i C:\Users\Alex\Desktop\LightsailDefaultKey-us-east-1.pem bitnami@54.198.229.178

SSH_KEY_LOCATION = r'C:\Users\Alex\Desktop\LightsailDefaultKey-us-east-1.pem'
SERVER_ADDRESS = 'bitnami@54.198.229.178'

def scp(local_path, remote_path, recursive=False):
  os.system(f'scp -i {SSH_KEY_LOCATION} {"-r" if recursive else ""} {local_path} {SERVER_ADDRESS}:{remote_path}')

def run_commands_over_ssh(*commands):
  os.system(f'ssh -i {SSH_KEY_LOCATION} {SERVER_ADDRESS} "{"; ".join(commands)}"')


# Deploy DB
scp('../data-collection/debate.db', '/home/bitnami/debate-rankings/data-collection/')
print('Deployed database!', '\n')

# Build and deploy client
os.system('cd ../site/client/ && npm install')
os.system(f'npm run build --prefix ../site/client/')
scp('../site/client/build/', '/home/bitnami/debate-rankings/site/client/', recursive=True)
run_commands_over_ssh('sudo systemctl restart nginx')
print('Deployed front-end!', '\n')

# Deploy server
scp('../site/server/bin/', '/home/bitnami/debate-rankings/site/server/', recursive=True)
scp('../site/server/public/', '/home/bitnami/debate-rankings/site/server/', recursive=True)
scp('../site/server/routes/', '/home/bitnami/debate-rankings/site/server/', recursive=True)
scp('../site/server/views/', '/home/bitnami/debate-rankings/site/server/', recursive=True)
scp('../site/server/app.js', '/home/bitnami/debate-rankings/site/server/')
scp('../site/server/package-lock.json', '/home/bitnami/debate-rankings/site/server/')
scp('../site/server/package.json', '/home/bitnami/debate-rankings/site/server/')
run_commands_over_ssh(
  'pm2 stop www',
  'PORT=3000 pm2 start ~/debate-rankings/site/server/bin/www'
)
print('Deployed back-end!', '\n')
