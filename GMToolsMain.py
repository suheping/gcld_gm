import sys

import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import GMTools
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QDialog, QPushButton, QLabel


# 连接数据库gcld
def connectDB():
    global conn,ip,port,user,pwd,gs
    # 对话框布局
    vbox = QVBoxLayout()  # 纵向布局
    hbox = QHBoxLayout()  # 横向布局
    dialog = QDialog()
    okBtn = QPushButton("确定")
    panel = QLabel()
    # 获取按钮text
    text = ui.Button_connectDB.text()
    print(text)
    # 当前数据库未连接，连接数据库
    if text == '连接数据库':
        # 按钮显示为 连接数据库
        ui.Button_connectDB.setText('连接数据库')
        # 获取ip、端口、用户名、密码
        ip = ui.lineEdit.text()
        port_str = ui.lineEdit_2.text()
        user = ui.lineEdit_3.text()
        pwd = ui.lineEdit_4.text()
        try:  # port强转为int类型
            port = int(port_str)
        except Exception as e:
            panel.setText('端口只能是数字！！！')
            print(e)
        else:  # port强转成功
            # 判断是否有字段为空，为空则提示
            if ip == '' or port_str == '' or user == '' or pwd == '':
                panel.setText('请完整输入数据库连接信息！！！')
            # 不为空，连接数据库
            else:
                try:  # 尝试连接数据库
                    conn = pymysql.connect(
                        host=ip,
                        port=port,
                        user=user,
                        password=pwd,
                        database='gcld',
                        charset='utf8')
                except Exception as e:  # 连接数据库报错了
                    print(e)
                    conn = None
                else:   # 正常连接数据库
                    # 将按钮改为断开连接
                    ui.Button_connectDB.setText('断开连接')
                    panel.setText('数据库已连接！')
                    # 第一次连接数据库后，查询全部武将信息
                    # 查询所有武将信息
                    gs = generals()
    #  已经连接数据库，断开连接
    else:
        conn.close()
        # 将按钮改为连接数据库
        ui.Button_connectDB.setText('连接数据库')
        panel.setText('数据库连接已断开！')
        # 几个重要数据置为空
        # setup()
        # 清空所有页面输入框
        clearAll()

    # 显示对话框
    okBtn.clicked.connect(dialog.close)
    dialog.setWindowTitle("提示信息！")
    hbox.addWidget(okBtn)
    vbox.addWidget(panel)
    vbox.addLayout(hbox)
    dialog.setLayout(vbox)
    dialog.setWindowModality(Qt.ApplicationModal)  # 该模式下，只有该dialog关闭，才可以关闭父界面
    dialog.exec_()


# 获取玩家列表，并显示在下拉框中
def getPlayerList():
    global cursor
    try:
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select player_id, player_name from player;")
        res = cursor.fetchall()
    except Exception as e:
        print(e)
        res = None
    else:
        print('查询玩家列表正常')
        # 获取到玩家角色名列表，格式如下：
        # ['将军1', '将军2', '将军3', '将军4', '将军5', '将军6', '将军7', '将军8', '将军9', '玩游人生亲测', '玩游人生淘宝']
        player_name_list = []
        for i in res:
            player_name_list.append(i.get('player_name'))
        print(player_name_list)
        # 角色名下拉列表显示查询到的角色
        ui.comboBox.addItems(player_name_list)
        # 默认选择第0个角色
        ui.comboBox.setCurrentIndex(0)


# 获取玩家数据
def getPlayerData():
    # 拿到现在选择的是哪个玩家、玩家等级、金币数量
    playerName = ui.comboBox.currentText()
    print(playerName)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute('select player_id, player_lv, sys_gold  from player where player_name = %s',playerName)
    res_base = cursor.fetchall()
    print(res_base)
    # 取到玩家id、等级、金币数量
    playerId = res_base[0].get('player_id')
    playerLv = res_base[0].get('player_lv')
    sysGold = res_base[0].get('sys_gold')
    # 玩家等级、金币数量，写入界面
    ui.lineEdit_lv.setText(str(playerLv))
    ui.lineEdit_gold.setText(str(sysGold))

    # 查询资源信息
    cursor.execute('SELECT copper, wood, food, iron from player_resource where player_id = %s', playerId)
    res_resource = cursor.fetchall()
    print(res_resource)
    # 取到银币、木材、粮食、铁
    copper = res_resource[0].get('copper')
    wood = res_resource[0].get('wood')
    food = res_resource[0].get('food')
    iron = res_resource[0].get('iron')
    # 写入界面
    ui.lineEdit_copper.setText(str(copper))
    ui.lineEdit_wood.setText(str(wood))
    ui.lineEdit_food.setText(str(food))
    ui.lineEdit_iron.setText(str(iron))

    # 获取兵器等级，未开放的兵器将等级修改框置为不可编辑
    cursor.execute('SELECT lv from player_weapon where player_id = %s ORDER BY weapon_id;',playerId)
    res_weapon = cursor.fetchall()
    print(res_weapon)
    # 第几个兵器
    j = 1
    for i in res_weapon:
        if j == 1:
            w1_lv = i.get('lv')
            ui.lineEdit_w1.setText(str(w1_lv))
            ui.lineEdit_w1.setEnabled(True)
        elif j == 2:
            w2_lv = i.get('lv')
            ui.lineEdit_w2.setText(str(w2_lv))
            ui.lineEdit_w2.setEnabled(True)
        elif j == 3:
            w3_lv = i.get('lv')
            ui.lineEdit_w3.setText(str(w3_lv))
            ui.lineEdit_w3.setEnabled(True)
        elif j == 4:
            w4_lv = i.get('lv')
            ui.lineEdit_w4.setText(str(w4_lv))
            ui.lineEdit_w4.setEnabled(True)
        elif j == 5:
            w5_lv = i.get('lv')
            ui.lineEdit_w5.setText(str(w5_lv))
            ui.lineEdit_w5.setEnabled(True)
        elif j == 6:
            w6_lv = i.get('lv')
            ui.lineEdit_w6.setText(str(w6_lv))
            ui.lineEdit_w6.setEnabled(True)
        j = j+1
    # 如果当前j=1，意味着没有进for循环，也就是一个兵器也没有
    if j ==1:
        ui.lineEdit_w1.setText("")
        ui.lineEdit_w2.setText("")
        ui.lineEdit_w3.setText("")
        ui.lineEdit_w4.setText("")
        ui.lineEdit_w5.setText("")
        ui.lineEdit_w6.setText("")
        ui.lineEdit_w1.setEnabled(False)
        ui.lineEdit_w2.setEnabled(False)
        ui.lineEdit_w3.setEnabled(False)
        ui.lineEdit_w4.setEnabled(False)
        ui.lineEdit_w5.setEnabled(False)
        ui.lineEdit_w6.setEnabled(False)
    elif j ==2:
        ui.lineEdit_w2.setText("")
        ui.lineEdit_w3.setText("")
        ui.lineEdit_w4.setText("")
        ui.lineEdit_w5.setText("")
        ui.lineEdit_w6.setText("")
        ui.lineEdit_w2.setEnabled(False)
        ui.lineEdit_w3.setEnabled(False)
        ui.lineEdit_w4.setEnabled(False)
        ui.lineEdit_w5.setEnabled(False)
        ui.lineEdit_w6.setEnabled(False)
    elif j == 3:
        ui.lineEdit_w3.setText("")
        ui.lineEdit_w4.setText("")
        ui.lineEdit_w5.setText("")
        ui.lineEdit_w6.setText("")
        ui.lineEdit_w3.setEnabled(False)
        ui.lineEdit_w4.setEnabled(False)
        ui.lineEdit_w5.setEnabled(False)
        ui.lineEdit_w6.setEnabled(False)
    elif j == 4:
        ui.lineEdit_w4.setText("")
        ui.lineEdit_w5.setText("")
        ui.lineEdit_w6.setText("")
        ui.lineEdit_w4.setEnabled(False)
        ui.lineEdit_w5.setEnabled(False)
        ui.lineEdit_w6.setEnabled(False)
    elif j == 5:
        ui.lineEdit_w5.setText("")
        ui.lineEdit_w6.setText("")
        ui.lineEdit_w5.setEnabled(False)
        ui.lineEdit_w6.setEnabled(False)
    elif j == 6:
        ui.lineEdit_w6.setText("")
        ui.lineEdit_w6.setEnabled(False)

    # 获取玩家武将信息
    cursor.execute("SELECT general_id, '' as general_name, lv from player_general_military where player_id =%s ORDER BY lv;",playerId)
    res_general = cursor.fetchall()
    # 第几个武将游标
    x = 1
    print('res_general--------------------')
    print(res_general)
    print('gs------------------------')
    print(gs)

    for i in res_general: # 遍历查询结果
        for j in gs:   # 遍历所有武将列表
            if i.get('general_id') == j.get('id'):  # 如果找到了对应武将
                i.update(general_name = j.get('name'))  # 更新查询结果，写入武将名
                if x == 1:  # 当前是第一个武将
                    general_name = i.get('general_name')
                    general_lv = str(i.get('lv'))
                    ui.lineEdit_j1.setText(general_name)
                    ui.lineEdit_jl1.setText(general_lv)
                    ui.comboBox_tj1.addItems(tjs)
                    ui.lineEdit_jl1.setEnabled(True)
                    ui.comboBox_tj1.setEnabled(True)
                elif x == 2:
                    general_name = i.get('general_name')
                    general_lv = str(i.get('lv'))
                    ui.lineEdit_j2.setText(general_name)
                    ui.lineEdit_jl2.setText(general_lv)
                    ui.comboBox_tj2.addItems(tjs)
                    ui.lineEdit_jl2.setEnabled(True)
                    ui.comboBox_tj2.setEnabled(True)
                elif x == 3:
                    general_name = i.get('general_name')
                    general_lv = str(i.get('lv'))
                    ui.lineEdit_j3.setText(general_name)
                    ui.lineEdit_jl3.setText(general_lv)
                    ui.comboBox_tj3.addItems(tjs)
                    ui.lineEdit_jl3.setEnabled(True)
                    ui.comboBox_tj3.setEnabled(True)
                elif x == 4:
                    general_name = i.get('general_name')
                    general_lv = str(i.get('lv'))
                    ui.lineEdit_j4.setText(general_name)
                    ui.lineEdit_jl4.setText(general_lv)
                    ui.comboBox_tj4.addItems(tjs)
                    ui.lineEdit_jl4.setEnabled(True)
                    ui.comboBox_tj4.setEnabled(True)
                elif x == 5:
                    general_name = i.get('general_name')
                    general_lv = str(i.get('lv'))
                    ui.lineEdit_j5.setText(general_name)
                    ui.lineEdit_jl5.setText(general_lv)
                    ui.comboBox_tj5.addItems(tjs)
                    ui.lineEdit_jl5.setEnabled(True)
                    ui.comboBox_tj5.setEnabled(True)
                elif x == 6:
                    general_name = i.get('general_name')
                    general_lv = str(i.get('lv'))
                    ui.lineEdit_j6.setText(general_name)
                    ui.lineEdit_jl6.setText(general_lv)
                    ui.comboBox_tj6.addItems(tjs)
                    ui.lineEdit_jl6.setEnabled(True)
                    ui.comboBox_tj6.setEnabled(True)
                elif x == 7:
                    general_name = i.get('general_name')
                    general_lv = str(i.get('lv'))
                    ui.lineEdit_j7.setText(general_name)
                    ui.lineEdit_jl7.setText(general_lv)
                    ui.comboBox_tj7.addItems(tjs)
                    ui.lineEdit_jl7.setEnabled(True)
                    ui.comboBox_tj7.setEnabled(True)
                elif x == 8:
                    general_name = i.get('general_name')
                    general_lv = str(i.get('lv'))
                    ui.lineEdit_j8.setText(general_name)
                    ui.lineEdit_jl8.setText(general_lv)
                    ui.comboBox_tj8.addItems(tjs)
                    ui.lineEdit_jl8.setEnabled(True)
                    ui.comboBox_tj8.setEnabled(True)
                x = x+1
    # 如果当前x=1，那么就是没有进for循环，武将数量为0，将界面武将名、等级输入框清空、置灰
    if x == 1:
        # 武将名置空
        ui.lineEdit_j1.setText("")
        ui.lineEdit_j2.setText("")
        ui.lineEdit_j3.setText("")
        ui.lineEdit_j4.setText("")
        ui.lineEdit_j5.setText("")
        ui.lineEdit_j6.setText("")
        ui.lineEdit_j7.setText("")
        ui.lineEdit_j8.setText("")
        # 武将等级置空
        ui.lineEdit_jl1.setText("")
        ui.lineEdit_jl2.setText("")
        ui.lineEdit_jl3.setText("")
        ui.lineEdit_jl4.setText("")
        ui.lineEdit_jl5.setText("")
        ui.lineEdit_jl6.setText("")
        ui.lineEdit_jl7.setText("")
        ui.lineEdit_jl8.setText("")
        # 武将等级置灰
        ui.lineEdit_jl1.setEnabled(False)
        ui.lineEdit_jl2.setEnabled(False)
        ui.lineEdit_jl3.setEnabled(False)
        ui.lineEdit_jl4.setEnabled(False)
        ui.lineEdit_jl5.setEnabled(False)
        ui.lineEdit_jl6.setEnabled(False)
        ui.lineEdit_jl7.setEnabled(False)
        ui.lineEdit_jl8.setEnabled(False)
        # 目标武将下拉框置空
        ui.comboBox_tj1.clear()
        ui.comboBox_tj2.clear()
        ui.comboBox_tj3.clear()
        ui.comboBox_tj4.clear()
        ui.comboBox_tj5.clear()
        ui.comboBox_tj6.clear()
        ui.comboBox_tj7.clear()
        ui.comboBox_tj8.clear()
        # 目标武将下拉框置灰
        ui.comboBox_tj1.setEnabled(False)
        ui.comboBox_tj2.setEnabled(False)
        ui.comboBox_tj3.setEnabled(False)
        ui.comboBox_tj4.setEnabled(False)
        ui.comboBox_tj5.setEnabled(False)
        ui.comboBox_tj6.setEnabled(False)
        ui.comboBox_tj7.setEnabled(False)
        ui.comboBox_tj8.setEnabled(False)
    elif x == 2:
        # 武将名置空
        ui.lineEdit_j2.setText("")
        ui.lineEdit_j3.setText("")
        ui.lineEdit_j4.setText("")
        ui.lineEdit_j5.setText("")
        ui.lineEdit_j6.setText("")
        ui.lineEdit_j7.setText("")
        ui.lineEdit_j8.setText("")
        # 武将等级置空
        ui.lineEdit_jl2.setText("")
        ui.lineEdit_jl3.setText("")
        ui.lineEdit_jl4.setText("")
        ui.lineEdit_jl5.setText("")
        ui.lineEdit_jl6.setText("")
        ui.lineEdit_jl7.setText("")
        ui.lineEdit_jl8.setText("")
        # 武将等级置灰
        ui.lineEdit_jl2.setEnabled(False)
        ui.lineEdit_jl3.setEnabled(False)
        ui.lineEdit_jl4.setEnabled(False)
        ui.lineEdit_jl5.setEnabled(False)
        ui.lineEdit_jl6.setEnabled(False)
        ui.lineEdit_jl7.setEnabled(False)
        ui.lineEdit_jl8.setEnabled(False)
        # 目标武将下拉框置空
        ui.comboBox_tj2.clear()
        ui.comboBox_tj3.clear()
        ui.comboBox_tj4.clear()
        ui.comboBox_tj5.clear()
        ui.comboBox_tj6.clear()
        ui.comboBox_tj7.clear()
        ui.comboBox_tj8.clear()
        # 目标武将下拉框置灰
        ui.comboBox_tj2.setEnabled(False)
        ui.comboBox_tj3.setEnabled(False)
        ui.comboBox_tj4.setEnabled(False)
        ui.comboBox_tj5.setEnabled(False)
        ui.comboBox_tj6.setEnabled(False)
        ui.comboBox_tj7.setEnabled(False)
        ui.comboBox_tj8.setEnabled(False)
    elif x == 3:
        # 武将名置空
        ui.lineEdit_j3.setText("")
        ui.lineEdit_j4.setText("")
        ui.lineEdit_j5.setText("")
        ui.lineEdit_j6.setText("")
        ui.lineEdit_j7.setText("")
        ui.lineEdit_j8.setText("")
        # 武将等级置空
        ui.lineEdit_jl3.setText("")
        ui.lineEdit_jl4.setText("")
        ui.lineEdit_jl5.setText("")
        ui.lineEdit_jl6.setText("")
        ui.lineEdit_jl7.setText("")
        ui.lineEdit_jl8.setText("")
        # 武将等级置灰
        ui.lineEdit_jl3.setEnabled(False)
        ui.lineEdit_jl4.setEnabled(False)
        ui.lineEdit_jl5.setEnabled(False)
        ui.lineEdit_jl6.setEnabled(False)
        ui.lineEdit_jl7.setEnabled(False)
        ui.lineEdit_jl8.setEnabled(False)
        # 目标武将下拉框置空
        ui.comboBox_tj3.clear()
        ui.comboBox_tj4.clear()
        ui.comboBox_tj5.clear()
        ui.comboBox_tj6.clear()
        ui.comboBox_tj7.clear()
        ui.comboBox_tj8.clear()
        # 目标武将下拉框置灰
        ui.comboBox_tj3.setEnabled(False)
        ui.comboBox_tj4.setEnabled(False)
        ui.comboBox_tj5.setEnabled(False)
        ui.comboBox_tj6.setEnabled(False)
        ui.comboBox_tj7.setEnabled(False)
        ui.comboBox_tj8.setEnabled(False)
    elif x == 4:
        # 武将名置空
        ui.lineEdit_j4.setText("")
        ui.lineEdit_j5.setText("")
        ui.lineEdit_j6.setText("")
        ui.lineEdit_j7.setText("")
        ui.lineEdit_j8.setText("")
        # 武将等级置空
        ui.lineEdit_jl4.setText("")
        ui.lineEdit_jl5.setText("")
        ui.lineEdit_jl6.setText("")
        ui.lineEdit_jl7.setText("")
        ui.lineEdit_jl8.setText("")
        # 武将等级置灰
        ui.lineEdit_jl4.setEnabled(False)
        ui.lineEdit_jl5.setEnabled(False)
        ui.lineEdit_jl6.setEnabled(False)
        ui.lineEdit_jl7.setEnabled(False)
        ui.lineEdit_jl8.setEnabled(False)
        # 目标武将下拉框置空
        ui.comboBox_tj4.clear()
        ui.comboBox_tj5.clear()
        ui.comboBox_tj6.clear()
        ui.comboBox_tj7.clear()
        ui.comboBox_tj8.clear()
        # 目标武将下拉框置灰
        ui.comboBox_tj4.setEnabled(False)
        ui.comboBox_tj5.setEnabled(False)
        ui.comboBox_tj6.setEnabled(False)
        ui.comboBox_tj7.setEnabled(False)
        ui.comboBox_tj8.setEnabled(False)
    elif x == 5:
        # 武将名置空
        ui.lineEdit_j5.setText("")
        ui.lineEdit_j6.setText("")
        ui.lineEdit_j7.setText("")
        ui.lineEdit_j8.setText("")
        # 武将等级置空
        ui.lineEdit_jl5.setText("")
        ui.lineEdit_jl6.setText("")
        ui.lineEdit_jl7.setText("")
        ui.lineEdit_jl8.setText("")
        # 武将等级置灰
        ui.lineEdit_jl5.setEnabled(False)
        ui.lineEdit_jl6.setEnabled(False)
        ui.lineEdit_jl7.setEnabled(False)
        ui.lineEdit_jl8.setEnabled(False)
        # 目标武将下拉框置空
        ui.comboBox_tj5.clear()
        ui.comboBox_tj6.clear()
        ui.comboBox_tj7.clear()
        ui.comboBox_tj8.clear()
        # 目标武将下拉框置灰
        ui.comboBox_tj5.setEnabled(False)
        ui.comboBox_tj6.setEnabled(False)
        ui.comboBox_tj7.setEnabled(False)
        ui.comboBox_tj8.setEnabled(False)
    elif x == 6:
        # 武将名置空
        ui.lineEdit_j6.setText("")
        ui.lineEdit_j7.setText("")
        ui.lineEdit_j8.setText("")
        # 武将等级置空
        ui.lineEdit_jl6.setText("")
        ui.lineEdit_jl7.setText("")
        ui.lineEdit_jl8.setText("")
        # 武将等级置灰
        ui.lineEdit_jl6.setEnabled(False)
        ui.lineEdit_jl7.setEnabled(False)
        ui.lineEdit_jl8.setEnabled(False)
        # 目标武将下拉框置空
        ui.comboBox_tj6.clear()
        ui.comboBox_tj7.clear()
        ui.comboBox_tj8.clear()
        # 目标武将下拉框置灰
        ui.comboBox_tj6.setEnabled(False)
        ui.comboBox_tj7.setEnabled(False)
        ui.comboBox_tj8.setEnabled(False)
    elif x == 7:
        # 武将名置空
        ui.lineEdit_j7.setText("")
        ui.lineEdit_j8.setText("")
        # 武将等级置空
        ui.lineEdit_jl7.setText("")
        ui.lineEdit_jl8.setText("")
        # 武将等级置灰
        ui.lineEdit_jl7.setEnabled(False)
        ui.lineEdit_jl8.setEnabled(False)
        # 目标武将下拉框置空
        ui.comboBox_tj7.clear()
        ui.comboBox_tj8.clear()
        # 目标武将下拉框置灰
        ui.comboBox_tj7.setEnabled(False)
        ui.comboBox_tj8.setEnabled(False)
    elif x == 8:
        # 武将名置空
        ui.lineEdit_j8.setText("")
        # 武将等级置空
        ui.lineEdit_jl8.setText("")
        # 武将等级置灰
        ui.lineEdit_jl8.setEnabled(False)
        # 目标武将下拉框置空
        ui.comboBox_tj8.clear()
        # 目标武将下拉框置灰
        ui.comboBox_tj8.setEnabled(False)

    print(res_general)


# 取到所有的武将，添加到gs中
def generals():
    conn1 = pymysql.connect(
        host=ip,
        port=port,
        user=user,
        password=pwd,
        database='gcld_sdata',
        charset='utf8')
    cursor1 = conn1.cursor(cursor=pymysql.cursors.DictCursor)
    cursor1.execute('SELECT id ,name from general;')
    res_grenerals = cursor1.fetchall()
    gs = general_list + res_grenerals
    return gs


# 断开数据库连接后，清空所有数据
def clearAll():
    # 玩家列表
    ui.comboBox.clear()
    # 基础信息
    ui.lineEdit_lv.clear()
    ui.lineEdit_gold.clear()
    ui.lineEdit_copper.clear()
    ui.lineEdit_wood.clear()
    ui.lineEdit_food.clear()
    ui.lineEdit_iron.clear()
    # 兵器等级
    ui.lineEdit_w1.clear()
    ui.lineEdit_w2.clear()
    ui.lineEdit_w3.clear()
    ui.lineEdit_w4.clear()
    ui.lineEdit_w5.clear()
    ui.lineEdit_w6.clear()
    # 武将
    ui.lineEdit_j1.clear()
    ui.lineEdit_j2.clear()
    ui.lineEdit_j3.clear()
    ui.lineEdit_j4.clear()
    ui.lineEdit_j5.clear()
    ui.lineEdit_j6.clear()
    ui.lineEdit_j7.clear()
    ui.lineEdit_j8.clear()
    # 武将等级
    ui.lineEdit_jl1.clear()
    ui.lineEdit_jl2.clear()
    ui.lineEdit_jl3.clear()
    ui.lineEdit_jl4.clear()
    ui.lineEdit_jl5.clear()
    ui.lineEdit_jl6.clear()
    ui.lineEdit_jl7.clear()
    ui.lineEdit_jl8.clear()
    # 神将下拉框
    ui.comboBox_tj1.clear()
    ui.comboBox_tj2.clear()
    ui.comboBox_tj3.clear()
    ui.comboBox_tj4.clear()
    ui.comboBox_tj5.clear()
    ui.comboBox_tj6.clear()
    ui.comboBox_tj7.clear()
    ui.comboBox_tj8.clear()


# 初始化数据
def setup():
    global general_list, tjs, gs, player_name_list, res_base, res_resource, res_weapon, res_general
    # 初始化数据
    # 神将、魔将列表
    general_list = []
    general_list.append({'id': 269, 'name': '神·陈宫'})
    general_list.append({'id': 270, 'name': '神·郭嘉'})
    general_list.append({'id': 271, 'name': '神·陆逊'})
    general_list.append({'id': 272, 'name': '神·周瑜'})
    general_list.append({'id': 273, 'name': '神·吕布'})
    general_list.append({'id': 274, 'name': '魔·赵云'})
    general_list.append({'id': 275, 'name': '魔·诸葛'})
    general_list.append({'id': 276, 'name': '魔·孙权'})
    general_list.append({'id': 277, 'name': '魔·曹操'})
    general_list.append({'id': 278, 'name': '魔·刘备'})
    print(general_list)
    # 魔将、神将 名称列表
    tjs = []
    for i in general_list:
        tjs.append(i.get('name'))
    print(tjs)
    # # 全部武将信息
    gs = []
    # 玩家列表
    player_name_list = []
    # 玩家基本信息
    res_base = []
    # 玩家资源信息
    res_resource = []
    # 玩家兵器信息
    res_weapon = []
    # 玩家武将信息
    res_general = []


# 修改基础信息
def modify_base():
    # 如果已经连接数据库
    if ui.Button_connectDB.text() == '断开连接':
        cursor.execute('')
    else:
        print('请先连接数据库，再修改基础数据！')


# 修改兵器等级
def modify_weapon():
    # 如果已经连接数据库
    if ui.Button_connectDB.text() == '断开连接':
        cursor.execute('')
    else:
        print('请先连接数据库，再修改兵器等级！')


# 修改武将信息
def modify_general():
    # 如果已经连接数据库
    if ui.Button_connectDB.text() == '断开连接':
        cursor.execute('')
    else:
        print('请先连接数据库，再修改武将信息！')


# 送一套真屠龙
def send_tulong():
    # 如果已经连接数据库
    if ui.Button_connectDB.text() == '断开连接':
        cursor.execute('')
    else:
        print('请先连接数据库，再赠送真屠龙！')


# 送一个顶级晶石
def send_jingshi():
    # 如果已经连接数据库
    if ui.Button_connectDB.text() == '断开连接':
        cursor.execute('')
    else:
        print('请先连接数据库，再赠送顶级晶石！')


def click_success():
    print("啊哈哈哈我终于成功了！")



if __name__ == '__main__':
    # 初始化数据
    setup()
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = GMTools.Ui_mainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # 事件监听
    # 监听连接数据库按钮
    ui.Button_connectDB.clicked.connect(connectDB)
    # 监听获取玩家列表按钮
    ui.Button_getPlayerList.clicked.connect(getPlayerList)
    # 监听选定玩家按钮
    ui.Button_selectPlayer.clicked.connect(getPlayerData)
    # 监听修改基础信息按钮
    ui.Button_modify_Base.clicked.connect(modify_base)
    # 监听修改兵器信息按钮
    ui.Button_modify_weapon.clicked.connect(modify_weapon)
    # 监听修改武将信息按钮
    ui.Button_modify_general.clicked.connect(modify_general)
    # 监听赠送真屠龙按钮
    ui.Button_tulong.clicked.connect(send_tulong)
    # 监听赠送顶级晶石按钮
    ui.Button_jingshi.clicked.connect(send_jingshi)

    sys.exit(app.exec_())