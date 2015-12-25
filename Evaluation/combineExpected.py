
# -------------- This file adds actual expected results to submission file -----------------#

f=open('submission.csv','r')
g=open('testHistory.csv','r') # ts.csv generated before

h=open('res.csv','w+')

lines=f.readlines()

i=0
for line in g.readlines():
        k=line.split(',')
        toWrite=k[5]
        h.write(lines[i][0:-1]+','+toWrite+'\n')
        i+=1
        
    
h.close()
f.close()
g.close()

#----------------- Note ---------------------#
# After this file executed:
#     rename res.csv to submission.csv 
#--------------------------------------------#
