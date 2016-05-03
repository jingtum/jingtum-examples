#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

from jingtumsdk.jingtumwallet import FinGate
from jingtumsdk.jingtumwallet import Wallet
from jingtumsdk.logger import logger
import time
import sys
import re
import pprint

wait_seconds = 0
WAIT_SECONDS = 90
transaction_done = False

#config just for test
test_api_address = "tapi.jingtum.com"
is_https_false = False
is_https_true = True
test_web_socket_address = "wss://tapi.jingtum.com:5443" 
api_version_v2 = "v2"
api_version_v1 = "v1"

# root account just for test
test_address = "jHb9CJAWyB4jr91VRWn96DkukG4bwdtyTh"
test_secret = "snoPBjXtMeMyMHUVTgbuqAfg1SUTb"
test_issuer = "jBciDE8Q3uJjf111VeiUNM775AMKHEbBLS"

# ulimit account just for test
test_ulimit_address = "jJ8PzpT7er3tXEWaUsVTPy3kQUaHVHdxvp"
test_ulimit_secret = "shYK7gZVBzw4m71FFqZh9TWGXLR6Q"

fingate_attributes = [('clienthelper','api服务器'),('is_https','安全连接'),('api_version','api版本'),('ws','web socket')]
fingate_methods = [('getPrefix','交易前缀'),('getActiveAmount','激活数量'), ('getTrustLimit','信任额度'),('getServerInfo','银关信息'), ('getStatus','服务器状态'), ('getFinGate','银关账号')]
#,('issueCustomTum','发通通')]
def show_wallet(wallets):
	for wallet_tuple in wallets:
		try:
			print("%s:\t%s\t%s" % (wallet_tuple[0], wallet_tuple[1].address, wallet_tuple[1].secret))
		except Exception as e:
			print("钱包 %s 有误: %s" % (wallet_tuple[0],e))
def show_fingate(fingates):
	for fingate_tuple in fingates:
		if type(fingate_tuple) == type(()):
			print("\n... %s" % fingate_tuple[0])
			fg = fingate_tuple[1]
		else:
			print("\n... %s" % fingate_tuple)
			fg = fingate_tuple
		for attr in fingate_attributes:
			try:
				if attr[0] == 'clienthelper':
					print("\t%s:\t\t%s" % (attr[1],getattr(fg,attr[0]).netloc))
				else:
					print("\t%s:\t\t%s" % (attr[1],getattr(fg,attr[0])))
			except Exception as e:
				print("\t\t.!.!.!没有属性 %s" % attr[0])
				print("\t\t\t%s" % e)
		for attr in fingate_methods:
			try:
				print("\t%s\t\t%s" % (attr[1],str(getattr(fg,attr[0])())))
			except Exception as e:
				print("\t%s:" % (attr[1]))
				print("\t\t.!.!.!调用 .%s() 错误: %s" % (attr[0],e))
# init FinGate

print("\n********银关测试*********")
#answer = raw_input("->敲击键盘开始测试 ->   ")
print("fingate_settest, fingate_v1, fingate_v2  初始化 FinGate():")
fingate = FinGate()
fingate_settest = FinGate()
fingate_v1 = FinGate()
fingate_v2 = FinGate()
fingate_list = [('fingate_settest',fingate_settest),('fingate_setserver_v1',fingate_v1),('fingate_setserver_v2',fingate_v2)]
print("fingate_settest 设置测试环境.setTest():")
fingate_settest.setTest()
print("fingate_v1 设置测试环境.setServer():")
fingate_v1.setServer(test_api_address, is_https_true, test_web_socket_address, api_version_v1)
print("fingate_v2 设置测试环境 .setServer():")
fingate_v2.setServer(test_api_address, is_https_true, test_web_socket_address, api_version_v2)
print("设置银关账号 .setFingate():")
fingate.setFinGate(test_address, test_secret)
for fingate_tuple in fingate_list:
	fingate_tuple[1].setFinGate(test_address, test_secret)
print("设置激活和信任额度 .setActiveAmount() 和 .setTrustLimit()")
fingate.setActiveAmount(5)
fingate.setTrustLimit(50)
fingate_settest.setActiveAmount(1)
fingate_settest.setTrustLimit(10)
fingate_v1.setActiveAmount(10)
fingate_v2.setActiveAmount(100)
fingate_v1.setTrustLimit(1000)
fingate_v2.setTrustLimit(10000)
print("设置交易流水前缀 .setPrefix() 和 .getPrefix()")
fingate.setPrefix('JT')
fingate_settest.setPrefix('WA')
fingate_v1.setPrefix('WB')
fingate_v2.setPrefix('WC')

print("设置通通服务 .setTTongServer()")
if hasattr(fingate_settest,'setTTongServer'):
	for fingate_tuple in fingate_list:
		fingate_tuple[1].setTTongServer(True,'3fec2e6ce676f9be2a9da8bc39cc327838f1eb54ce54a4087807b2cff3cf8637','JT0000002C')
else:
	print("\t.!.!.! 没有 .setTTongServer() method")

print("获取资源号 .getNextUUID()")
for fingate_tuple in fingate_list:
	print("\t%s:\t->%s" % ( fingate_tuple[0],fingate_tuple[1].getNextUUID()))

print("\n********+钱包测试*********")

print("创建钱包 .createWallet()")
wallet_list = []
wallet = None
for fingate_tuple in fingate_list:
	wallet_var = re.sub(r'fingate','wallet',fingate_tuple[0])
	create_wallet = fingate_tuple[1].createWallet()
	if create_wallet.has_key('success') and create_wallet['success']:
		my_address, my_secret = create_wallet["wallet"]["address"], create_wallet["wallet"]["secret"]
		print("\t......钱包创建成功")
#		print("\t\t%s:\t%s : %s" % (wallet_var, my_address, my_secret))
		wallet = Wallet(my_address,my_secret,fingate=fingate_tuple[1])
		wallet_list.append((wallet_var,wallet))
	else:
		print("\t.!.!.!钱包创建失败")
		print("%s" % wallet_var)

wallet_settest = wallet_list[0][1]
wallet_v1 = wallet_list[1][1]
wallet_v2 = wallet_list[2][1]

if len(wallet_list) < len(fingate_list):
	print(".!.!.!钱包创建有问题")
if __name__ == "__main__":
	print("\n*****显示银关*****")
	show_fingate([('fingate_formal',fingate),] + fingate_list)
	print("*****显示创建的三个钱包，对应于前面三个测试银关*****")
	show_wallet(wallet_list)
	print("\n*******激活钱包*************")
	print("\t银关 %s 同步激活 %s" % ("fingate_settest", "wallet_settest"))
	try:
		ret_settest = fingate_settest.activeWallet(wallet_settest.address,is_sync=True)
	except Exception as e:
		print("激活失败 %s" % e)
	print("\t银关 %s 同步激活 %s" % ("fingate_setserver_v1", "wallet_setserver_v1"))
	try:
		ret_v1 = fingate_v1.activeWallet(wallet_v1.address,is_sync=True)
	except Exception as e:
		print("激活失败 %s" % e)
	print("\t银关 %s 异步激活 %s" % ("fingate_setserver_v2", "wallet_setserver_v2"))
	try:
		ret_v2 = fingate_v2.activeWallet(wallet_v2.address,is_sync=False)
	except Exception as e:
		print("激活失败 %s" % e)
	if not ret_settest:
		print("\nfingate_settest 激活 wallet_settest 失败")
	else:
		print("fingate_settest 激活 wallet_settest 成功")
	if not ret_v1:
		print("fingate_setserver_v1 激活 wallet_setserver_v1 失败")
	else:
		print("fingate_setserver_v1 激活 wallet_setserver_v1 成功")

	if ret_v2 and 'success' in ret_v2.keys() and ret_v2['success']:
		client_resource_v2 = ret_v2['client_resource_id']
		time.sleep(10)
		while not wallet_v2.isActivated() and wait_seconds < WAIT_SECONDS:
			print("等候异步激活完成")
			wait_seconds += 10 
			time.sleep(10)
			transaction_done = True
			print("\t... .getTransaction(\'%s\')" % client_resource_v2)
			pprint.pprint(wallet_v2.getTransaction(client_resource_v2))
			print("\t... .getBalance()")
			pprint.pprint(wallet_v2.getBalance())
	
		if wallet_v2.isActivated():
			print("fingate_setserver_v2 激活 wallet_setserver_v2 成功")
			balance_v2 = wallet_v2.getBalance()
			if not transaction_done:
				print("\t... .getTransaction(\'%s\')" % client_resource_v2)
				pprint.pprint(wallet_v2.getTransaction(client_resource_v2))
				print("\t... .getBalance()")
				pprint.pprint(wallet_v2.getBalance())
			print("钱包信息")
			print("\t... .isActivated()  = %s" % wallet_v2.isActivated())
			print("\t... .getSecret()    = %s" % wallet_v2.getSecret())
			print("\t... .getAddress()   = %s" % wallet_v2.getAddress())
			print("\t... .getWallet()    = %s %s" % wallet_v2.getWallet())
			print("\n******转账操作*********")
			print("\n\t现在用fingate_v2作一些账户操作")
			wallet_ulimit = Wallet(test_ulimit_address, test_ulimit_secret,fingate=fingate_v2)
			print("\t... wallet_setserver_v2.submitPayment() 同步转给 wallet_setserver_v1 25个井通")
			pprint.pprint(wallet_v2.submitPayment('SWT',25,wallet_v1.address,is_sync=True))
			print("\t... wallet_ulimit.submitPayment() 同步转给 wallet_setserver_v1 1000个井通")
			pprint.pprint(wallet_ulimit.submitPayment('SWT',1000,wallet_v1.address,is_sync=True))
			print("\t... wallet_ulimit.submitPayment() 同步转给 wallet_setserver_v1 75 美元")
			pprint.pprint(wallet_ulimit.submitPayment('USD',75,wallet_v1.address,issuer=test_issuer,is_sync=True))
			print("\t\t wallet_setserver_v1 钱包状态 和 盈余")
			print("\t\t .isActivated() = %s before .getBalance()" % wallet_v1.isActivated())
			pprint.pprint(wallet_v1.getBalance())
			print("\t\t .isActivated() = %s after .getBalance()" % wallet_v1.isActivated())
	
	
		else:
			print("fingate_setserver_v2 激活 wallet_setserver_v2 失败")
	
	else:
		print("fingate_setserver_v2 激活 wallet_setserver_v2 失败")
