from function_definition import DATA_FRAME_FUNCTIONS
from expression import Expr, ExpressionParseException
import pandas as pd

# --- Special DataFrame Function Handling ---
class DataFrameFunctionCall(Expr):
    def __init__(self, name, args):
        self.name = name
        self.args = args
    
    def evaluate(self, context):
        if self.name not in DATA_FRAME_FUNCTIONS:
            raise ExpressionParseException(f"Unknown function: {self.name}")
        
        df_key = self.args[0].evaluate(context)
        df = context.get_dataframe(df_key)
        if df is None or not isinstance(df, pd.DataFrame):
            raise ExpressionParseException(f"Invalid DataFrame reference: {df_key}")
        
        column = self.args[1].evaluate(context)
        condition = self.args[2].evaluate(context) if len(self.args) > 2 else None
        
        # 캐싱 키 생성
        cache_key = f"{self.name}:{df_key}:{column}:{condition}"
        cached_result = context.get_cache(cache_key)
        if cached_result is not None:
            return cached_result
        
        result = DATA_FRAME_FUNCTIONS[self.name](df, column, condition)
        context.set_cache(cache_key, result)
        return result
    
    def to_string(self):
        return f"{self.name}({', '.join(arg.to_string() for arg in self.args)})"
    
    def to_resolved_string(self, context):
        return f"{self.name}({', '.join(arg.to_resolved_string(context) for arg in self.args)})"