from function_definition import FUNCTIONS
from expression import Expr, ExpressionParseException

class FunctionCall(Expr):
    def __init__(self, name, args):
        self.name = name
        self.args = args
    
    def evaluate(self, context):
        if self.name not in FUNCTIONS:
            raise ExpressionParseException(f"Unknown function: {self.name}")
        arg_values = [arg.evaluate(context) for arg in self.args]
        return FUNCTIONS[self.name](*arg_values)
    
    def to_string(self):
        return f"{self.name}({', '.join(arg.to_string() for arg in self.args)})"
    
    def to_resolved_string(self, context):
        return f"{self.name}({', '.join(arg.to_resolved_string(context) for arg in self.args)})"
    
