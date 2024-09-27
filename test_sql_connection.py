import pyodbc

# 测试连接
server = 'localhost,1433'
database = 'TestDB'
username = 'sa'
password = 'qwerty123456!'
driver = '{ODBC Driver 17 for SQL Server}'

try:
    connection = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};'
    )
    print("Connection successful!")
    
    # 测试查询
    cursor = connection.cursor()
    cursor.execute("SELECT TOP 1 * FROM JsonData")  # 确保表名正确
    row = cursor.fetchone()
    print(row)

    cursor.close()
    connection.close()

except pyodbc.Error as e:
    print(f"Error: {e}")