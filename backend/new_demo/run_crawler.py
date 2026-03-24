import sys
import os

# 添加 packages 目录到路径
packages_path = os.path.join(os.path.dirname(__file__), '..', 'packages')
sys.path.insert(0, packages_path)

# 导入并运行爬虫
from agri_mysql_crawler import run_pipeline

if __name__ == "__main__":
    run_pipeline()