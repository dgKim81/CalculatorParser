import re
from expression import *
from expression_function import *
from data_frame_function import DataFrameFunctionCall
from function_definition import *
# --- Parser ---
class CalculatorParser:
    def __init__(self):
        pass

    def read_expression(self, expression):
        #self.tokens = re.findall(r'\"(?:[^\"]|\"\")*\"|\d+\.\d*|[()+\-*/=<>]|\w+|\[.*?\]|,', expression.replace(' ', ''))
        expression = self.preprocess_expression(expression)
        self.tokens = re.findall(r'"(?:[^"]|"")*"|\d+\.\d*|<=|>=|[()+\-*/=<>]|\w+|\[.*?\]|,', expression)
        self.ast = None
        self.parse()
    
    def preprocess_expression(self, expression):
        """Preserves spaces inside quoted strings while removing others."""
        tokens = re.split(r'(\"(?:[^\"]|\"\")*\"|\S+)', expression)
        return ''.join(t if t.startswith('"') and t.endswith('"') else t.replace(' ', '') for t in tokens if t)
    
    def parse(self):
        if self.ast == None:
            self.current = 0
            self.ast = self.parse_expression()
            
        return self.ast 
    
    def peek(self):
        return self.tokens[self.current] if self.current < len(self.tokens) else None

    def consume(self):
        token = self.peek()
        self.current += 1
        return token

    def parse_expression(self):
        node = self.parse_comparison()
        return node

    def parse_comparison(self):
        node = self.parse_term_pm()
        while self.peek() in ('=', '<', '>', '<=', '>='):
            op = self.consume()
            right = self.parse_term_pm()
            if op == '=':
                node = Equal(node, right)
            elif op == '>':
                node = Greater(node, right)
            elif op == '<':
                node = Less(node, right)
            elif op == '>=':
                node = GreaterEqual(node, right)
            elif op == '<=':
                node = LessEqual(node, right)
        return node
    
    def parse_term_pm(self):
        node = self.parse_term_md()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.parse_term_md()
            node = Add(node, right) if op == '+' else Subtract(node, right)
        return node
    
    def parse_term_md(self):
        node = self.parse_factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            right = self.parse_factor()
            node = Multiply(node, right) if op == '*' else Divide(node, right)
        return node

    def parse_factor(self):
        token = self.consume()
        if token.isdigit() or '.' in token:
            return Value(float(token))
        elif re.match(r'\[.*?\]', token):  # Variable with brackets
            return Variable(token.strip('[]'))
        elif re.match(r'[a-zA-Z_]+', token):  # Function call
            self.consume()  # Consume '('
            args = []
            while self.peek() != ')':
                args.append(self.parse_expression())
                if self.peek() == ',':
                    self.consume()
            self.consume()  # Consume ')'
            return DataFrameFunctionCall(token, args) if token in DATA_FRAME_FUNCTIONS else FunctionCall(token, args)
        elif token.startswith('"') and token.endswith('"'):
            return Value(token[1:-1].replace("\"\"", "\""))
        elif token == '(':
            node = self.parse_expression()
            self.consume()  # Consume ')'
            return node
        elif token == '-':
            return Negate(self.parse_factor())
        raise ExpressionParseException("Invalid syntax")

    def calculate(self, context):
        return self.ast.evaluate(context)

    def to_string(self):
        return self.ast.to_string()
    
    def to_resolved_string(self, context):
        return self.ast.to_resolved_string(context)