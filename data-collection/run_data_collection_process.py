import os

start = '2022-08-01'
end = '2023-08-01'
sleep_time = 3
PYTHON = 'python3' if os.name == 'posix' else 'python'


# Scrape tournament ids
os.system(f'npx cypress run --spec "cypress/integration/scrape_tournament_ids.js" --env start="{start}",end="{end}"')

# # Scrape entries from each tournament
os.system(f'npx cypress run --spec "cypress/integration/scrape_bid_tournaments.js" --env start="{start}",end="{end}"')

# # Get round pages for each entry
os.system(f'{PYTHON} get_round_pages.py start="{start}" end="{end}" sleep={sleep_time}')

# # Process round pages for each entry
os.system(f'{PYTHON} process_round_pages.py start="{start}" end="{end}"')
