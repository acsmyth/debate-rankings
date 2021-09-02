const startYMD = '2018-08-01';
const endYMD = '2019-08-01';

const start = new Date(startYMD); // inclusive
const end = new Date(endYMD); // exclusive

const tournamentIds = [];

const getIdFromUrl = (url) => {
  const idx = url.indexOf('?tourn_id=');
  return parseInt(url.slice(idx + 10));
};

describe('Scrape Round Data', () => {
  it('Scrape', () => {
    cy.readFile('bid_tournament_names.json').each((tournamentName) => {
      cy.wait(2000);
      cy.visit('https://www.tabroom.com/index/index.mhtml');
      cy.get('form[action="/index/search.mhtml"]')
        .type(tournamentName)
        .submit();
      cy.get('tr[role="row"] > td:nth-child(3)').each((date, index) => {
        // cy.log(index);
        // cy.log(date[0].innerText);
        const tournamentDate = new Date(date[0].innerText);
        if (tournamentDate >= start && tournamentDate < end) {
          // cy.log(getIdFromUrl(ele[0].href));
          cy.get('a[href*="/index/tourn/index.mhtml?tourn_id="]:not([title])')
            .eq(index)
            .then((ele) => {
              tournamentIds.push(getIdFromUrl(ele[0].href));
            });
        }
      });
    });
    cy.writeFile(
      `bid_tournament_ids_${startYMD}___${endYMD}.json`,
      tournamentIds
    );
  });
});
