import csv
import os

# 成绩建立
def store_score():
    score_dict = {
        '许耀尹':
        ['20190117022', '13980873867', '99', '99', '93', '92', '95', '89'],
        '张施淼':
        ['20190117016', '13550908081', '95', '96', '88', '92', '88', '90'],
        '王茜蕾':
        ['20190117012', '13652076886', '92', '86', '83', '88', '82', '91'],
        '姚馨雅':
        ['20190117014', '17568010701', '99', '96', '88', '92', '83', '87'],
        '吴梦双':
        ['20190117018', '13689605539', '97', '97', '66', '89', '91', '88'],
        '梅庭萱':
        ['20190117017', '13626108899', '92', '99', '74', '86', '88', '82'],
        '贾永林':
        ['20190117023', '18982156995', '93', '93', '82', '75', '87', '84'],
        '杨采悦':
        ['20190117020', '13880169698', '96', '90', '79', '95', '80', '80'],
        '刘未钦':
        ['20190117005', '13453429089', '94', '93', '65', '93', '85', '79'],
        '郑瑜竹':
        ['20190117019', '13881358209', '96', '97', '87', '68', '83', '89']
    }

    with open('ScoreManageSystem/score.csv', 'w') as f:
        w = csv.DictWriter(f, score_dict.keys())
        w.writeheader()
        w.writerow(score_dict)
    
    print('成绩信息建立完成\n')

# 一级菜单
def login_menu():
    
    # 提供注册、登录、推出三个选项
    print('Welcome to Yao\'s Score Management System')
    print('若您已有账号,请输入1登录')
    print('若您没有账号,请输入2注册')
    print('若您要退出系统,请输入3退出')
    
    # 获取用户选择 1 2 3中的哪个选项
    def get_choice():
        choice = input('请输入您要选择的操作:')
        if choice != '1' and choice != '2' and choice != '3':
            raise ValueError('Invalid input')
        
        return choice

    # 捕获异常
    try:
        choice = get_choice()
    except ValueError as e:
        print(e)
    else:
        if choice == '1': #登录
            login()
        elif choice == '2': #注册
            register()
        else: #退出
            exit()

# 注册用户
def register():
    username = input('请输入要使用的用户名:')
    passwd = input('请输入要使用的密码:')

    print('注册后,将会返回一级菜单')

    with open('ScoreManageSystem/user_info.txt','a') as f:
        f.write('{} {}\n'.format(username,passwd))
    
    print('注册成功！将跳转至一级菜单\n')
    login_menu()

# 退出系统
def exit():
    print('Bye')
    os._exit(0)

# 用户登录
def login():
    max_times = 3 #最大登录次数
    print('如果您在{}次之内没有成功登录,将会被强制退出系统'.format(max_times))

    loop_count = 0
    flag = 0 # 0表示登录失败 1表示成功
    while loop_count < 3:
        loop_count += 1
        # 获取用户输入的用户名和密码
        enter_name = input('请输入用户名:')
        enter_passwd = input('请输入密码:')

        # 遍历存储的用户信息
        with open('ScoreManageSystem/user_info.txt','r') as f:
            # 按行读取
            line = f.readlines()
            for elem in line:
                elem = elem.strip()
                actual_name,actual_passwd = elem.split() #将用户名和密码分割
                if actual_name == enter_name and actual_passwd == enter_passwd:
                    flag = 1
                    break
                else:
                    continue
        
        if flag == 0: #登录失败 重新尝试
            print('错误的用户名或密码,还有{}次登录机会\n'.format(max_times-loop_count))
        else: #登录成功 跳出循环
            break
        
    if flag == 0: # 超过N次登录次数 强制退出系统
        print('登陆失败,强制退出系统')
        exit()
    else:
        print('登录成功.欢迎{}.将跳转至二级菜单\n'.format(enter_name))
        user_menu() 

# 二级菜单
def user_menu():
    
    print('若您要查询个人成绩,请输入1')
    print('若您要统计个人成绩,请输入2')
    print('若您要统计总评成绩,请输入3')
    print('若您要退出系统,请输入4')

    # 获取用户选择 1 2 3 4中的哪个选项
    def get_choice():
        choice = input('请输入您要选择的操作:')
        if choice != '1' and choice != '2' and choice != '3' and choice != '4':
            raise ValueError('Invalid input')
        return choice

    # 捕获异常
    try:
        choice = get_choice()
    except ValueError as e:
        print(e)
    else:
        if choice == '1': #查询个人成绩
            sear_indi_score()
        elif choice == '2': #统计个人成绩
            calc_indi_score()
        elif choice == '3': #统计总评成绩
            calc_all_score()
        else: #退出系统
            exit()

# 查询个人成绩
def sear_indi_score():
    
    name = input('请输入要查询的学生姓名:')
    print('如果输入错误的学生姓名,将跳转至二级菜单\n')

    flag = 0 #如果能查询到置1 否则为0
    info_list = [] # 信息列表
    with open('ScoreManageSystem/score.csv','r') as f:
        w = csv.DictReader(f)
        order_dict = next(w)
        for key,val in order_dict.items():
            if key == name:
                flag = 1
                info_list = val
                break
    
    info_list = eval(info_list)
    if flag == 0: #查询失败
        print('输入学生姓名错误,查询失败,重新跳转至二级菜单\n')
    else: #查询成功
        print('学号:{}'.format(info_list[0]))
        print('电话:{}'.format(info_list[1]))
        print('大学计算机:{}'.format(info_list[2]))
        print('军事理论:{}'.format(info_list[3]))
        print('高等数学:{}'.format(info_list[4]))
        print('心理学导论:{}'.format(info_list[5]))
        print('民用航空概论:{}'.format(info_list[6]))
        print('大学体育:{}\n'.format(info_list[7]))
        print('查询成功,重新跳转至二级菜单\n')
    
    user_menu()

# 统计个人
def calc_indi_score():
    
    name = input('请输入要查询的学生姓名:')
    print('如果输入错误的学生姓名,将跳转至二级菜单\n')

    flag = 0 #如果能查询到置1 否则为0
    info_list = [] # 信息列表
    with open('ScoreManageSystem/score.csv','r') as f:
        w = csv.DictReader(f)
        order_dict = next(w)
        for key,val in order_dict.items():
            if key == name:
                flag = 1
                info_list = val
                break
    
    info_list = eval(info_list)
    
    if flag == 0: #查询失败
        print('输入学生姓名错误,查询失败,重新跳转至二级菜单\n')
    else: #查询成功
        score_list = info_list[2:] #获得成绩切片

        # 将字符串转换为int
        for i in range(len(score_list)):
            score_list[i] = int(score_list[i])

        total_score = sum(score_list) #总分
        mean_score = total_score / len(score_list) #平均分

        print('总分:{}'.format(total_score))
        print('平均分:{}\n'.format(mean_score))

        print('查询成功,重新跳转至二级菜单\n')
    
    user_menu()

# 统计所有同学
def calc_all_score():
    
    print('所有同学的总分按从高到低排名')

    score_dict = {}
    with open('ScoreManageSystem/score.csv','r') as f:
        w = csv.DictReader(f)
        order_dict = next(w)
        for key,val in order_dict.items():
            val = eval(val)
            # 将list中的每个元素转换为int
            for i in range(len(val)):
                val[i] = int(val[i])
            total_val = sum(val[2:])
            score_dict[key] = total_val
    
    # 按照字典的value排序 list中每个元素为一个tuple
    sorted_list = sorted(score_dict.items(),
                            key=lambda x: x[1],
                            reverse=True)
    
    for name,score in sorted_list:
        print('{}:{}'.format(name,score))
    
    print('\n查询成功,重新跳转至二级菜单\n')
    user_menu()


if __name__ == "__main__":
    store_score() #建立成绩信息
    login_menu() #登录
    