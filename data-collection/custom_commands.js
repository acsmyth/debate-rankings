export const exists = async (selector) => {
  cy.document().then(($document) => {
    const res = $document.querySelectorAll(selector);
    // console.log(res);
    // console.log('exists: ' + !!res.length);
    return !!res.length;
  });
};

export const contains = (searchText) => {
  const res = Cypress.$(`div:contains('${searchText}')`);
  console.log("CONTAINS:");
  console.log(!!res.length ? "true" : "false");
  return !!res.length;
};

// export const contains = (searchText) => {
//   cy.document().then(($document) => {
//     const element = $document.evaluate(
//       `//*[contains(text(), '${searchText}')]`,
//       $document,
//       null,
//       XPathResult.FIRST_ORDERED_NODE_TYPE,
//       null
//     ).singleNodeValue;
//     console.log('xxxxxxxxx');
//     console.log(`//*[contains(text(), '${searchText}')]`);
//     console.log(element);
//     console.log('contains: ' + (element !== null));
//     console.log('yyyyyyyyy');
//     return element !== null;
//   });
// };
