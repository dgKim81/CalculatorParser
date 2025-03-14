# --- Context Class ---
class EvaluationContext:
    def __init__(self, dataframes=None, variables=None):
        self.dataframes = dataframes if dataframes else {}
        self.variables = variables if variables else {}
        self.cache = {}
        self.current_dataframe = None
        self.current_index = -1
    
    def get_dataframe(self,key):
        return self.dataframes.get(key, None)
    
    def select_dataframe(self, key):
        self.current_dataframe = self.dataframes.get(key, None)
        self.current_index = 0 if self.current_dataframe is not None else -1
    
    def next(self):
        if self.current_dataframe is None:
            return False
        self.current_index += 1
        if self.current_index >= len(self.current_dataframe):
            self.current_index = -1
            return False
        return True
    
    def get_variable(self, key):
        if self.current_dataframe is not None and self.current_index >= 0:
            if key in self.current_dataframe.columns:
                return self.current_dataframe.iloc[self.current_index][key]
        return self.variables.get(key, None)
    
    def set_variable(self, key, value):
        if self.current_dataframe is not None and self.current_index >= 0:
            self.current_dataframe.at[self.current_index, key] = value
        else:
            self.variables[key] = value
    
    def get_cache(self, key):
        return self.cache.get(key, None)
    
    def set_cache(self, key, value):
        self.cache[key] = value