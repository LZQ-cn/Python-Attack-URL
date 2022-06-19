""" 
main.py 为主函数
如果是第一次运行的话, 请先执行以下语句
"""

import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

creating = """CREATE TABLE names(name TEXT)"""
cursor.execute(creating)
conn.commit()

cursor.close()
conn.close()

"""
注: 这些语句的作用是创建一个数据库文件 (data.db), 并在其中创建一个数
    据表, 表名为 names, 其中包含名为 name 的用于储存字符串变量的字段名.
    
    这么做的目的很简单, 要被攻击的网站会自动识别用户名是否已经注册过, 如果
    是的话则无法注册, 因此每次生成用户名后都要储存, 以保证即使生成了生成过
    的用户名, 也可以检测到并且重新生成.
"""
