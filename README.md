Rule Engine with AST


Overview
This project implements a 3-tier rule engine that determines user eligibility based on attributes such as age, department, income, and experience. The system leverages an Abstract Syntax Tree (AST) to represent conditional rules, allowing for dynamic creation, combination, and evaluation of rules.

Key Features:
AST Representation: Each rule is parsed and converted into an AST, which can be dynamically created and modified.
Rule Combination: Multiple rules can be combined efficiently using logical operators (AND, OR).
Rule Evaluation: Rules can be evaluated against user data to determine eligibility.
Storage: Rules and metadata are stored in an SQLite database.

Prerequisites
Before running the project, make sure you have the following installed:
Python 3.x: You can download it from Python's official website.
SQLite: Comes pre-installed with Python. You can also download it here if needed.

Setup Instructions
Clone or Download the Repository:
Download the project files or clone the repository into your local machine.

Set Up Virtual Environment (Optional but Recommended): Open a terminal in the project folder and run the following commands:
bash
Copy code
# Create a virtual environment
python -m venv env
# Activate the virtual environment
# On Windows:
.\env\Scripts\activate
# On macOS/Linux:
source env/bin/activate

Install Dependencies: There are no third-party libraries required for this project. Ensure Python and SQLite are installed.

Create the SQLite Database:
The code automatically creates a database called rules.db if it does not exist. This is handled in the setup_db() function.

Run the Application:
Open a terminal inside the project folder and run the following command to execute the application:
bash
Copy code
python rule_engine.py

Project Structure:
RuleEngineProject/
    ├── env/                 # Optional virtual environment folder
    ├── rule_engine.py        # Main Python file
    ├── rules.db              # SQLite database file (auto-generated)
    ├── README.md             # Project README file

Functionality
1. create_rule(rule_string):
Converts a rule string into an AST representation.
Example Rule:
python
Copy code
rule1 = "((age > 30 AND department == 'Sales') OR (age < 25 AND department == 'Marketing')) AND (salary > 50000 OR experience > 5)"
ast1 = create_rule(rule1)
2. combine_rules(rules):
Combines multiple ASTs into a single AST using logical operators like AND or OR.
Example:
python
Copy code
combined_ast = combine_rules([rule1, rule2])
3. evaluate_rule(ast, data):
Evaluates the rule AST against user-provided data (in dictionary format) and returns True if the user meets the conditions, False otherwise.
Example Data:
python
Copy code
data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
result = evaluate_rule(ast, data)

Testing
The main Python file (rule_engine.py) includes sample rules and test cases to demonstrate the following:
AST creation from individual rules.
Combining rules into a single AST.
Evaluating rules against sample user data.
Database storage of rules.
Run the file to execute the test cases:
bash
Copy code
python rule_engine.py
Expected output:
bash
Copy code
AST1: Node(type=operator, value=AND)
AST2: Node(type=operator, value=AND)
Combined AST: Node(type=operator, value=AND)
Evaluation result: True
Retrieved AST: {'type': 'operand', 'left': None, 'right': None, 'value': 'age > 30'}

Future Improvements
Error Handling: Implement error handling for invalid rule strings and data.
Rule Modification: Add functionality to modify existing rules dynamically.
Advanced Functions: Extend the system to support user-defined functions for more complex conditions.