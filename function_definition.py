# --- Function Registry ---
FUNCTIONS = {
    "max": max,
    "min": min,
    "abs": lambda x: abs(x),
    "and": lambda a, b: bool(a) and bool(b),
    "or": lambda a, b: bool(a) or bool(b),
    "not": lambda a: not bool(a)
}

DATA_FRAME_FUNCTIONS = {
    "sum": lambda df, column, condition=None: df.query(condition)[column].sum() if condition else df[column].sum(),
    "count": lambda df, column, condition=None: df.query(condition)[column].count() if condition else df[column].count(),
    "countNotNull": lambda df, column, condition=None: df.query(condition)[column].notnull().sum() if condition else df[column].notnull().sum(),
    "rank": lambda df, column, condition=None: df.query(condition)[column].rank() if condition else df[column].rank()
}