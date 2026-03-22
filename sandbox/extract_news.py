import os
import re
import json

html_path = r"d:\HuaweiMoveData\Users\32874\Desktop\CleverFarming\frontend\agricultural-news\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'const newsData = \[\s*(.*?)\s*\];'
match = re.search(pattern, content, re.DOTALL)
if not match:
    print("Could not find newsData block")
    exit(1)
news_data_section = match.group(1)

# To tolerate missing image field:
item_pattern = r'\{\s*id:\s*(\d+),\s*title:\s*\'([^\']*)\',\s*category:\s*\'([^\']*)\',\s*summary:\s*\'([^\']*)\',\s*content:\s*`(.*?)`,\s*(?:image:\s*\'([^\']*)\',\s*)?author:\s*\'([^\']*)\',\s*time:\s*\'([^\']*)\',\s*views:\s*(\d+)\s*\}'

items = []
matches = re.finditer(item_pattern, news_data_section, re.DOTALL)
for m in matches:
    items.append({
        'id': int(m.group(1)),
        'title': m.group(2),
        'category': m.group(3),
        'summary': m.group(4),
        'content': m.group(5).strip(),
        'image': m.group(6) if m.group(6) else "",
        'author': m.group(7),
        'time': m.group(8),
        'views': int(m.group(9))
    })

os.makedirs(r"d:\HuaweiMoveData\Users\32874\Desktop\CleverFarming\backend\data", exist_ok=True)
with open(r"d:\HuaweiMoveData\Users\32874\Desktop\CleverFarming\backend\data\news.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(items)} items to news.json")
