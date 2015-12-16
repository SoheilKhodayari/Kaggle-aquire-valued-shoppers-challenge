########################################################################
#  Task:     This script generates appropriate features for the data.  #
#            reads the .CSV files chunk by chunk to tweak memory       #
#            limits and to gain speed.                                 #
#                                                                      #
#  Input: loction of dataset files                                     #
#  Output: shopper_data.csv                                            #
########################################################################


import datetime as dt
import os.path
import csv
import gc
import time

# ---- Breaks a CSV file (sorted by ID) into chunks ------ #
def split_by_id(fname):
    
    global shopper_dict
    
    dr = csv.DictReader( open(fname, 'rb') )
    row = dr.next()
    curr_id = row['id']
    
    output = []
    shopper_data = shopper_dict.get(curr_id, None)
    
    while True:
        row_id = row['id']
                    
        if row_id == curr_id:
            if shopper_data is not None:
                output.append(row)
        else:
            if shopper_data is not None:
                # Yield chunk
                yield (shopper_data, output)

                # Set up next chunk
                del output
                output = [row]

            curr_id = row_id
            shopper_data = shopper_dict.get(row_id, None)
            
        try:
            row = dr.next()
        except StopIteration:
            if shopper_data is not None:
                yield (shopper_data, output)
            break
        
def aggregate_history(data):
    # Extracts features at the shopper level, based on the shopper's transaction history
    levels = ['company', 'brand', 'category']

    shopper_data, transaction_history = data
    offer_date = dt.datetime.strptime( shopper_data['offerdate'] , '%Y-%m-%d').date()

    for row in transaction_history:
        date = row['date']
        trans_date = dt.datetime.strptime( date , '%Y-%m-%d').date()

            # Filter out transactions that are more than one year old or occurred after the offer date
        if (offer_date - trans_date).days < 365 and (offer_date - trans_date).days > 0:

            # ----- FEATURE EXTRACTION CODE GOES HERE -----#

            for lvl in levels:
                if row[lvl] == shopper_data[lvl] and offer_date != trans_date:
                    # Recency
                    recency = offer_date - trans_date
                    shopper_data[ lvl + '_recency' ] = min( shopper_data.get(lvl + '_recency', float('Inf')), recency.days)

                    # Frequency
                    shopper_data[ lvl + '_frequency' ] = shopper_data.get(lvl + '_frequency', 0) + 1

                    # Monetary
                    shopper_data[ lvl + '_monetary' ] = shopper_data.get(lvl + '_monetary', 0) + float(row['purchaseamount'])

                    # Quantity
                    shopper_data[ lvl + '_qty' ] = shopper_data.get(lvl +'_qty', 0) + float(row['purchasequantity'])*float(row['productsize'])
            
    # End FOR LOOP
    for lvl in levels:
        monetary  = shopper_data.get( lvl + '_monetary' , 0 )
        quantity  = shopper_data.get( lvl + '_qty'      , 0 )
        frequency = shopper_data.get( lvl + '_frequency', 0 )
        if monetary > 0 and quantity > 0 and frequency > 0:
            shopper_data[ lvl + '_avg_price'       ] = monetary/quantity
            shopper_data[ lvl + '_avg_basket_size' ] = quantity/frequency

    return shopper_data

if __name__ == '__main__':

    # ----- TWEAK PERFORMANCE HERE -----#
    num_process = 4
    chunksize = 512
    # ----------------------------------#
    
    start = time.clock()
    
    offer_fname = 'offers.csv'
    transaction_fname = 'reduced.csv'
    trainHistory_fname = 'trainHistory.csv'
    
    transactions = transaction_fname
    trainHistory = csv.DictReader( open(trainHistory_fname, 'rb') )
    offers = csv.DictReader( open(offer_fname, 'rb') )

    out_fname = 'workspace/shopper_data.csv'
    outfile = open(out_fname, 'wb')

    levels = ['company', 'brand', 'category']
    metrics = ['_recency','_frequency', '_monetary', '_qty', '_avg_price', '_avg_basket_size']
        
    # ----- Read in offers -----#
    offer_dict = {}
    for row in offers:
        offer_dict[row['offer']] = row

    # ----- Merge offers with shoppers -----#
    shopper_dict = {}
    for row in trainHistory:
        offer = offer_dict[row['offer']]
        shopper_dict[row['id']] = dict( row.items() + offer.items() )

    # ----- Extract features from transaction history -----#
    
    if num_process > 1:
        from multiprocessing import Pool
        p = Pool( num_process )
        out_arr = p.imap_unordered( aggregate_history , split_by_id(transactions) , chunksize = chunksize)
    else:
        out_arr = map( aggregate_history , split_by_id(transactions) )

    # ----- Write output -----#
    for row in out_arr:
        shopper_dict[row['id']] = row
    
    output = [y for (x,y) in shopper_dict.items()]
    levels = ['company', 'brand', 'category']
    header = list(set(output[0].keys()
                      + [lvl + metric
                         for lvl in levels
                         for metric in metrics]))
    dw = csv.DictWriter(outfile, fieldnames = header)
    dw.writeheader()
    dw.writerows(output)

    print 'Extraction complete. Elapsed time: %.2f' %(time.clock() - start)
        
        

         
