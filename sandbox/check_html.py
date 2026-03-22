import json
import re

# 读取HTML文件
with open('api/farming-almanac/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查是否有未闭合的引号或括号
# 检查单引号是否匹配
single_quotes = content.count("'")
if single_quotes % 2 != 0:
    print("警告: 单引号数量不匹配")

# 检查双引号是否匹配
double_quotes = content.count('"')
if double_quotes % 2 != 0:
    print("警告: 双引号数量不匹配")

# 检查括号是否匹配
parentheses_open = content.count('(')
parentheses_close = content.count(')')
if parentheses_open != parentheses_close:
    print(f"警告: 括号不匹配 - 开括号: {parentheses_open}, 闭括号: {parentheses_close}")

brackets_open = content.count('{')
brackets_close = content.count('}')
if brackets_open != brackets_close:
    print(f"警告: 大括号不匹配 - 开大括号: {brackets_open}, 闭大括号: {brackets_close}")

braces_open = content.count('[')
braces_close = content.count(']')
if braces_open != braces_close:
    print(f"警告: 中括号不匹配 - 开中括号: {braces_open}, 闭中括号: {braces_close}")

print("HTML文件检查完成")