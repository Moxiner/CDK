from cmath import e
from datetime import date
from distutils import command
from fileinput import close
from msilib.schema import Class
from warnings import WarningMessage
import mc
import os
import json
import time
PluginName = "CDK"
ConfigPath = "plugins/py/CDK"

class InitializationFile:
    def CreateFile():
        '''创建 date 文件'''
        try:
            if os.path.exists(f"{ConfigPath}/date.json"):
                PrintLog.InfoLog("配置文件已存在")
            else:
                os.makedirs(ConfigPath)
                configFilm = open(f"{ConfigPath}/date.json","w+")
                configFilm.close()
                PrintLog.InfoLog("配置文件创建完成")
        except :
            PrintLog.ErroeLog("配置文件创建失败")

class PrintLog:
    '''标准化输出'''   
    def GetTime():
        '''获取当前时间'''
        return time.strftime("%H:%M:%S")

    def InfoLog(concent:str):
        '''输出Info通知'''
        mc.logout(f"\033[0m[{PrintLog.GetTime()} Info][{PluginName}] {concent}\n\033[0m")
    
    def WarmLog(concent:str):
        '''输出Warm警告'''
        mc.logout(f"\033[1;33m[{PrintLog.GetTime()} Info][{PluginName}] {concent}\n\033[0m")
    
    def ErroeLog(concent:str):
        '''输出Erroe错误'''
        mc.logout(f"\033[1;31m[{PrintLog.GetTime()} Info][{PluginName}] {concent}\n\033[0m")

class GUI:
    '''GUI界面，GUI处理并返回为字典结果'''
    def manage(admin):
        '''管理界面，GUI处理并返回为字典结果'''
        j = {
            "content":[{"type":"label","text":"管理兑换妈"},
            {"default":1,"options":["添加兑换码","删除兑换码"],"type":"dropdown","text":"请选择发放模式"}
            ],"type":"custom_form","title":"管理兑换码"
            }
        return admin.sendCustomForm(f"{j}")

    def add(admin):
        '''添加兑换码界面，GUI处理并返回为字典结果'''
        j = {
            "content":[{"type":"label","text":"添加兑换码"},
            {"placeholder":"请输入兑换码","default":"","type":"input","text":""},
            {"type":"label","text":"发放模式"},
            {"default":1,"options":["单人单次使用","多人单次使用"],"type":"dropdown","text":"请选择发放模式"},
            {"type":"label","text":"发放内容"},
            {"default":1,"options":["计分板","手持物品","计分板和手持物品"],"type":"dropdown","text":"请选择发放内容"},
            {"type":"label","text":"计分板名称"},
            {"placeholder":"请输入计分板名称","default":"","type":"input","text":""},
            {"type":"label","text":"计分板数量"},
            {"placeholder":"请输入计分板数量","default":"","type":"input","text":""}
            ],"type":"custom_form","title":"添加兑换码"
            }
        date = admin.sendCustomForm(f"{j}")
        return date
    def remove(admin):
        '''删除兑换码界面，GUI处理并返回为字典结果'''

        j = {
             "content":[ #{"type":"label","text":"删除兑换码"},
            {"default":1,"options":[f"{DateDeal.GetCDK()}"],"type":"dropdown","text":"删除兑换码"}
            ],"type":"custom_form","title":"删除兑换码"
            }
        date = admin.sendCustomForm(f"{j}")
        return date

    def use(player):
        '''使用兑换码界面，GUI处理并返回为字典结果'''

        j = {
            "content":[{"type":"label","text":"兑换码"},
            {"placeholder":"请输入兑换码","default":"","type":"input","text":""}
            ],"type":"custom_form","title":"兑换码"
            }
        date = player.sendCustomForm(f"{j}")
        return date

class DateDeal:
    '''处理数据'''
    def GetCDK():
        '''获取兑换码并返回为列表结果'''
        j = open(f"{ConfigPath}/date.json")
        date = json.load(j)
        close
        return date.key()
    def ManageCDK(e):
        date = GUI.manage(e)
        PrintLog(f"{date}")

    def AddCDK(e):
        date = GUI.add(e)
        PrintLog(f"{date}")

    def DelCDK(e):
        date = GUI.add(e)
        PrintLog(f"{date}")

    def UseCDK(e):
        date = GUI.use(e)
        PrintLog(f"{date}")

class Command:
    def Input(e):
        cmd = e["cmd"]
        player = e["player"]
        if cmd == "/cdk manage":
            if player.perm != 0:
                DateDeal.ManageCDK(player)
            else:
                player.sendTextPacket("§l§7[§2CDK§7]§e你没有足够的权限") 
        elif cmd == "/cdk add":
            if player.perm != 0:
                DateDeal.AddCDK(player)
            else:
                player.sendTextPacket("§l§7[§2CDK§7]§e你没有足够的权限") 
        elif cmd == "/cdk del":
            if player.perm != 0:
                DateDeal.DelCDK(player)
            else:
                player.sendTextPacket("§l§7[§2CDK§7]§e你没有足够的权限") 
        elif cmd == "/cdk":
            DateDeal.UseCDK(player)
        return False
InitializationFile.CreateFile()
mc.setListener("onInputCommand",Command.Input)
mc.setCommandDescription("cdk manage","兑换码管理",)
mc.setCommandDescription("cdk add","添加兑换码")
mc.setCommandDescription("cdk del","删除兑换码")
mc.setCommandDescription("cdk","使用兑换码")

PrintLog.InfoLog("加载完成  版本0.01")
PrintLog.InfoLog("作者：莫欣儿")

