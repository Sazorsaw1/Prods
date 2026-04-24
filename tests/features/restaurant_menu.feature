Feature: Restaurant homepage browsing
  The customer homepage should keep the menu and featured sections easy to browse.

  Scenario: Load the homepage with the main actions
    Given the customer homepage is open
    Then the customer homepage shows the main actions

  Scenario: Search for a matching menu item
    Given the customer homepage is open
    When the user searches for "Avocado"
    Then only menu cards matching "Avocado" are shown

  Scenario: Search for a menu item that does not exist
    Given the customer homepage is open
    When the user searches for "RandomFood123"
    Then the empty search state is shown

  Scenario: Filter the menu by dessert
    Given the customer homepage is open
    When the user filters the menu by "dessert"
    Then only "dessert" menu cards are shown

  Scenario: Today's recommendation shows four menu cards
    Given the customer homepage is open
    Then today's recommendation shows four menu cards

  Scenario: People favorites section is present
    Given the customer homepage is open
    Then the people favorites section is visible

  Scenario: Chef's pick section is present
    Given the customer homepage is open
    Then the chef's pick section is visible
