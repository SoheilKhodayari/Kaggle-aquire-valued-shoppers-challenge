########################################################################
#  Task:     This script generates a Kaggle submission file            #
#            from the created VW predictions.                          #
#                                                                      #
#  Input: vowpal wabbit .vw prediction file                            #
#  Output: a submission file                                           #
########################################################################


loc_predictions = "workspace/predictions.txt"
loc_testHistory = "testHistory.csv"
loc_submission = "submission.csv"


def generate_submission(loc_predictions, loc_testHistory, loc_submission):
	preds = {}
	for e, line in enumerate( open(loc_predictions) ):
		row = line.strip().split(" ")
		# row[0]=repeatProb, row[1]=id
		preds[ row[1] ] = row[0]
		
	
	with open(loc_submission, "wb") as outfile:
		for e, line in enumerate( open(loc_testHistory) ):
			if e == 0:
				outfile.write( "id,repeatProbability\n" )
			else:
				row = line.strip().split(",")
				if row[0] not in preds:
					outfile.write(row[0]+",0\n")
				else:
					outfile.write(row[0]+","+preds[row[0]]+"\n")
					

if __name__ == '__main__':
	generate_submission(loc_predictions, loc_testHistory, loc_submission)
