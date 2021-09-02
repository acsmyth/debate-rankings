describe('Scrape Tabroom', () => {
  it('Scrape', () => {
    cy.visit('https://www.tabroom.com/index/index.mhtml');
    const chooseOption = (categoryIndex, option) => {
      cy.get('div[class*="chosen-container chosen-container-single"]')
        .eq(categoryIndex)
        .click();
      cy.get('li').contains(option).click();
    };
    const navigateToPage = (circuit, year, state, country) => {
      chooseOption(1, year);
      chooseOption(2, state);
      chooseOption(3, country);
      chooseOption(0, circuit);
    };
    cy.get('select[name="state"]')
      .children()
      .each((event) => {
        const state = event[0].label;
        if (state === '') return;
        cy.log('Starting ' + state + '...');
        cy.wait(2000);
        navigateToPage('National Circuit', '2018', state, 'United States');
        cy.downloadPage('webpages_2018/WEBPAGE ' + state, 'webpages');
      });
  });
});
