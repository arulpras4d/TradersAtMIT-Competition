#Run in between 1st and 2nd rounds of PD
import ast
import numpy as np

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
buzz_mean = np.mean(buzz['TRA'])
assoc_mean  = np.mean(assoc['TRA'])
alpha_mean = np.mean(alpha['TRA'])
god_mean = np.mean(god['TRA'])

#given std equation
def std(q,t):
	return (q*(600-t))/60.0


#comparing values to assign q values to each source
def assignQ():
	quality_vector = [0.4,0.8,2,4]
	bcount = 0
	ascount = 0
	alcount = 0
	gcount = 0
	result = {'Buzzfeed': 0,'The Associated Press': 0,'Seeking Alpha': 0,'@ETFGodfather': 0}
	for i in quality_vector:
		if bcount==0 and buzz_mean-std(i,buzz_time[0]) <= buzz['TRA'][0] <= buzz_mean+std(i,buzz_time[0]) and buzz_mean-std(i,buzz_time[1]) <= buzz['TRA'][1] <= buzz_mean+std(i,buzz_time[1]) and buzz_mean-std(i,buzz_time[2]) <= buzz['TRA'][2] <= buzz_mean+std(i,buzz_time[2]):
			result['Buzzfeed'] = i
			bcount = 1
		if ascount==0 and assoc_mean-std(i,assoc_time[0]) <= assoc['TRA'][0] <= assoc_mean+std(i,assoc_time[0]) and assoc_mean-std(i,assoc_time[1]) <= assoc['TRA'][1] <= assoc_mean+std(i,assoc_time[1]) and assoc_mean-std(i,assoc_time[2]) <= assoc['TRA'][2] <= assoc_mean+std(i,assoc_time[2]):
			result['The Associated Press'] = i
			ascount = 1
		if alcount==0 and alpha_mean-std(i,alpha_time[0]) <= alpha['TRA'][0] <= alpha_mean+std(i,alpha_time[0]) and alpha_mean-std(i,alpha_time[1]) <= alpha['TRA'][1] <= alpha_mean+std(i,alpha_time[1]) and alpha_mean-std(i,alpha_time[2]) <= alpha['TRA'][2] <= alpha_mean+std(i,alpha_time[2]):
			result['Seeking Alpha'] = i
			alcount = 1
		if gcount==0 and god_mean-std(i,god_time[0]) <= god['TRA'][0] <= god_mean+std(i,god_time[0]) and god_mean-std(i,god_time[1]) <= god['TRA'][1] <= god_mean+std(i,god_time[1]) and god_mean-std(i,god_time[2]) <= god['TRA'][2] <= god_mean+std(i,god_time[2]):
			result['@ETFGodfather'] = i
			gcount = 1

	return result

result = assignQ()
print(result)