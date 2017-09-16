Feature: Header properties
  In order to interact with document headers
  As a developer using python-docx
  I need read/write properties on the Header object


  Scenario Outline: Get Header.is_linked_to_previous
    Given a header and footer <having-or-no> definition
     Then header.is_linked_to_previous is <value>
      And footer.is_linked_to_previous is <value>

    Examples: Header.is_linked_to_previous states
      | having-or-no | value |
      | having a     | False |
      | having no    | True  |

  Scenario: Get Header.body
    Given a header and footer having a definition
     Then header.body is a HeaderFooterBody object
      And header.body contains the text of the header
      And footer.body is a HeaderFooterBody object
      And footer.body contains the text of the footer

  Scenario: Write Header.body
    Given a header and footer having a definition
     When I change the text in the footer
      And I save the document
     Then the footer contains the text I added
