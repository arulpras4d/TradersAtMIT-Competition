from tradersbot import TradersBot
from assignQValue import estimate_distribution_mean

#initialize tradersbot
t = TradersBot('localhost','trader0','trader0')

buzz = {'TRA':[],'DER':[],'SA':[],'TM':[],'IT':[]}
assoc = {'TRA':[],'DER':[],'SA':[],'TM':[],'IT':[]}
alpha = {'TRA':[],'DER':[],'SA':[],'TM':[],'IT':[]}
god = {'TRA':[],'DER':[],'SA':[],'TM':[],'IT':[]}
buzz_time = []
assoc_time = []
alpha_time = []
god_time = []
#gets estimation data from news
def news_Callback(msg,TradersOrder):
	temp = msg["news"]["body"].split(";")
	tempTRA = temp[0].split(" ")
	tempDER = temp[1].split(" ")
	tempSA = temp[2].split(" ")
	tempTM = temp[3].split(" ")
	tempIT = temp[4].split(" ")

	if msg["news"]["source"] == 'Buzzfeed':
		buzz['TRA'].append(float(tempTRA[-1]))
		buzz['DER'].append(float(tempDER[-1]))
		buzz['SA'].append(float(tempSA[-1]))
		buzz['TM'].append(float(tempTM[-1]))
		buzz['IT'].append(float(tempIT[-1]))
		buzz_time.append(msg["news"]["time"])
	elif msg["news"]["source"] == 'The Associated Press':
		assoc['TRA'].append(float(tempTRA[-1]))
		assoc['DER'].append(float(tempDER[-1]))
		assoc['SA'].append(float(tempSA[-1]))
		assoc['TM'].append(float(tempTM[-1]))
		assoc['IT'].append(float(tempIT[-1]))
		assoc_time.append(msg["news"]["time"])
	elif msg["news"]["source"] == 'Seeking Alpha':
		alpha['TRA'].append(float(tempTRA[-1]))
		alpha['DER'].append(float(tempDER[-1]))
		alpha['SA'].append(float(tempSA[-1]))
		alpha['TM'].append(float(tempTM[-1]))
		alpha['IT'].append(float(tempIT[-1]))
		alpha_time.append(msg["news"]["time"])
	else:
		god['TRA'].append(float(tempTRA[-1]))
		god['DER'].append(float(tempDER[-1]))
		god['SA'].append(float(tempSA[-1]))
		god['TM'].append(float(tempTM[-1]))
		god['IT'].append(float(tempIT[-1]))
		god_time.append(msg["news"]["time"])

	f = open('data.txt','w')
	f.write(str(buzz))
	f.write('\n')
	f.write(str(buzz_time))
	f.write('\n')
	f.write(str(assoc))
	f.write('\n')
	f.write(str(assoc_time))
	f.write('\n')
	f.write(str(alpha))
	f.write('\n')
	f.write(str(alpha_time))
	f.write('\n')
	f.write(str(god))
	f.write('\n')
	f.write(str(god_time))
	f.close()

	#from assignQValue.py
	estimate_distribution_mean()
#run tradersbot
t.onNews = news_Callback
t.run()