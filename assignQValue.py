import ast
import math
import numpy as np

rnd = 1 	#change after 1st round

	
def estimate_distribution_mean():
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
			for j in range(0,len(buzz_time)):
				if buzz_mean['TRA']-std(i,buzz_time[j]) <= buzz['TRA'][j] <= buzz_mean['TRA']+std(i,buzz_time[j]):
					bcount+=1
				if bcount == len(buzz_time):
					result['Buzzfeed'] = i
			for j in range(0,len(assoc_time)):
				if assoc_mean['TRA']-std(i,assoc_time[j]) <= assoc['TRA'][j] <= assoc_mean['TRA']+std(i,assoc_time[j]):
					ascount+=1
				if ascount == len(assoc_time):
					result['The Associated Press'] = i
			for j in range(0,len(alpha_time)):
				if alpha_mean['TRA']-std(i,alpha_time[j]) <= alpha['TRA'][j] <= alpha_mean['TRA']+std(i,alpha_time[j]):
					alcount+=1
				if alcount == len(alpha_time):
					result['Seeking Alpha'] = i
			for j in range(0,len(god_time)):
				if god_mean['TRA']-std(i,god_time[j]) <= god['TRA'][j] <= god_mean['TRA']+std(i,god_time[j]):
					gcount+=1
				if gcount == len(god_time):
					result['@ETFGodfather'] = i

		return result

	#index price is sum of stock prices
	def index(prices):
		return sum(prices)

	#given true price range
	true_price_range = {'TRA':[20.0,40.0],'DER':[10.0,20.0],'SA':[60.0,90.0],'TM':[30.0,70.0],'IT':[50.0,80.0]}

	#given correlation coefficients, [TRA,DER,SA,TM,IT]
	correlation_coefficients = [[1,0.46,-0.58,-0.6,-0.39],[0.46,1,-0.22,0,-0.38],[-0.58,-0.22,1,-0.11,0.52],[-0.06,0,-0.11,1,-0.19],[-0.39,-0.38,0.52,-0.19,1]]

	#assigns qvalues
	if rnd == 1:
		qvalues = assignQ()
	else:
		qvalues = {'Buzzfeed': 0,'The Associated Press': 0,'Seeking Alpha': 0,'@ETFGodfather': 0}			#change to values at end of round 1

	Z = 1 		#confidence level 68%
	source_names = ['Buzzfeed','The Associated Press','Seeking Alpha','@ETFGodfather']
	stock_names = ['TRA','DER','SA','TM','IT']
	print(qvalues)
	for i in source_names:
		index_min = 0
		index_max = 0
		for j in stock_names:
			if i == 'Buzzfeed' and len(buzz_time)!=0:
				if len(buzz[j])>1:
					error = Z*((std(qvalues[i],buzz_time[-1]))/(math.sqrt(len(buzz[j])-1)))
				else:
					error = 0
				minval = buzz_mean[j]-error
				maxval = buzz_mean[j]+error
				print("Buzzfeed ",j,": ",minval,", ",maxval)
				index_min+=minval
				index_max+=maxval
				if j == 'IT':
					print("Buzzfeed IDX: ",index_min,", ",index_max)
			elif i == 'The Associated Press' and len(assoc_time)!=0:
				if len(assoc[j])>1:
					error = Z*((std(qvalues[i],assoc_time[-1]))/(math.sqrt(len(assoc[j])-1)))
				else:
					error = 0
				minval = assoc_mean[j]-error
				maxval = assoc_mean[j]+error
				print("The Associated Press ",j,": ",minval,", ",maxval)
				index_min+=minval
				index_max+=maxval
				if j == 'IT':
					print("The Associated Press IDX: ",index_min,", ",index_max)
			elif i == 'Seeking Alpha' and len(alpha_time)!=0:
				if len(alpha[j])>1:
					error = Z*((std(qvalues[i],alpha_time[-1]))/(math.sqrt(len(alpha[j])-1)))
				else:
					error = 0
				minval = alpha_mean[j]-error
				maxval = alpha_mean[j]+error
				print("Seeking Alpha ",j,": ",minval,", ",maxval)
				index_min+=minval
				index_max+=maxval
				if j == 'IT':
					print("Seeking Alpha IDX: ",index_min,", ",index_max)
			elif i == '@ETFGodfather' and len(god_time)!=0:
				if len(god[j])>1:
					error = Z*((std(qvalues[i],god_time[-1]))/(math.sqrt(len(god[j])-1)))
				else:
					error = 0
				minval = god_mean[j]-error
				maxval = god_mean[j]+error
				print("@ETFGodfather ",j,": ",minval,", ",maxval)
				index_min+=minval
				index_max+=maxval
				if j == 'IT':
					print("@ETFGodfather IDX: ",index_min,", ",index_max)