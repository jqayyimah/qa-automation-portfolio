describe('Login Tests', () => {
  
  beforeEach(() => {
    cy.visit('https://example.com/login'); // replace with your app's login URL
  });

  it('should login successfully with valid credentials', () => {
    cy.get('input[name="email"]').type('user@example.com');
    cy.get('input[name="password"]').type('Passw0rd!');
    cy.get('button[type="submit"]').click();

    // Assert user is redirected to dashboard/homepage
    cy.url().should('include', '/dashboard');
    cy.contains('Welcome').should('be.visible');
  });

  it('should show error with invalid password', () => {
    cy.get('input[name="email"]').type('user@example.com');
    cy.get('input[name="password"]').type('WrongPassword');
    cy.get('button[type="submit"]').click();

    // Assert error message
    cy.contains('Invalid username or password').should('be.visible');
  });

  it('should validate required fields', () => {
    cy.get('button[type="submit"]').click();

    cy.contains('Email is required').should('be.visible');
    cy.contains('Password is required').should('be.visible');
  });

});
