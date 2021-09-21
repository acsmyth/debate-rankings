const startYMD = Cypress.env("start");
const endYMD = Cypress.env("end");

const start = new Date(startYMD); // inclusive
const end = new Date(endYMD); // exclusive

const tournamentData = [];

const getIdFromUrl = (url) => {
  const idx = url.indexOf("?tourn_id=");
  return parseInt(url.slice(idx + 10));
};

describe("Scrape Round Data", () => {
  it("Scrape", () => {
    cy.readFile("tabroom/bid_tournament_names.json").each((tournamentName) => {
      cy.visit("https://www.tabroom.com/index/index.mhtml");
      cy.get('form[action="/index/search.mhtml"]')
        .type(tournamentName)
        .submit();
      cy.get('tr[role="row"] > td:nth-child(3)').each((date, index) => {
        const tournamentDate = new Date(date[0].innerText);
        const tournamentName = Cypress.$('tr[role="row"] > td:nth-child(1)')[
          index
        ].innerText;
        if (tournamentDate >= start && tournamentDate < end) {
          cy.get('a[href*="/index/tourn/index.mhtml?tourn_id="]:not([title])')
            .eq(index)
            .then((ele) => {
              tournamentData.push({
                id: getIdFromUrl(ele[0].href),
                name: tournamentName,
                date: date[0].innerText,
              });
            });
        }
      });
    });
    cy.writeFile(
      `tabroom/bid_tournament_ids_${startYMD}___${endYMD}.json`,
      tournamentData
    );
  });
});
