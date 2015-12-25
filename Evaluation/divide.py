

# ----------- This divides the Train Data to half, half for training and half for testing ------------ #

f=open('tr.csv','w')
g=open('ts.csv','w')

h=open('trainHistory.csv','r')
i=0
for line in h.readlines():
    if i==0:
        f.write(line)
        k=line.split(',')
        g.write(line)
    elif i>0:
        if i%2==0:
            f.write(line)
        else:
            k=line.split(',')
            g.write(line)
    i+=1

f.close()
g.close()
h.close()

# -------------------- NOTE ------------------------#
# After This file executed:
#     rename tr.csv to trainHistory
#     rename ts.csv to testHistory
# --------------------------------------------------#
