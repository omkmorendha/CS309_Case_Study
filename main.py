# with open('Data.csv', 'r') as inp:
#     lines = inp.readlines()

# with open('purged_csv_file.csv', 'w') as out:
#     for line in lines:
#         if not '?' in line:
#             out.write(line)

import pandas as pd
import random as rand
from math import sqrt
from scipy.stats import chi2
from scipy.stats import norm
from scipy.stats import t

def mean(arr):
    total = 0
    for element in arr:
        total += element
    
    return total / len(arr)

def median(arr):
    arr = list(arr)
    arr.sort()
    n = len(arr)
    if n&1 == 1:
        return arr[n//2]
    else:
        return (arr[n//2]+arr[(n//2)-1])/2

def sd(arr):                #Standard Deviation
    ans = 0
    m = mean(arr)

    for element in arr:
        ans += (element - m) ** 2

    return ans / len(arr)

def simple_random_sampling(arr, n):
    visited = []

    while(len(visited) < n and len(visited) < len(arr)):
        i = rand.randint(0, len(arr) - 1)        
        
        if (arr[i] not in visited):
            visited.append(arr[i])

    return visited

def sample_size_single_mean(Za, S, d):
    n = (Za * S / d) ** 2
    return n

def sample_size_two_mean(Za, Zb, s, m1, m2):
    n = (2 * s * (Za + Zb) / (m1 - m2)) ** 2
    return n

def one_sample_z_test(sample, estimated_mean, z_tab):
    sample_mean = mean(sample)
    sample_sd = sd(sample)
    sample_size = len(sample)
    z_calc = abs(sample_mean - estimated_mean)/(sample_sd/sqrt(sample_size-1))
    print(f"Z_calc = {z_calc} and Z_tab = {z_tab}")

    if z_calc <= z_tab:
        print("Null hypothesis is accepted")
    else:
        print("Null hypothesis is rejected")

def two_sample_z_test(sample1, sample2, z_tab):
    s1_mean = mean(sample1)
    s2_mean = mean(sample2)

    s1_sd = sd(sample1)
    s2_sd = sd(sample2)

    s1_size = len(sample1)
    s2_size = len(sample2)

    z_calc = abs(s1_mean-s2_mean)/sqrt(s1_sd**2/s1_size + s2_sd**2/ s2_size)

    print(f"Z_cal = {z_calc} and Z_tab = {z_tab}")
    if z_calc <= z_tab:
        print("Null hypothesis accepted")
    else:
        print("Null hypothesis is rejected")

def one_sample_t_test(sample, population_mean, t_tab):
    sample_mean = mean(sample)
    sample_sd = sd(sample)
    sample_size = len(sample)
    t_calc = abs(sample_mean - population_mean)/(sample_sd/sqrt(sample_size-1))
    print(f"t_cal = {t_calc} and t_tab = {t_tab}")
    if t_calc <= t_tab:
        print("Accept Null hypothesis")
    else:
        print("Null hypothesis rejected")

def two_sample_t_test(sample1, sample2, t_tab):
    s1_mean = mean(sample1)
    s2_mean = mean(sample2)

    s1_sd = sd(sample1)
    s2_sd = sd(sample2)

    s1_size = len(sample1)
    s2_size = len(sample2)

    t_calc = abs(s1_mean-s2_mean)/(sqrt(s1_sd**2/s1_size + s2_sd**2/s2_size))
    print(f"t_cal = {t_calc} and t_tab = {t_tab}")
    if t_calc <= t_tab:
        print("Accept Null hypothesis")
    else:
        print("Null hypothesis rejected")

def rank_test(sample, tab_value):
    m = median(tuple(sample))
    i=0
    while(i<len(sample)):
        if sample[i] == m:
            del sample[i]
            continue
        i+=1

    runs = 1
    for i in range(len(sample) - 1):
        if (sample[i]-m)*(sample[i+1]-m)<0:
            runs += 1

    if runs in range(tab_value[0],tab_value[1]+1):
        print("Accept Null Hypothesis")
    else:
        print("Reject Null Hypothesis")

def one_sample_sign_test(sample, tab_value, conjectured_median):
    neg_count = 0
    pos_count = 0
    n = len(sample)

    for value in sample:
        if value<conjectured_median:
            neg_count+=1
        elif value> conjectured_median:
            pos_count+=1
        else:
            n-=1

    x = min(pos_count, neg_count)
    z = ((x+0.05)-(n/2)) / sqrt(n/2)
    if abs(z) <= tab_value:
        print("Reject Null Hypothesis")
    else:
        print("Accept Null Hypothesis")

def two_sample_sign_test(before_sample, after_sample, tab_value):
    neg_count = 0
    pos_count = 0
    n = len(before_sample)

    for i in range(len(before_sample)):
        if before_sample[i]-after_sample[i] < 0:
            neg_count += 1
        elif before_sample[i]-after_sample[i]>0:
            pos_count += 1
        else:
            n -= 1

    x = min(pos_count, neg_count)
    z = ((x + 0.05) - (n / 2)) / sqrt(n / 2)
    if abs(z) <= tab_value:
        print("Reject Null Hypothesis")
    else:
        print("Accept Null Hypothesis")

def rank_sum_test(sample1, sample2, tab_value):
    data = sample1 + sample2
    freq = {}
    rank = {}

    for d in data:
      if d in freq.keys():
        freq[d] += 1
      else:
        freq[d] = 1

    data.sort()

    for i in range(len(data)):
      if data[i] not in rank.keys():
        rank[data[i]] = i + (freq[data[i]]+1)/2

    n1 = min(len(sample1), len(sample2))
    n2 = max(len(sample1), len(sample2))

    R = 0

    small_sample = sample1 if len(sample1) < len(sample2) else sample2

    for d in small_sample:
      R += rank[d]

    z = (R-(n1*(n1+n2+1))/2)/(sqrt(n1*n2*(n1+n2+1)/12))

    if abs(z) < tab_value:
      print("Accept Null Hypothesis")
    else:
      print("Reject Null Hypothesis")

def signed_rank_test(before_sample, after_sample, tab_value):
    def find_rank(data):
        freq = {}
        rank = {}

        for d in data:
            if d in freq.keys():
                freq[d] += 1
            else:
                freq[d] = 1
        data.sort()

        for i in range(len(data)):
            if data[i] not in rank.keys():
                rank[data[i]] = i + (freq[data[i]] + 1) / 2
        return rank

    D = [d[0] - d[1] for d in zip(before_sample, after_sample)]
    _D_ = [abs(d) for d in D]
    rank = find_rank(_D_)
    n = len(before_sample)
    neg_count = pos_count = 0
    for d in D:
      if d < 0:
        neg_count += rank[abs(d)]
      elif d > 0:
        pos_count += rank[abs(d)]
      else:
          n-=1

    Ws = min(pos_count,neg_count)
    if n<30:
        z = Ws
        if abs(z) > tab_value:
            print("Accept Null Hypothesis")
        else:
            print("Reject Null Hypothesis")
    else:
        z = (Ws-(n*(n+1)/4)/sqrt(n*(n+1)*(2*n+1)/24))
        if abs(z) < tab_value:
            print("Accept Null Hypothesis")
        else:
            print("Reject Null Hypothesis")
        
def goodness_of_fit(obs, exp, chi2_tab):
    chi2_cal = 0

    for i in range(0, len(obs)):
        chi2_cal += ((obs[i] - exp[i]) ** 2) / exp[i]
    
    if(chi2_cal <= chi2_tab):
        print("Accept Null Hypothesis")
    else:
        print("Reject Null Hypothesis")

def chi_2_test_table(table, chi2_tab):
    chi2_cal = 0
    row_sum = [sum(i) for i in table]
    col_sum = [sum(i) for i in zip(*table)]
    N = sum(row_sum)

    for row in range(len(table)):
        for i in range(len(table[row])):
            exp = row_sum[row] * col_sum[i] / N
            if (exp != 0):
                chi2_cal += ((table[row][i] - exp) ** 2) / exp

    if(chi2_cal <= chi2_tab):
        print("Accept Null Hypothesis")
    else:
        print("Reject Null Hypothesis")
    
data = pd.read_csv("purged_csv_file.csv")
index = data["index"].tolist()
date = data["Date"].tolist()
time = data["Time"].tolist()
gap = data["Global_active_power"].tolist()
grp = data["Global_reactive_power"].tolist()

vol = data["Voltage"].tolist()
vol = [float(i) for i in vol]

gint = data["Global_intensity"].tolist()
sub1 = data["Sub_metering_1"].tolist()
sub2 = data["Sub_metering_2"].tolist()
sub3 = data["Sub_metering_3"].tolist() 

sd_dic = {'gap' : sd(gap), 'grp' : sd(grp), 'vol' : sd(vol), 'gint' : sd(gint), 'sub1' : sd(sub1), 'sub2' : sd(sub2), 'sub3' : sd(sub3)}
mean_dic = {'gap' : mean(gap), 'grp' : mean(grp), 'vol' : mean(vol), 'gint' : mean(gint), 'sub1' : mean(sub1), 'sub2' : mean(sub2), 'sub3' : mean(sub3)}

# For Goodness of Fit test
# n = len(gint)
# exp = [mean(gint)] * n
# chi2_tab = chi2.ppf(0.95, n)
# goodness_of_fit(gint, exp, chi2_tab)

# n = len(sub1)
# chi2_tab = chi2.ppf(0.95, n)
# table = [None, None, None]
# table[0] = sub1
# table[1] = sub2
# table[2] = sub3
# chi_2_test_table(table, chi2_tab)

# z_tab = norm.ppf(1- .05/2)
# n = sample_size_single_mean(z_tab, sd_dic["vol"], 5)
# sample = simple_random_sampling(vol, n) 
# one_sample_z_test(sample, 240, z_tab)

n = 28
t_tab = t.ppf(1 - .05/2, n)
sample = simple_random_sampling(vol, n)
one_sample_t_test(sample, 280, t_tab)