import { contains, exists } from '../../custom_commands';

const varsityLdNames = [
  'Varsity Lincoln Douglas',
  'Varsity Lincoln-Douglas',
  'Varsity LD',
];

describe('Scrape Tournament Pages', () => {
  it('Scrape', () => {
    cy.readFile('tournament_ids.json').each((id) => {
      cy.wait(2000);
      cy.visit(`https://www.tabroom.com/index/tourn/index.mhtml?tourn_id=${id}`)
        .then(() => {
          return exists(
            'a[href*="/index/tourn/results/index.mhtml?tourn_id="]'
          );
        })
        .then((eleExists) => {
          cy.log('eleExists: ' + (eleExists ? 'true' : 'false'));
          if (!eleExists) {
            return;
          }
          cy.get('a[href*="/index/tourn/results/index.mhtml?tourn_id="]')
            .contains('Results')
            .click();

          cy.get('[class="chosen-container chosen-container-single"]').click();
          const found = false;
          varsityLdNames.some((option) => {
            cy.get('li[class="active-result"]').then(($element) => {
              if ($element.find(option).length) {
                cy.click($element);
                found = true;
                return true;
              }
            });
          });
          if (!found) return;
          cy.get('a[class="blue full nowrap"]')
            .contains('Round')
            .each((round) => {
              round.click();
              cy.log(round);
              cy.downloadPage(
                'tournament_results/RESULTS_ID_' + id + '_ROUND_'
              );
            });
        });
    });
  });
});
