#accidentally deleted this earlier
import csv
import cPickle as pickle
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import math

def center_data(lst):
    # centers data to mean 0, variance 1
    mean = sum(lst)/float(len(lst))
    lst = [x - mean for x in lst]
    var = sum([x**2 for x in lst])/float(len(lst))
    std = var**0.5
    lst = [x/std for x in lst]
    return lst

def linear_change(lst):
    # x_t - x_{t-1}
    change = [0]
    for i in range(1, len(lst)):
        change.append(lst[i] - lst[i-1])
    return change

def proportional_change(lst):
    # log(x_t) - log(x_{t-1})
    lst = [math.log(x) for x in lst]
    return linear_change(lst)

def main():
    # load open outcry data into a data frame
    outcry_data = pd.read_csv('./outcry_data.csv')
    outcry_data.TAMIT = proportional_change(outcry_data.TAMIT)
    outcry_data.GDP = proportional_change(outcry_data.GDP)
    plt.plot(outcry_data.GDP, outcry_data.TAMIT)
    plt.show()
    model = smf.ols(formula='TAMIT ~ GDP', data=outcry_data)
    res = model.fit()
    print(res.summary())

if __name__ == '__main__':
    main()
    exit(1)
