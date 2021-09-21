export const exists = async (selector) => {
  cy.document().then(($document) => {
    const res = $document.querySelectorAll(selector);
    return !!res.length;
  });
};

export const contains = (searchText) => {
  const res = Cypress.$(`div:contains('${searchText}')`);
  return !!res.length;
};
