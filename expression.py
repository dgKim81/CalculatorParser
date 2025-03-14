from abc import ABC, abstractmethod

class ExpressionParseException(Exception):
    def __init__(self, message):
        super().__init__(f"Expression Parse Error: {message}")

# --- AST Node Base Class ---
class Expr(ABC):
    @abstractmethod
    def evaluate(self, context):
        pass
    
    @abstractmethod
    def to_string(self):
        pass
    
    @abstractmethod
    def to_resolved_string(self, context):
        pass

# --- Concrete Expression Classes ---
class Value(Expr):
    def __init__(self, value):
        self.value = value
    
    def evaluate(self, context):
        return self.value
    
    def to_string(self):
        return str(self.value)
    
    def to_resolved_string(self, context):
        return str(self.value)
    
    def __repr__(self):
        return f"Value({self.value})"

class Variable(Expr):
    def __init__(self, name):
        self.name = name
    
    def evaluate(self, context):
        return context.get_variable(self.name)
    
    def to_string(self):
        return f"[{self.name}]"
    
    def to_resolved_string(self, context):
        return str(context.get_variable(self.name))
    
    def __repr__(self):
        return f"Variable({self.name})"

class BinaryOp(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    @abstractmethod
    def operate(self, left, right):
        pass
    
    def evaluate(self, context):
        left_val, right_val = self.left.evaluate(context), self.right.evaluate(context)
        return self.operate(left_val, right_val)
    
    def to_string(self):
        return f"({self.left.to_string()} {self.op_symbol()} {self.right.to_string()})"
    
    def to_resolved_string(self, context):
        return f"({self.left.to_resolved_string(context)} {self.op_symbol()} {self.right.to_resolved_string(context)})"
    
class Add(BinaryOp):
    def operate(self, left, right):
        if isinstance(left, str) or isinstance(right, str):
            return str(left) + str(right)
        return left + (1 if right is True else 0) if isinstance(right, bool) else left + right
    
    def op_symbol(self):
        return '+'
    
class Subtract(BinaryOp):
    def operate(self, left, right):
        if isinstance(left, str) or isinstance(right, str):
            raise ExpressionParseException("Cannot subtract string from a number")
        return left - (1 if right is True else 0) if isinstance(right, bool) else left - right
    
    def op_symbol(self):
        return '-'

class Multiply(BinaryOp):
    def operate(self, left, right):
        if isinstance(left, str) and isinstance(right, (int, float)):
            return left * int(right)
        if isinstance(right, str) and isinstance(left, (int, float)):
            return right * int(left)
        return left * right
    
    def op_symbol(self):
        return '*'

class Divide(BinaryOp):
    def operate(self, left, right):
        if isinstance(left, str) or isinstance(right, str):
            raise ExpressionParseException("Cannot divide a string by a number")
        return left / right
    
    def op_symbol(self):
        return '/'

# --- Unary Operations ---
class UnaryOp(Expr):
    def __init__(self, operand):
        self.operand = operand
    
    @abstractmethod
    def operate(self, operand):
        pass
    
    def evaluate(self, context):
        return self.operate(self.operand.evaluate(context))
    
    def to_string(self):
        return f"(-{self.operand.to_string()})"

    def to_resolved_string(self, context):
        return f"(-{self.operand.to_resolved_string(context)})"
    
class Negate(UnaryOp):
    def operate(self, operand):
        return -operand
    
class CompareOp(BinaryOp):
    def operate(self, left, right):
        return self.compare(left, right)
    
    @abstractmethod
    def compare(self, left, right):
        pass

class Equal(CompareOp):
    def compare(self, left, right):
        return left == right
    
    def op_symbol(self):
        return '='

class Greater(CompareOp):
    def compare(self, left, right):
        return left > right
    
    def op_symbol(self):
        return '>'

class Less(CompareOp):
    def compare(self, left, right):
        return left < right
    
    def op_symbol(self):
        return '<'
    
class GreaterEqual(CompareOp):
    def compare(self, left, right):
        return left >= right
    
    def op_symbol(self):
        return '>='
    
class LessEqual(CompareOp):
    def compare(self, left, right):
        return left >= right
    
    def op_symbol(self):
        return '<='