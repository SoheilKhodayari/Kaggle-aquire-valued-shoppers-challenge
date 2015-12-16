# -*- coding: UTF-8 -*-

###################################################################################
#  Task:     This script reduces the original transactions.csv file(around 22GB)  #
#            size to around 1.6GB with respect to other data set files.           #
#  Method:                                              			  #
#            rows from the transactions data which don’t have a category id or    #
#	     a company id which is on offer will be discared.                     #
#										  #										  #
#  Input: location of primary dataset as function arguments                       #
#  Output: creates a reduced transaction file                                     #
###################################################################################


def reduce_data(loc_offers, loc_transactions, loc_reduced):
  start = datetime.now()
  offers_cat = {}
  offers_co = {}
  
  for e, line in enumerate( open(loc_offers) ):
    offers_cat[ line.split(",")[1] ] = 1
    offers_co[ line.split(",")[3] ] = 1
    
  with open(loc_reduced, "wb") as outfile:
    
    #go through transactions file and reduce
    reduced = 0
    for e, line in enumerate( open(loc_transactions) ):
      if e == 0:
        outfile.write( line )
      else:
        #only write when if category in offers dict
        if line.split(",")[3] in offers_cat or line.split(",")[4] in offers_co:
          outfile.write( line )
          reduced += 1
          
      # show progress
      if e % 5000000 == 0:
        print e, reduced, datetime.now() - start
  print e, reduced, datetime.now() - start



