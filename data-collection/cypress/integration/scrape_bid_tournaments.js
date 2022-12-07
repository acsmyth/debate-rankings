const startYMD = Cypress.env("start");
const endYMD = Cypress.env("end");

const varsityLdNames = [
  "Varsity Lincoln Douglas",
  "Varsity Lincoln-Douglas",
  "Varsity LD",
  "LD Varsity",
  "VLD",
  "Lincoln-Douglas Debate",
  "Lincoln-Douglas",
  "Lincoln Douglas",
  "LD",
  "OLD",
  "TOC LD",
  "Lincoln Douglas - TOC",
  "Varsity LD - Online",
  "Lincoln Douglas Varsity",
  "LD - Varsity \\(In Person\\)",
  "LD - Varsity \\(Online\\)",
];

let entryUrls = {};

const getEntryIdFromUrl = (url) => {
  const idx = url.indexOf("&entry_id=");
  return url.slice(idx + 10);
};

describe("Scrape Tournament Pages", () => {
  it("Scrape", () => {
    cy.readFile(`tabroom/bid_tournament_ids_${startYMD}___${endYMD}.json`).each(
      (tournamentData) => {
        const id = tournamentData.id;
        entryUrls[id] = [];
        cy.wait(2000);
        cy.visit(
          `https://www.tabroom.com/index/tourn/index.mhtml?tourn_id=${id}`
        );
        cy.get("body")
          .then(($body) => {
            return (
              $body.find(
                'a[href*="/index/tourn/results/index.mhtml?tourn_id="]'
              ).length > 0
            );
          })
          .then((hasResults) => {
            if (!hasResults) {
              cy.log(`No results for ${id}`);
              return;
            }
            cy.get('a[href*="/index/tourn/results/index.mhtml?tourn_id="]')
              .contains("Results")
              .click();
            cy.get(
              '[class*="chosen-container chosen-container-single"]'
            ).click();
            cy.get('li[class*="active-result"]')
              .then(($getResult) => {
                const matches = [];
                $getResult.each((key) => {
                  const element = $getResult[key];
                  varsityLdNames.some((name) => {
                    if (element.innerText == name) {
                      matches.push(name);
                      return true;
                    }
                    return false;
                  });
                });
                return matches;
              })
              .then((matches) => {
                matches.forEach((ldName) => {
                  cy.get("li")
                    .contains(new RegExp("^" + ldName + "$", "g"))
                    .click({ force: true })
                    .then(() => {
                      if (
                        Cypress.$('a[class="chosen-single"] > span').text() !==
                        ldName
                      ) {
                        cy.get("li")
                          .contains(new RegExp("^" + ldName + "$", "g"))
                          .click({ force: true });
                      }
                    });
                  cy.contains("Prelim Records").click();
                  cy.get(
                    'tr[role="row"] > td:nth-child(2) > a[href*="/index/tourn/postings/entry_record.mhtml?"]'
                  ).each((entry) => {
                    entryUrls[id].push(getEntryIdFromUrl(entry[0].href));
                  });
                });
              });
          });
      }
    );
    cy.writeFile(
      `tabroom/tournament_entry_ids_${startYMD}___${endYMD}.json`,
      entryUrls
    );
  });
});
