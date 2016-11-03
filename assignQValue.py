#probably have to do this in between 1st and 2nd rounds
import ast
import numpy as np

dataFile = 'data.txt'

with open(dataFile) as f:
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

#given std equation and quality vector
def std(q,t):
	return (q*(600-t))/60.0

quality_vector = [0.4,0.8,2,4]

#comparing values to assign q values to each source
print(buzz_mean,assoc_mean,alpha_mean,god_mean)


print(buzz['TRA'][0],assoc['TRA'][0],alpha['TRA'][0],god['TRA'][0])
print(buzz['TRA'][1],assoc['TRA'][1],alpha['TRA'][1],god['TRA'][1])
print(buzz['TRA'][2],assoc['TRA'][2],alpha['TRA'][2],god['TRA'][2])

print(std(quality_vector[1],buzz_time[1]))
print(std(quality_vector[0],assoc_time[1]))
print(std(quality_vector[3],alpha_time[1]))
print(std(quality_vector[2],god_time[1]))

