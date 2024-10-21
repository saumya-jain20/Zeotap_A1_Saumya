import json
import sqlite3

# Node class for AST representation
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # 'operator' or 'operand'
        self.left = left  # Left child
        self.right = right  # Right child
        self.value = value  # Value for operand nodes

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value})"


# Simple tokenizer for parsing rule strings into components
def tokenize(rule_string):
    import re
    tokens = re.findall(r'\w+|[><=!&|()]+', rule_string)
    return tokens


# Function to create an AST from a rule string
def create_rule(rule_string):
    tokens = tokenize(rule_string)
    operators = []
    operands = []

    def apply_operator():
        op = operators.pop()
        right = operands.pop()
        left = operands.pop()
        operands.append(Node(node_type="operator", left=left, right=right, value=op))

    precedence = {'AND': 1, 'OR': 0}
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.isdigit():
            operands.append(Node(node_type="operand", value=int(token)))
        elif token.isalpha():
            if tokens[i+1] in ['>', '<', '>=', '<=', '==', '!=']:
                operator = tokens[i+1]
                operands.append(Node(node_type="operand", value=f"{token} {operator} {tokens[i+2]}"))
                i += 2
        elif token in ['AND', 'OR']:
            while operators and precedence[operators[-1]] >= precedence[token]:
                apply_operator()
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                apply_operator()
            operators.pop()  # Remove '('
        i += 1

    while operators:
        apply_operator()

    return operands[0]


# Function to combine multiple rules into a single AST
def combine_rules(rules):
    if not rules:
        return None

    ast_list = [create_rule(rule) for rule in rules]
    root = ast_list[0]

    for ast in ast_list[1:]:
        root = Node(node_type="operator", left=root, right=ast, value="AND")

    return root


# Evaluate the AST for given user data
def evaluate_rule(ast, data):
    if ast.type == "operand":
        condition = ast.value
        attr, operator, value = condition.split()
        value = int(value) if value.isdigit() else value
        return eval(f'data.get("{attr}") {operator} {value}')
    elif ast.type == "operator":
        left_val = evaluate_rule(ast.left, data)
        right_val = evaluate_rule(ast.right, data)
        if ast.value == "AND":
            return left_val and right_val
        elif ast.value == "OR":
            return left_val or right_val
    return False


# Example SQLite setup to store rules
def setup_db():
    conn = sqlite3.connect('rules.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rules
                 (id INTEGER PRIMARY KEY, rule_string TEXT, rule_ast TEXT)''')
    conn.commit()
    conn.close()


# Store rule in the database
def store_rule(rule_string, ast):
    conn = sqlite3.connect('rules.db')
    c = conn.cursor()
    c.execute('INSERT INTO rules (rule_string, rule_ast) VALUES (?, ?)', (rule_string, json.dumps(ast.__dict__)))
    conn.commit()
    conn.close()


# Retrieve and parse rule from the database
def retrieve_rule(rule_id):
    conn = sqlite3.connect('rules.db')
    c = conn.cursor()
    c.execute('SELECT rule_ast FROM rules WHERE id=?', (rule_id,))
    result = c.fetchone()
    conn.close()

    if result:
        return json.loads(result[0])
    return None


# Testing the functionality with sample rules
if __name__ == "__main__":
    # Setup the database (run only once)
    setup_db()

    # Define some rules
    rule1 = "((age > 30 AND department == 'Sales') OR (age < 25 AND department == 'Marketing')) AND (salary > 50000 OR experience > 5)"
    rule2 = "((age > 30 AND department == 'Marketing')) AND (salary > 20000 OR experience > 5)"

    # Create and store rules
    ast1 = create_rule(rule1)
    ast2 = create_rule(rule2)

    print("AST1:", ast1)
    print("AST2:", ast2)

    # Combine the rules
    combined_ast = combine_rules([rule1, rule2])
    print("Combined AST:", combined_ast)

    # Example user data
    data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}

    # Evaluate the combined rule
    result = evaluate_rule(combined_ast, data)
    print("Evaluation result:", result)

    # Store rule in the database
    store_rule(rule1, ast1)

    # Retrieve rule from the database
    retrieved_ast = retrieve_rule(1)
    print("Retrieved AST:", retrieved_ast)
