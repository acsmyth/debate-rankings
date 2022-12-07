from deploy_utils import scp


scp('../data-collection/debate.db', '~/debate-rankings/data-collection/')
print('Deployed database!', '\n')
