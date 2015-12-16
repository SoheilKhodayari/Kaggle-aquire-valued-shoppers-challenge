########################################################################
#  Task:     This script generates appropriate features for the data.  #
#	     It also calls a specific function so as to reduce the     #
#            dataset size.                                             #
#                                                                      #
#  Input: loction of dataset files                                     #
#  Output: reduced.csv,train.vw,test.vw                                #
########################################################################


#---------- Importing neccessary modules---------------#
from datetime import datetime, date
from collections import defaultdict
from utils.util import delta_days
from utils.reduceDate import reduce_data
from utils.classes import *
import sys
import time
#------------------------------------------------------#


#---------- Specifing dataset locations ---------------#
loc_offers = "offers.csv"
loc_transactions = "transactions.csv"
loc_train = "trainHistory.csv"
loc_test = "testHistory.csv"
#------------------------------------------------------#


#---------- Specifing output locations ----------------#
loc_reduced = "workspace/reduced.csv" 
loc_out_train = "workspace/train.vw"
loc_out_test = "workspace/test.vw"
#------------------------------------------------------#


# -- Joins two lists of tuples (or namedtuples) on a key field. ----------------------- #

def inner_join(lot0, lot1, key0=None, key1=None, sort=True):
        
    d1 = {key1(r): r for r in lot1}
    result = []
    for e in lot0:
        k = key0(e)
        if k in d1:
            result.append((e, d1[k]))
    return result

def join_history_and_offer():
        
        offers = Offer.get_offers(sys.maxint)
        train_histories = History.getHistories(sys.maxint)

        file = open('workspace/joinedTrainHistory.csv', 'w')

        for history, offer in inner_join(train_histories, offers, lambda offer: offer.offer, lambda history: history.offer, False):
            out = history.user + ',' + offer.company + ',' + offer.category + ',' + offer.brand.strip() 
            out += (',' + history.chain + ',' + history.market + ',' + history.repeattrips + ',' + history.repeater)
            out += (',' + history.offerdate.strip() + ',' + offer.quantity + ',' + offer.offervalue + '\n')
            file.write(out)
        file.close()
        
#----------------------------------------------------------------------------------------#

def generate_features(loc_train, loc_test, loc_transactions, loc_out_train, loc_out_test):
        #--- keep offer data in offers associative array ---#
	offers = {}
	for e, line in enumerate( open(loc_offers) ):
		row = line.strip().split(",")
		offers[ row[0] ] = row

	#--- dicts for keeping test and train rows with the shopper id as their key ---#
	train_ids = {}
	test_ids = {}
	for e, line in enumerate( open(loc_train) ):
		if e > 0:
			row = line.strip().split(",")
			#--- let the shopper id be dict key ---#
			train_ids[row[0]] = row
	for e, line in enumerate( open(loc_test) ):
		if e > 0:
			row = line.strip().split(",")
			#--- let the shopper id be dict key ---#
			test_ids[row[0]] = row
			
	with open(loc_out_train, "wb") as out_train, open(loc_out_test, "wb") as out_test:
		last_id = 0
		features = defaultdict(float)
		#--- iterate through transactions ---# 
		for e, line in enumerate( open(loc_transactions) ):
                        #--- skiping file header ---#
			if e > 0: 
				row = line.strip().split(",")
				#--- if we get to a new shopper id then fill the feature dicts ---#
				if last_id != row[0] and e != 1:
					
					#--- generate negative features ---#
					if "has_bought_company" not in features:
						features['never_bought_company'] = 1
					
					if "has_bought_category" not in features:
						features['never_bought_category'] = 1
						
					if "has_bought_brand" not in features:
						features['never_bought_brand'] = 1
						
					if "has_bought_brand" in features and "has_bought_category" in features and "has_bought_company" in features:
						features['has_bought_brand_company_category'] = 1
					
					if "has_bought_brand" in features and "has_bought_category" in features:
						features['has_bought_brand_category'] = 1
					
					if "has_bought_brand" in features and "has_bought_company" in features:
						features['has_bought_brand_company'] = 1
						
					outline = ""
					test = False
					for k, v in features.items():
						
						if k == "label" and v == 0.5:
							outline = "1 '" + last_id + " |f" + outline
							test = True
						elif k == "label":
							outline = str(v) + " '" + last_id + " |f" + outline
						else:
							outline += " " + k+":"+str(v) 
					outline += "\n"
					if test:
						out_test.write( outline )
					else:
						out_train.write( outline )
						
					features = defaultdict(float)
				if row[0] in train_ids or row[0] in test_ids:
					if row[0] in train_ids:
						history = train_ids[row[0]]
						if train_ids[row[0]][5] == "t":
							features['label'] = 1
						else:
							features['label'] = 0
					else:
						history = test_ids[row[0]]
						features['label'] = 0.5
						
					
					features['offer_value'] = offers[ history[2] ][4]
					features['offer_quantity'] = offers[ history[2] ][2]
					offervalue = offers[ history[2] ][4]
					
					features['total_spend'] += float( row[10] )
					
					if offers[ history[2] ][3] == row[4]:
						features['has_bought_company'] += 1.0
						features['has_bought_company_q'] += float( row[9] )
						features['has_bought_company_a'] += float( row[10] )
						
						date_delta_days = delta_days(row[6],history[-1])
						if date_delta_days < 30:
							features['has_bought_company_30'] += 1.0
							features['has_bought_company_q_30'] += float( row[9] )
							features['has_bought_company_a_30'] += float( row[10] )
						if date_delta_days < 60:
							features['has_bought_company_60'] += 1.0
							features['has_bought_company_q_60'] += float( row[9] )
							features['has_bought_company_a_60'] += float( row[10] )
						if date_delta_days < 90:
							features['has_bought_company_90'] += 1.0
							features['has_bought_company_q_90'] += float( row[9] )
							features['has_bought_company_a_90'] += float( row[10] )
						if date_delta_days < 180:
							features['has_bought_company_180'] += 1.0
							features['has_bought_company_q_180'] += float( row[9] )
							features['has_bought_company_a_180'] += float( row[10] )
					
					if offers[ history[2] ][1] == row[3]:
						
						features['has_bought_category'] += 1.0
						features['has_bought_category_q'] += float( row[9] )
						features['has_bought_category_a'] += float( row[10] )
						date_delta_days = delta_days(row[6],history[-1])
						if date_delta_days < 30:
							features['has_bought_category_30'] += 1.0
							features['has_bought_category_q_30'] += float( row[9] )
							features['has_bought_category_a_30'] += float( row[10] )
						if date_delta_days < 60:
							features['has_bought_category_60'] += 1.0
							features['has_bought_category_q_60'] += float( row[9] )
							features['has_bought_category_a_60'] += float( row[10] )
						if date_delta_days < 90:
							features['has_bought_category_90'] += 1.0
							features['has_bought_category_q_90'] += float( row[9] )
							features['has_bought_category_a_90'] += float( row[10] )						
						if date_delta_days < 180:
							features['has_bought_category_180'] += 1.0
							features['has_bought_category_q_180'] += float( row[9] )
							features['has_bought_category_a_180'] += float( row[10] )				
					if offers[ history[2] ][5] == row[5]:
						features['has_bought_brand'] += 1.0
						features['has_bought_brand_q'] += float( row[9] )
						features['has_bought_brand_a'] += float( row[10] )
						date_delta_days = delta_days(row[6],history[-1])
						if date_delta_days < 30:
							features['has_bought_brand_30'] += 1.0
							features['has_bought_brand_q_30'] += float( row[9] )
							features['has_bought_brand_a_30'] += float( row[10] )
						if date_delta_days < 60:
							features['has_bought_brand_60'] += 1.0
							features['has_bought_brand_q_60'] += float( row[9] )
							features['has_bought_brand_a_60'] += float( row[10] )
						if date_delta_days < 90:
							features['has_bought_brand_90'] += 1.0
							features['has_bought_brand_q_90'] += float( row[9] )
							features['has_bought_brand_a_90'] += float( row[10] )						
						if date_delta_days < 180:
							features['has_bought_brand_180'] += 1.0
							features['has_bought_brand_q_180'] += float( row[9] )
							features['has_bought_brand_a_180'] += float( row[10] )	
				last_id = row[0]
				if e % 100000 == 0:
					print e
					


if __name__ == '__main__':

	# --- comment out below 3 lines if you already have reduced.csv --------------- #
	start = time.clock()
	reduce_data(loc_offers, loc_transactions, loc_reduced)
	print 'Reduction complete. Elapsed time: %.2f' %(time.clock() - start)
	# ----------------------------------------------------------------------------- #

	# --- starting to generatefeatures  ------------------------------------------- #
	start = time.clock()
	generate_features(loc_train, loc_test, loc_reduced, loc_out_train, loc_out_test)
	print 'Extraction complete. Elapsed time: %.2f' %(time.clock() - start)
	# ----------------------------------------------------------------------------- #
