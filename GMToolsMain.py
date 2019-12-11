# coding=utf-8

import sys

import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import GMTools
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QDialog, QPushButton, QLabel


# 连接数据库gcld
def connectDB():
    global conn,ip,port,user,pwd
    # 获取按钮text
    text = ui.Button_connectDB.text()
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
            QMessageBox.warning(MainWindow, '提示信息', '端口只能是数字！！！', QMessageBox.Ok)
            print(e)
        else:  # port强转成功
            # 判断是否有字段为空，为空则提示
            if ip == '' or port_str == '' or user == '' or pwd == '':
                QMessageBox.warning(MainWindow, '提示信息', '请输入完整的数据库连接信息！！！', QMessageBox.Ok)
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
                    QMessageBox.critical(MainWindow, '提示信息', '数据库连接报错了！！！', QMessageBox.Ok)
                    print(e)
                    conn = None
                else:   # 正常连接数据库
                    # 将按钮改为断开连接
                    ui.Button_connectDB.setText('断开连接')
                    QMessageBox.information(MainWindow, '提示信息', '数据库连接成功！！！', QMessageBox.Ok)
                    print('--------------------------数据库已连接--------------------------------------')
    #  已经连接数据库，断开连接
    else:
        conn.close()
        # 将按钮改为连接数据库
        ui.Button_connectDB.setText('连接数据库')
        QMessageBox.information(MainWindow, '提示信息', '数据库连接已断开！！！', QMessageBox.Ok)
        print('-----------------------------------数据库连接已断开-------------------------------------')
        # 几个重要数据置为空
        # setup()
        # 清空所有页面输入框
        clearAll()


# 获取玩家列表，并显示在下拉框中
def getPlayerList():
    global cursor
    if ui.Button_connectDB.text() == '断开连接':
        try:
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute("select player_id, player_name from player;")
            res = cursor.fetchall()
        except Exception as e:
            print(e)
            res = None
        else:
            # 获取到玩家角色名列表，格式如下：
            # ['将军1', '将军2', '将军3', '将军4', '将军5', '将军6', '将军7', '将军8', '将军9', '玩游人生亲测', '玩游人生淘宝']
            player_name_list = []
            for i in res:
                player_name_list.append(i.get('player_name'))
            print('-----------------已获取到玩家列表--------------------------')
            print(player_name_list)
            # 角色名下拉列表显示查询到的角色
            ui.comboBox.addItems(player_name_list)
            # 默认选择第0个角色
            ui.comboBox.setCurrentIndex(0)
    else:
        QMessageBox.warning(MainWindow, '提示信息', '请先连接数据库！！！', QMessageBox.Ok)


# 获取玩家数据
def getPlayerData():
    global playerId
    if ui.Button_connectDB.text() == '断开连接':
        # 拿到现在选择的是哪个玩家、玩家等级、金币数量
        playerName = ui.comboBox.currentText()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute('select player_id, player_lv, sys_gold  from player where player_name = %s',playerName)
        res_base = cursor.fetchall()
        # 取到玩家id、等级、金币数量
        playerId = res_base[0].get('player_id')
        playerLv = res_base[0].get('player_lv')
        sysGold = res_base[0].get('sys_gold')
        # 玩家等级、金币数量，写入界面
        ui.lineEdit_lv.setText(str(playerLv))
        ui.lineEdit_gold.setText(str(sysGold))
        print('-------当前选择玩家为: ',playerName,' ----等级为: ',playerLv,'------金币数量为:',sysGold)

        # 查询资源信息
        cursor.execute('SELECT copper, wood, food, iron from player_resource where player_id = %s', playerId)
        res_resource = cursor.fetchall()
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
        print('------------',playerName,' 银币：',copper,' 木材：',wood,' 粮食：',food,' 铁：',iron)
        # 获取兵器等级，未开放的兵器将等级修改框置为不可编辑
        cursor.execute('SELECT lv from player_weapon where player_id = %s ORDER BY weapon_id;',playerId)
        res_weapon = cursor.fetchall()
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

        print('------- ',playerName,' 有如下武将 ----------------------------------')
        print(res_general)
    else:
        QMessageBox.warning(MainWindow, '提示信息', '请先连接数据库！！！', QMessageBox.Ok)


# 断开数据库连接后，清理所有输入框中的数据
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
    general_list.append({'id': 0,'name': '不变'})
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
    # 魔将、神将 名称列表
    tjs = []
    for i in general_list:
        tjs.append(i.get('name'))
    # # 全部武将信息
    gs = [{'id': 0, 'name': '不变'}, {'id': 269, 'name': '神·陈宫'}, {'id': 270, 'name': '神·郭嘉'}, {'id': 271, 'name': '神·陆逊'}, {'id': 272, 'name': '神·周瑜'}, {'id': 273, 'name': '神·吕布'}, {'id': 274, 'name': '魔·赵云'}, {'id': 275, 'name': '魔·诸葛'}, {'id': 276, 'name': '魔·孙权'}, {'id': 277, 'name': '魔·曹操'}, {'id': 278, 'name': '魔·刘备'}, {'id': 110, 'name': '陆逊'}, {'id': 201, 'name': '吕布'}, {'id': 202, 'name': '张飞'}, {'id': 203, 'name': '关羽'}, {'id': 204, 'name': '赵云'}, {'id': 205, 'name': '马超'}, {'id': 206, 'name': '太史慈'}, {'id': 207, 'name': '许褚'}, {'id': 208, 'name': '典韦'}, {'id': 209, 'name': '张辽'}, {'id': 210, 'name': '孙策'}, {'id': 211, 'name': '黄忠'}, {'id': 212, 'name': '夏侯惇'}, {'id': 213, 'name': '夏侯渊'}, {'id': 214, 'name': '徐晃'}, {'id': 215, 'name': '甘宁'}, {'id': 217, 'name': '庞德'}, {'id': 218, 'name': '魏延'}, {'id': 219, 'name': '吕蒙'}, {'id': 220, 'name': '孙尚香'}, {'id': 221, 'name': '张郃'}, {'id': 222, 'name': '文丑'}, {'id': 223, 'name': '颜良'}, {'id': 224, 'name': '周泰'}, {'id': 225, 'name': '华雄'}, {'id': 226, 'name': '曹彰'}, {'id': 227, 'name': '严颜'}, {'id': 228, 'name': '董卓'}, {'id': 229, 'name': '张任'}, {'id': 230, 'name': '黄盖'}, {'id': 231, 'name': '关兴'}, {'id': 232, 'name': '孟获'}, {'id': 233, 'name': '廖化'}, {'id': 234, 'name': '曹洪'}, {'id': 235, 'name': '祝融'}, {'id': 236, 'name': '张苞'}, {'id': 237, 'name': '曹仁'}, {'id': 238, 'name': '夏侯霸'}, {'id': 239, 'name': '周仓'}, {'id': 240, 'name': '高顺'}, {'id': 241, 'name': '孙坚'}, {'id': 242, 'name': '凌统'}, {'id': 243, 'name': '程普'}, {'id': 244, 'name': '袁绍'}, {'id': 245, 'name': '马岱'}, {'id': 246, 'name': '淳于琼'}, {'id': 247, 'name': '张济'}, {'id': 248, 'name': '于禁'}, {'id': 249, 'name': '臧霸'}, {'id': 250, 'name': '关平'}, {'id': 251, 'name': '马腾'}, {'id': 252, 'name': '侯成'}, {'id': 253, 'name': '潘凤'}, {'id': 254, 'name': '魏续'}, {'id': 255, 'name': '樊稠'}, {'id': 256, 'name': '李典'}, {'id': 257, 'name': '韩当'}, {'id': 258, 'name': '宋宪'}, {'id': 259, 'name': '张梁'}, {'id': 260, 'name': '韩遂'}, {'id': 261, 'name': '李傕'}, {'id': 262, 'name': '郭汜'}, {'id': 263, 'name': '祖茂'}, {'id': 264, 'name': '徐荣'}, {'id': 265, 'name': '乐进'}, {'id': 267, 'name': '姜维'}, {'id': 268, 'name': '司马懿'}]
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
        # 获取界面中角色等级、金币
        t_player_lv = ui.lineEdit_lv.text()
        t_player_gold = ui.lineEdit_gold.text()
        # 获取界面中 银币、木材、粮食、铁
        t_player_copper = ui.lineEdit_copper.text()
        t_player_wood = ui.lineEdit_wood.text()
        t_player_food = ui.lineEdit_food.text()
        t_player_iron = ui.lineEdit_iron.text()
        try:
            # 修改等级、金币
            cursor.execute("UPDATE player set player_lv = %s , sys_gold = %s where player_id = %s",
                           (t_player_lv, t_player_gold, playerId))
            # 修改银币、木材、粮食、铁
            cursor.execute(
                "UPDATE player_resource SET copper =%s , wood =%s , food =%s , iron =%s where player_id = %s",
                (t_player_copper, t_player_wood, t_player_food, t_player_iron, playerId))
            conn.commit()
        except Exception as e:
            QMessageBox.critical(MainWindow, '提示信息', '修改基础信息报错了！！！', QMessageBox.Ok)
        else:
            QMessageBox.information(MainWindow, '提示信息', '修改基础信息成功！！！', QMessageBox.Ok)
    else:
        QMessageBox.warning(MainWindow, '提示信息', '请先连接数据库！！！', QMessageBox.Ok)


# 修改兵器等级
def modify_weapon():
    # 如果已经连接数据库
    if ui.Button_connectDB.text() == '断开连接':
        try:
            if ui.lineEdit_w1.isEnabled(): # 判断武器1是否已开放
                t_w1 = ui.lineEdit_w1.text()
                cursor.execute("UPDATE player_weapon set lv = %s where player_id = %s and weapon_id = 1",
                               (t_w1, playerId))
            if ui.lineEdit_w2.isEnabled():
                t_w2 = ui.lineEdit_w2.text()
                cursor.execute("UPDATE player_weapon set lv = %s where player_id = %s and weapon_id = 2",
                               (t_w2, playerId))
            if ui.lineEdit_w3.isEnabled():
                t_w3 = ui.lineEdit_w3.text()
                cursor.execute("UPDATE player_weapon set lv = %s where player_id = %s and weapon_id = 3",
                               (t_w3, playerId))
            if ui.lineEdit_w4.isEnabled():
                t_w4 = ui.lineEdit_w4.text()
                cursor.execute("UPDATE player_weapon set lv = %s where player_id = %s and weapon_id = 4",
                               (t_w4, playerId))
            if ui.lineEdit_w5.isEnabled():
                t_w5 = ui.lineEdit_w5.text()
                cursor.execute("UPDATE player_weapon set lv = %s where player_id = %s and weapon_id = 5",
                               (t_w5, playerId))
            if ui.lineEdit_w6.isEnabled():
                t_w6 = ui.lineEdit_w6.text()
                cursor.execute("UPDATE player_weapon set lv = %s where player_id = %s and weapon_id = 6",
                               (t_w6, playerId))
            conn.commit()
        except Exception as e:
            QMessageBox.critical(MainWindow, '提示信息', '更新兵器信息报错了！！！', QMessageBox.Ok)
        else:
            QMessageBox.information(MainWindow, '提示信息', '更新兵器信息成功！！！', QMessageBox.Ok)
    else:
        QMessageBox.warning(MainWindow, '提示信息', '请先连接数据库！！！', QMessageBox.Ok)


# 修改武将信息
def modify_general():
    # 如果已经连接数据库
    if ui.Button_connectDB.text() == '断开连接':
        try:
            # 修改武将1
            if ui.lineEdit_jl1.isEnabled():
                # 获取武将1的名字
                s_jn1 = ui.lineEdit_j1.text()
                # 转换为武将1的id
                s_ji1 = getIdByName(s_jn1)
                # 获取界面上的等级
                t_jl1 = ui.lineEdit_jl1.text()
                # 获取目标武将
                t_jn1 = ui.comboBox_tj1.currentText()
                if t_jn1 != '不变':  # 如果选择了目标武将
                    # 获取目标武将id
                    t_ji1 = getIdByName(t_jn1)
                else:
                    # 目标武将id不变，仍为原武将id
                    t_ji1 = s_ji1
                # 执行sql更新武将信息
                cursor.execute("UPDATE player_general_military set general_id=%s , lv=%s where player_id = %s and general_id = %s",
                               (t_ji1, t_jl1, playerId, s_ji1))
                conn.commit()
            # 修改武将2
            if ui.lineEdit_jl2.isEnabled():
                # 获取武将2的名字
                s_jn2 = ui.lineEdit_j2.text()
                # 转换为武将2的id
                s_ji2 = getIdByName(s_jn2)
                # 获取界面上的等级
                t_jl2 = ui.lineEdit_jl2.text()
                # 获取目标武将
                t_jn2 = ui.comboBox_tj2.currentText()
                if t_jn2 != '不变':  # 如果选择了目标武将
                    # 获取目标武将id
                    t_ji2 = getIdByName(t_jn2)
                else:
                    # 目标武将id不变，仍为原武将id
                    t_ji2 = s_ji2
                # 执行sql更新武将信息
                cursor.execute("UPDATE player_general_military set general_id=%s , lv=%s where player_id = %s and general_id = %s",
                               (t_ji2, t_jl2, playerId, s_ji2))
                conn.commit()
            # 修改武将3
            if ui.lineEdit_jl3.isEnabled():
                # 获取武将3的名字
                s_jn3 = ui.lineEdit_j3.text()
                # 转换为武将3的id
                s_ji3 = getIdByName(s_jn3)
                # 获取界面上的等级
                t_jl3 = ui.lineEdit_jl3.text()
                # 获取目标武将
                t_jn3 = ui.comboBox_tj3.currentText()
                if t_jn3 != '不变':  # 如果选择了目标武将
                    # 获取目标武将id
                    t_ji3 = getIdByName(t_jn3)
                else:
                    # 目标武将id不变，仍为原武将id
                    t_ji3 = s_ji3
                # 执行sql更新武将信息
                cursor.execute("UPDATE player_general_military set general_id=%s , lv=%s where player_id = %s and general_id = %s",
                               (t_ji3, t_jl3, playerId, s_ji3))
                conn.commit()
            # 修改武将4
            if ui.lineEdit_jl4.isEnabled():
                # 获取武将4的名字
                s_jn4 = ui.lineEdit_j4.text()
                # 转换为武将4的id
                s_ji4 = getIdByName(s_jn4)
                # 获取界面上的等级
                t_jl4 = ui.lineEdit_jl4.text()
                # 获取目标武将
                t_jn4 = ui.comboBox_tj4.currentText()
                if t_jn4 != '不变':  # 如果选择了目标武将
                    # 获取目标武将id
                    t_ji4 = getIdByName(t_jn4)
                else:
                    # 目标武将id不变，仍为原武将id
                    t_ji4 = s_ji4
                # 执行sql更新武将信息
                cursor.execute("UPDATE player_general_military set general_id=%s , lv=%s where player_id = %s and general_id = %s",
                               (t_ji4, t_jl4, playerId, s_ji4))
                conn.commit()
            # 修改武将5
            if ui.lineEdit_jl5.isEnabled():
                # 获取武将5的名字
                s_jn5 = ui.lineEdit_j5.text()
                # 转换为武将5的id
                s_ji5 = getIdByName(s_jn5)
                # 获取界面上的等级
                t_jl5 = ui.lineEdit_jl5.text()
                # 获取目标武将
                t_jn5 = ui.comboBox_tj5.currentText()
                if t_jn5 != '不变':  # 如果选择了目标武将
                    # 获取目标武将id
                    t_ji5 = getIdByName(t_jn5)
                else:
                    # 目标武将id不变，仍为原武将id
                    t_ji5 = s_ji5
                # 执行sql更新武将信息
                cursor.execute("UPDATE player_general_military set general_id=%s , lv=%s where player_id = %s and general_id = %s",
                               (t_ji5, t_jl5, playerId, s_ji5))
                conn.commit()
            # 修改武将6
            if ui.lineEdit_jl6.isEnabled():
                # 获取武将6的名字
                s_jn6 = ui.lineEdit_j6.text()
                # 转换为武将6的id
                s_ji6 = getIdByName(s_jn6)
                # 获取界面上的等级
                t_jl6 = ui.lineEdit_jl6.text()
                # 获取目标武将
                t_jn6 = ui.comboBox_tj6.currentText()
                if t_jn6 != '不变':  # 如果选择了目标武将
                    # 获取目标武将id
                    t_ji6 = getIdByName(t_jn6)
                else:
                    # 目标武将id不变，仍为原武将id
                    t_ji6 = s_ji6
                # 执行sql更新武将信息
                cursor.execute("UPDATE player_general_military set general_id=%s , lv=%s where player_id = %s and general_id = %s",
                               (t_ji6, t_jl6, playerId, s_ji6))
                conn.commit()
            # 修改武将7
            if ui.lineEdit_jl7.isEnabled():
                # 获取武将7的名字
                s_jn7 = ui.lineEdit_j7.text()
                # 转换为武将7的id
                s_ji7 = getIdByName(s_jn7)
                # 获取界面上的等级
                t_jl7 = ui.lineEdit_jl7.text()
                # 获取目标武将
                t_jn7 = ui.comboBox_tj7.currentText()
                if t_jn7 != '不变':  # 如果选择了目标武将
                    # 获取目标武将id
                    t_ji7 = getIdByName(t_jn7)
                else:
                    # 目标武将id不变，仍为原武将id
                    t_ji7 = s_ji7
                # 执行sql更新武将信息
                cursor.execute("UPDATE player_general_military set general_id=%s , lv=%s where player_id = %s and general_id = %s",
                               (t_ji7, t_jl7, playerId, s_ji7))
                conn.commit()
            # 修改武将8
            if ui.lineEdit_jl8.isEnabled():
                # 获取武将8的名字
                s_jn8 = ui.lineEdit_j8.text()
                # 转换为武将8的id
                s_ji8 = getIdByName(s_jn8)
                # 获取界面上的等级
                t_jl8 = ui.lineEdit_jl8.text()
                # 获取目标武将
                t_jn8 = ui.comboBox_tj8.currentText()
                if t_jn8 != '不变':  # 如果选择了目标武将
                    # 获取目标武将id
                    t_ji8 = getIdByName(t_jn8)
                else:
                    # 目标武将id不变，仍为原武将id
                    t_ji8 = s_ji8
                # 执行sql更新武将信息
                cursor.execute("UPDATE player_general_military set general_id=%s , lv=%s where player_id = %s and general_id = %s",
                               (t_ji8, t_jl8, playerId, s_ji8))
                conn.commit()
        except Exception as e:
            QMessageBox.critical(MainWindow, '提示信息', '更新武将信息报错了！！！', QMessageBox.Ok)
        else:
            QMessageBox.information(MainWindow, '提示信息', '更新武将信息成功！！！', QMessageBox.Ok)
    else:
        QMessageBox.warning(MainWindow, '提示信息', '请先连接数据库！！！', QMessageBox.Ok)


# 送一套真屠龙
def send_tulong():
    # 如果已经连接数据库
    if ui.Button_connectDB.text() == '断开连接':
        try:
            cursor.execute("INSERT INTO store_house ( `player_id`, `item_id`, `type`, `goods_type`, `owner`, `lv`, `attribute`, `quality`, `gem_id`, `num`, `state`, `refresh_attribute`, `quenching_times`, `quenching_times_free`, `special_skill_id`, `bind_expire_time`, `mark_id`) VALUES ( %s, 525, 14, 14, 0, 0, NULL, 6, 0, 1, 0, '', 0, 0, 0, 0, 0)",
                           playerId)
            conn.commit()
        except Exception as e:
            QMessageBox.critical(MainWindow, '提示信息', '赠送真屠龙报错了！！！', QMessageBox.Ok)
        else:
            QMessageBox.information(MainWindow, '提示信息', '已赠送真屠龙！！！', QMessageBox.Ok)
    else:
        QMessageBox.warning(MainWindow, '提示信息', '请先连接数据库！！！', QMessageBox.Ok)


# 送一个顶级晶石
def send_jingshi():
    # 如果已经连接数据库
    if ui.Button_connectDB.text() == '断开连接':
        try:
            cursor.execute("INSERT INTO store_house ( `player_id`, `item_id`, `type`, `goods_type`, `owner`, `lv`, `attribute`, `quality`, `gem_id`, `num`, `state`, `refresh_attribute`, `quenching_times`, `quenching_times_free`, `special_skill_id`, `bind_expire_time`, `mark_id`) VALUES (%s, 1080, 2, 1, 0, 80, '0', 15, 0, 1, 0, '4:5;3:5;1:5;2:5', 0, NULL, NULL, 0, 0)",
                           playerId)
            conn.commit()
        except Exception as e:
            QMessageBox.critical(MainWindow, '提示信息', '赠送顶级晶石报错了！！！', QMessageBox.Ok)
        else:
            QMessageBox.information(MainWindow, '提示信息', '已赠送顶级晶石！！！', QMessageBox.Ok)
    else:
        QMessageBox.warning(MainWindow, '提示信息', '请先连接数据库！！！', QMessageBox.Ok)


# 通过武将名称取到gid
def getIdByName(name):
    gid = 225
    for i in gs:
        if name == i.get('name'):
            gid = i.get('id')
    return gid


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
    # 设置默认数据
    ui.lineEdit.setText('127.0.0.1')
    ui.lineEdit_2.setText('3306')
    ui.lineEdit_3.setText('root')
    ui.lineEdit_4.setText('1234')
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