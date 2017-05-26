import pandas as pd
import numpy as np
import csv
import re
from itertools import islice

nodes_tags="/Users/eyobe/Desktop/UDML/analysis/openstreet/nodes_tags.csv"
ways_tags="/Users/eyobe/Desktop/UDML/analysis/openstreet/ways_tags.csv"



"""THIS FUNCTION CLEANS AND EXTRACTS PROBLEMATIC ZIP CODES """
def clean_zip_code(z):
    validcode=[]
    invalidcode=[]
    for value in z:
         #  US zipcodes  are usually five digit and sometimes may may be written as xxxxx-yyyy where 
            #xs and ys are integers.
        if (len(value)<5) or (not value.split("-")[0].isdigit()):  
            invalidcode.append(value)
        #print value[0:2]
        elif value.split("-")[0].isdigit() and int(value[0:2])!=77: #Houston, Texas zip code
             invalidcode.append(value)
        else:
             validcode.append(value)
    return invalidcode,validcode

zip_keys=['postcode','postal_code','Zipcode' 'zip_right','zip_left_1','zip_left_2','zip_right_1','zip_left']
zip_codes=[]
with open (cleaned_nodetags,"r") as f:
    reader=csv.DictReader(f)
    #way_header=reader.fieldnames
      #No Need of Escaping lines in this case since everything is written in English
    for line in reader:
         if line['key'] in zip_keys: 
            zip_codes.append(line['value'])
            
clean_zip_code(zip_codes)
