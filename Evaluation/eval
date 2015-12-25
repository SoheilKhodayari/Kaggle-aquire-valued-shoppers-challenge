 
# -------------- This is the main file for evaluation after running two previous scripts --------------- #

def evaluate(filePointer,cutOff):
        tp=0
        fp=0
        tn=0
        fn=0

        cnt=0
        for line in filePointer.readlines():
            if cnt==0:
                    cnt+=1
                    continue
            linee = line.split(",")
            actual = linee[2].strip()
            pred = linee[1]
            if eval(pred) > cutOff :
                if str(actual)=='t':
                        tp+=1
                elif str(actual)=='f':
                        fp+=1

            else:
                if str(actual)=='t':
                        fn+=1
                elif str(actual)=='f':
                        tn+=1
        return (tp,fp,tn,fn)

def precision(tp,fp,tn,fn):
        return tp/float(tp+fp)

def recall(tp,fp,tn,fn):
        return tp/float(tp+fn)

def trueNegRate(tp,fp,tn,fn):
        return tn/float(tn+fp)

def accuracy(tp,fp,tn,fn):
        return (tp+tn)/float(tp+tn+fp+fn)

def fscore(precision,recall):
        return 2*precision*recall/float(precision+recall)

def avg(s,length):
        return s/float(length)
        
def AverageCutoff():
        
        p=0
        lp=0
        r=0
        lr=0
        t=0
        lt=0
        a=0
        la=0
        s=0
        ls=0
        for i in range(99):
                f=open('submission.csv','r') # res.csv generated before
                cutoff=eval('0.0{0}'.format(i+1))
                tp,fp,tn,fn=evaluate(f,cutoff)

                PREC=precision(tp,fp,tn,fn)
                RECAL=recall(tp,fp,tn,fn)
                TrueNeg=trueNegRate(tp,fp,tn,fn)
                ACC=accuracy(tp,fp,tn,fn)
                FSCOR=fscore(PREC,RECAL)

                p+=PREC
                lp+=1
                r+=RECAL
                lr+=1
                t+=TrueNeg
                lt+=1
                a+=ACC
                la+=1
                s+=FSCOR
                ls+=1
                f.close()

        print "{0}\t {1}\t {2}\t {3}\t {4}\n".format(avg(p,lp),avg(r,lr),avg(t,lt),avg(a,la),avg(s,ls))
        
def avg_sample_cutoff():
        
        iterator=0
        p=0
        r=0
        t=0
        a=0
        s=0
        while(iterator<3):
                f=open('submission.csv','r') #res.csv generated before
                if iterator==0:
                        cutoff=0.25
                elif iterator==1:
                        cutoff=0.5
                else:
                        cutoff=0.75
                iterator+=1
                tp,fp,tn,fn=evaluate(f,cutoff)
                print(tp,fp,tn,fn)
                PREC=precision(tp,fp,tn,fn)
                RECAL=recall(tp,fp,tn,fn)
                TrueNeg=trueNegRate(tp,fp,tn,fn)
                ACC=accuracy(tp,fp,tn,fn)
                FSCOR=fscore(PREC,RECAL)
                p+=PREC
                r+=RECAL
                t+=TrueNeg
                a+=ACC
                s+=FSCOR
                f.close()
        print "{0}\t {1}\t {2}\t {3}\t {4}\n".format(avg(p,3),avg(r,3),avg(t,3),avg(a,3),avg(s,3))
        
def AUC():
  try:
	    import numpy as np
	    from sklearn.metrics import roc_auc_score
	except:
	    raise ImportError("need numpy and sklearn modules installed")

	list_actual=list()
	list_pred=list()

	f=open("submission.csv","r")

	for line in f.readlines():
		if line[2].strip() =='t':
			actual=1
		else:
			actual=0
		pred=float(line[1])

		list_actual.append(actual)
		list_pred.append(pred)

	y_scores = np.array(list_pred)
	y_true =  np.array(list_actual)

	auc_fscore = roc_auc_score(y_true, y_scores)

	print "AUC Score:{0}".format(auc_fscore)

