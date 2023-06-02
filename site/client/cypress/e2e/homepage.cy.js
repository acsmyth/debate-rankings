/// <reference types="cypress" />

context('Home Page', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000');
  });

  it('title is present', () => {
    cy.contains('Lincoln-Douglas Debate Elo Rankings');
  });

  it('table entries are present', () => {
    cy.get('.MuiDataGrid-renderingZone').children().should('have.length.greaterThan', 0);
  });
});
