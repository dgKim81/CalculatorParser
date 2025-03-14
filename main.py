import pandas as pd
from parser import CalculatorParser
from evaluation_context import EvaluationContext
import time
# 테스트 데이터 생성
data = pd.DataFrame({
    "A": [10, 20, 30],
    "B": [100, 200, 300],
    "C": [5, 15, 25]
})

# 컨텍스트 생성 및 DataFrame 선택
context = EvaluationContext(dataframes={"df": data})
parser = CalculatorParser()

# 테스트할 수식들
test_expressions = [
    "[A] + [B]",  # 기본 덧셈
    "[A] * 2 + [C]",  # 연산 조합
    "sum(\"df\", \"A\")",  # 전체 컬럼 합
    "count(\"df\", \"A\")",  # 개수 계산
    "max([A], [B])",  # 최대값 비교
    "and([A] > 15,[B] < 300)",  # 논리 연산
    "sum(\"df\", \"C\", \"A > 15\")",  # 조건을 포함한 sum()
]

# 실행 및 결과 출력
for expr in test_expressions:
    parser.read_expression(expr)
    print(f"Expression: {expr}")

    # DataFrame의 각 행을 순회하며 평가
    context.select_dataframe("df")
    while context.next():
        result = parser.calculate(context)
        print(f"  Row {context.current_index} -> Result: {result}")

    print("-" * 50)  # 구분선 출력

# 테스트
# expr = "max([A] + 5, [B] * ([C] - 3))"
# parser = CalculatorParser()
# parser.read_expression(expr)

# data = pd.DataFrame({"A": [3], "B": [2], "C": [8]})
# context = data
# result = parser.calculate(context)

# print(f"{expr} = {result}")
# print("Original Expression:", parser.to_string())
# print("Resolved Expression:", parser.to_resolved_string(context))

# expr = 'and([A] > 5,[B] <= 10)'
# parser = CalculatorParser()
# parser.read_expression(expr)

# data = pd.DataFrame({"A": [6], "B": [10]})
# context = { data: data.iloc[0].to_dict() }
# result = parser.calculate(context)

# print(f"{expr} = {result}")
# print("Original Expression:", parser.to_string())
# print("Resolved Expression:", parser.to_resolved_string(context))


# test_cases = [
#     ('"Test" + " String"', { "data": {}}, "Test String"),
#     ('max([X] + 3 * [Y], 10)', { "data": {"X": 2, "Y": 4}}, 14),
#     ('and([X] > 5,[Y] <= 10)', { "data": {"X": 6, "Y": 10}}, True),
#     ('max([A], [B])',  { "data": {"A": 5, "B": 7}}, 7),
#     ('"Hello"" World"', {}, 'Hello" World'),
#     ('min("abc", "def")', {}, "abc")
# ]

# for expr, context, expected in test_cases:
#     parser.read_expression(expr)
#     result = parser.calculate(context)
#     assert result == expected, f"Test failed: {expr} (Expected: {expected}, Got: {result})"
#     print(f"✅ {expr} = {result}")



# # 테스트할 수식 (복잡한 수식으로 테스트)
# expr = 'max([A] + 5 * [B], min([C] - 3, [D] / 2))'
# parser = CalculatorParser()

# # 대량의 데이터 생성
# num_rows = 1000000
# data = pd.DataFrame({
#     "A": [i % 10 for i in range(num_rows)],
#     "B": [(i % 5) + 1 for i in range(num_rows)],
#     "C": [i % 20 for i in range(num_rows)],
#     "D": [(i % 7) + 2 for i in range(num_rows)],
# })

# # 성능 테스트 1: 대량의 수식 파싱 속도 측정
# start_time = time.time()
# for _ in range(10000):  # 10,000번 수식 파싱
#     parser.read_expression(expr)
# parse_time = time.time() - start_time
# print(f"✅ 10,000 수식 파싱 시간: {parse_time:.4f}초")

# # 성능 테스트 2: 데이터 100,000개에 대해 수식 실행
# start_time = time.time()
# for i in range(num_rows):
#     context = data.iloc[i].to_dict()
#     result = parser.calculate(context)
# execution_time = time.time() - start_time
# print(f"✅ {num_rows} 수식 실행 시간: {execution_time:.4f}초")
