import os
from deploy_utils import scp, run_commands_over_ssh


# Deploy DB
scp('../data-collection/debate.db', '~/debate-rankings/data-collection/')
print('Deployed database!', '\n')

# Build and deploy client
os.system('cd ../site/client/ && npm install')
os.system(f'npm run build --prefix ../site/client/')
scp('../site/client/build/', '~/debate-rankings/site/client/', recursive=True)
run_commands_over_ssh('sudo systemctl restart nginx')
print('Deployed front-end!', '\n')

# Deploy server
scp('../site/server/bin/', '~/debate-rankings/site/server/', recursive=True)
scp('../site/server/public/', '~/debate-rankings/site/server/', recursive=True)
scp('../site/server/routes/', '~/debate-rankings/site/server/', recursive=True)
scp('../site/server/views/', '~/debate-rankings/site/server/', recursive=True)
scp('../site/server/app.js', '~/debate-rankings/site/server/')
scp('../site/server/package-lock.json', '~/debate-rankings/site/server/')
scp('../site/server/package.json', '~/debate-rankings/site/server/')
run_commands_over_ssh(
  'pm2 stop www',
  'PORT=3000 pm2 start ~/debate-rankings/site/server/bin/www'
)
print('Deployed back-end!', '\n')
