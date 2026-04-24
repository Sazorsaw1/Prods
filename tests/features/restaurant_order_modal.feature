Feature: Create order modal
  Customers should be able to interact with the create order modal safely.

  Scenario: Open and close the create order modal
    Given the customer homepage is open
    When the user opens the create order modal
    Then the create order modal is visible
    When the user closes the create order modal
    Then the create order modal is closed

  Scenario: Submitting without a table shows an alert
    Given the customer homepage is open
    When the user opens the create order modal
    And the user submits the order without selecting a table
    Then an alert asks for a table number

  Scenario: Submitting without a menu item shows an alert
    Given the customer homepage is open
    When the user opens the create order modal
    And the user chooses Table 1
    And the user submits the order without selecting a menu item
    Then an alert asks for at least one menu item

  Scenario: Selecting an item and increasing quantity updates the total
    Given the customer homepage is open
    When the user opens the create order modal
    And the user selects the first available order item
    And the user increases the first available order item quantity
    Then the total price increases above zero

  Scenario: Deselecting an item resets the total
    Given the customer homepage is open
    When the user opens the create order modal
    And the user selects the first available order item
    And the user deselects the first available order item
    Then the total price returns to zero
