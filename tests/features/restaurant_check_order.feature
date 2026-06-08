Feature: Check order modal
  Customers should get clear validation when checking an order status.

  Scenario: Open and close the check order modal
    Given the customer homepage is open
    When the user opens the check order modal
    Then the check order modal is visible
    When the user closes the check order modal
    Then the check order modal is closed

  Scenario: Checking without an order ID shows a validation message
    Given the customer homepage is open
    When the user opens the check order modal
    And the user checks an empty order ID
    Then a check order message asks for an order ID

  Scenario: Checking with a short order ID shows a validation message
    Given the customer homepage is open
    When the user opens the check order modal
    And the user enters "123" as the order ID
    And the user checks the order status
    Then a check order message asks for the 6 digit order number
