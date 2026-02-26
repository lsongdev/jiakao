import json
import re

input_file = "input.sql"
output_file = "output.json"

results = []

columns = [
    "s_id", "s_question", "s_img", "s_type", "s_km", "s_car",
    "item_a", "item_b", "item_c", "item_d",
    "answer", "s_explain",
    "chapter_id", "know_id",
    "add_time", "mod_time",
    "success_count", "error_count", "s_disable"
]

# 匹配 MySQL 单条 VALUES(...)
value_pattern = re.compile(
    r"'((?:\\'|[^'])*)'|NULL|(-?\d+)"
)

def parse_values(value_string):
    values = []
    for match in value_pattern.finditer(value_string):
        if match.group(1) is not None:
            # 字符串
            val = match.group(1).replace("\\'", "'")
            values.append(val)
        elif match.group(2) is not None:
            # 数字
            values.append(match.group(2))
        else:
            # NULL
            values.append(None)
    return values

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        if not line.startswith("INSERT INTO `subject` VALUES"):
            continue

        match = re.search(r"VALUES\s*\((.*)\);", line)
        if not match:
            continue

        values_str = match.group(1)
        values = parse_values(values_str)

        if len(values) != len(columns):
            print("字段数量不匹配，跳过")
            continue

        row = dict(zip(columns, values))

        subject = {
            "id": row["s_id"],
            "question": row["s_question"],
            "image": row["s_img"],

            "type": row["s_type"],
            "subject": row["s_km"],
            # "carType": row["s_car"],

            "chapterId": row["chapter_id"],
            "knowledgeId": row["know_id"],

            "options": {
                "A": row["item_a"],
                "B": row["item_b"],
                "C": row["item_c"],
                "D": row["item_d"],
            },

            "answer": row["answer"],
            "explain": row["s_explain"],

            "addTime": row["add_time"],
            "disabled": row["s_disable"] == "1"
        }

        results.append(subject)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"转换完成，共 {len(results)} 条记录")