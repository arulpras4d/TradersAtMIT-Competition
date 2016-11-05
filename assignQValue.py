import ast
import math
import numpy as np

rnd = 1 	#change after 1st round

with open('data.txt') as f:
	content = f.readlines()

#convert back to dictionaries/lists
buzz = ast.literal_eval(content[0])
buzz_time = ast.literal_eval(content[1])
assoc = ast.literal_eval(content[2])
assoc_time = ast.literal_eval(content[3])
alpha = ast.literal_eval(content[4])
alpha_time = ast.literal_eval(content[5])
god = ast.literal_eval(content[6])
god_time = ast.literal_eval(content[7])

#find mean of data
buzz_mean = {'TRA': np.mean(buzz['TRA']),'DER': np.mean(buzz['DER']),'SA': np.mean(buzz['SA']),'TM': np.mean(buzz['TM']),'IT': np.mean(buzz['IT'])}
assoc_mean  = {'TRA': np.mean(assoc['TRA']),'DER': np.mean(assoc['DER']),'SA': np.mean(assoc['SA']),'TM': np.mean(assoc['TM']),'IT': np.mean(assoc['IT'])}
alpha_mean = {'TRA': np.mean(alpha['TRA']),'DER': np.mean(alpha['DER']),'SA': np.mean(alpha['SA']),'TM': np.mean(alpha['TM']),'IT': np.mean(alpha['IT'])}
god_mean = {'TRA': np.mean(god['TRA']),'DER': np.mean(god['DER']),'SA': np.mean(god['SA']),'TM': np.mean(god['TM']),'IT': np.mean(god['IT'])}

#given standard deviation equation
def std(q,t):
	return (q*(600-t))/60.0


#comparing values to assign q values to each source
#CHANGE, dictionary mean values can't subtract
def assignQ():
	quality_vector = [0.4,0.8,2,4]
	bcount = 0
	ascount = 0
	alcount = 0
	gcount = 0
	result = {'Buzzfeed': 0,'The Associated Press': 0,'Seeking Alpha': 0,'@ETFGodfather': 0}
	for i in quality_vector:
		if len(buzz_time)!= 0 and bcount==0 and buzz_mean-std(i,buzz_time[0]) <= buzz['TRA'][0] <= buzz_mean+std(i,buzz_time[0]) and buzz_mean-std(i,buzz_time[1]) <= buzz['TRA'][1] <= buzz_mean+std(i,buzz_time[1]) and buzz_mean-std(i,buzz_time[2]) <= buzz['TRA'][2] <= buzz_mean+std(i,buzz_time[2]):
			result['Buzzfeed'] = i
			bcount = 1
		if len(assoc_time)!= 0 and ascount==0 and assoc_mean-std(i,assoc_time[0]) <= assoc['TRA'][0] <= assoc_mean+std(i,assoc_time[0]) and assoc_mean-std(i,assoc_time[1]) <= assoc['TRA'][1] <= assoc_mean+std(i,assoc_time[1]) and assoc_mean-std(i,assoc_time[2]) <= assoc['TRA'][2] <= assoc_mean+std(i,assoc_time[2]):
			result['The Associated Press'] = i
			ascount = 1
		if len(alpha_time)!= 0 and alcount==0 and alpha_mean-std(i,alpha_time[0]) <= alpha['TRA'][0] <= alpha_mean+std(i,alpha_time[0]) and alpha_mean-std(i,alpha_time[1]) <= alpha['TRA'][1] <= alpha_mean+std(i,alpha_time[1]) and alpha_mean-std(i,alpha_time[2]) <= alpha['TRA'][2] <= alpha_mean+std(i,alpha_time[2]):
			result['Seeking Alpha'] = i
			alcount = 1
		if len(god_time)!= 0 and gcount==0 and god_mean-std(i,god_time[0]) <= god['TRA'][0] <= god_mean+std(i,god_time[0]) and god_mean-std(i,god_time[1]) <= god['TRA'][1] <= god_mean+std(i,god_time[1]) and god_mean-std(i,god_time[2]) <= god['TRA'][2] <= god_mean+std(i,god_time[2]):
			result['@ETFGodfather'] = i
			gcount = 1

	return result

#index price is weighted average of stock prices
def index(true_price_list):
	return sum(true_price_list)/len(true_price_list)

#given true price range
true_price_range = {'TRA':[20.0,40.0],'DER':[10.0,20.0],'SA':[60.0,90.0],'TM':[30.0,70.0],'IT':[50.0,80.0]}

#given correlation coefficients, [TRA,DER,SA,TM,IT]
correlation_coefficients = [[1,0.46,-0.58,-0.6,-0.39],[0.46,1,-0.22,0,-0.38],[-0.58,-0.22,1,-0.11,0.52],[-0.06,0,-0.11,1,-0.19],[-0.39,-0.38,0.52,-0.19,1]]

#assigns qvalues
if rnd == 1:
	qvalues = assignQ()
else:
	qvalues = {'Buzzfeed': 0,'The Associated Press': 0,'Seeking Alpha': 0,'@ETFGodfather': 0}			#change to values at end of round 1

def estimate_distribution_mean():
	Z = 1 		#confidence level 68%
	source_names = ['Buzzfeed','The Associated Press','Seeking Alpha','@ETFGodfather']
	stock_names = ['TRA','DER','SA','TM','IT']
	for i in source_names:
		for j in stock_names:
			if i == 'Buzzfeed':
				error = Z*((std(qvalues[i]),buzz_time[-1])/(math.sqrt(len(buzz[j])-1)))
				minval = buzz_mean[j]-error
				maxval = buzz_mean[j]+error
				print("Buzzfeed ",j,": ",minval,", ",maxval,'\n')
			elif i == 'The Associated Press':
				error = Z*((std(qvalues[i]))/(math.sqrt(len(assoc[j])-1)))
				minval = assoc_mean[j]-error
				maxval = assoc_mean[j]+error
				print("The Associated Press ",j,": ",minval,", ",maxval,'\n')
			elif i == 'Seeking Alpha':
				error = Z*((std(qvalues[i]))/(math.sqrt(len(alpha[j])-1)))
				minval = alpha_mean[j]-error
				maxval = alpha_mean[j]+error
				print("Seeking Alpha ",j,": ",minval,", ",maxval,'\n')
			else:
				error = Z*((std(qvalues[i]))/(math.sqrt(len(god[j])-1)))
				minval = god_mean[j]-error
				maxval = god_mean[j]+error
				print("@ETFGodfather ",j,": ",minval,", ",maxval,'\n')