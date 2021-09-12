import { contains, exists } from "../../custom_commands";

const varsityLdNames = [
  "Varsity Lincoln Douglas",
  "Varsity Lincoln-Douglas",
  "Varsity LD",
  "VLD",
  "Lincoln-Douglas Debate",
  "Lincoln-Douglas",
  "Lincoln Douglas",
  "LD",
  "OLD",
];

let entryUrls = {};

const getEntryIdFromUrl = (url) => {
  const idx = url.indexOf("&entry_id=");
  return url.slice(idx + 10);
};

describe("Scrape Tournament Pages", () => {
  it("Scrape", () => {
    cy.readFile("bid_tournament_ids_2018-08-01___2019-08-01.json").each(
      (id) => {
        entryUrls[id] = [];
        cy.wait(2000);
        cy.visit(
          `https://www.tabroom.com/index/tourn/index.mhtml?tourn_id=${id}`
        );
        cy.get('a[href*="/index/tourn/results/index.mhtml?tourn_id="]')
          .contains("Results")
          .click();
        cy.get('[class*="chosen-container chosen-container-single"]').click();
        cy.get('li[class*="active-result"]')
          .then(($getResult) => {
            let ldName = false;
            $getResult.each((key) => {
              const element = $getResult[key];
              // console.log(element);
              varsityLdNames.some((name) => {
                if (element.innerText == name) {
                  // console.log("FOUND A MATCH: " + name);
                  ldName = name;
                  return true;
                }
                return false;
              });
            });
            return ldName;
          })
          .then((ldName) => {
            // cy.log(ldName);
            cy.get("li")
              .contains(new RegExp("^" + ldName + "$", "g"))
              .click({ force: true })
              .then(() => {
                if (
                  Cypress.$('a[class="chosen-single"] > span').text() !== ldName
                ) {
                  // console.log("CLICKING AGAIN " + Math.random());
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
      }
    );
    cy.writeFile("tournament_entry_ids.json", entryUrls);
  });
});
