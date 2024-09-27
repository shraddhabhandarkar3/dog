import pyodbc
import json
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 从 .env 文件中读取 SQL Server 配置信息
server = os.getenv('SQL_SERVER')  # SQL Server 地址
database = os.getenv('SQL_DATABASE')  # 数据库名称
username = os.getenv('SQL_USER')  # 用户名
password = os.getenv('SQL_PASSWORD')  # 密码
driver = '{ODBC Driver 17 for SQL Server}'  # SQL Server ODBC 驱动

# 建立 SQL Server 连接
connection = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};')
cursor = connection.cursor()

# 读取 JSON 文件
with open('metadata.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 插入数据到 SQL Server
for record in data:
    task_id = record.get('task_id', '')
    question = record.get('Question', '')
    level = record.get('Level', 0)
    file_name = record.get('file_name', '')
    final_answer = record.get('Final answer', '')
    metadata = record.get('Annotator Metadata', {})
    
    steps = metadata.get('Steps', '')
    number_of_steps = metadata.get('Number of steps', '')
    how_long = metadata.get('How long did this take?', '')
    tools = metadata.get('Tools', '')
    number_of_tools = metadata.get('Number of tools', '')

    # 执行 SQL 插入命令
    cursor.execute('''
        INSERT INTO Tasks (Question, Level, file_name, Final_answer, Steps, Number_of_steps, How_long_did_this_take, Tools, Number_of_tools)
        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (question, level, file_name, final_answer, steps, number_of_steps, how_long, tools, number_of_tools))

# 提交事务
connection.commit()

# 关闭连接
cursor.close()
connection.close()