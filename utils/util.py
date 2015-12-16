
#------------- Some helper functions are defined here--------------------# 

from datetime import datetime, date
def delta_days(date_string_one,date_string_two):
	date_format = "%Y-%m-%d"
	first = datetime.strptime(date_string_one, date_format)
	second = datetime.strptime(date_string_two, date_format)
	delta = second - first
	return delta.days

def func_mean(lst):
    return sum(lst) / float(len(lst))
    
    
def func_median(lst):
    even = (0 if len(lst) % 2 else 1) + 1
    half = (len(lst) - 1) // 2
    return sum(sorted(lst)[half:half + even]) / float(even)
