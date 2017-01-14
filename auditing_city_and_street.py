import pandas as pd
import numpy as np
import csv
import re
from itertools import islice

nodes_tags="/Users/eyobe/Desktop/UDML/analysis/openstreet/nodes_tags.csv"
ways_tags="/Users/eyobe/Desktop/UDML/analysis/openstreet/ways_tags.csv"

"""DICTIONARY THAT MAPS ABREVATED STREET NAMES INTO FULL NAME"""

street_mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Rd.": "Road",
            "Rd": "Road", "Pky":"Park way","Ct":"Court", "Dr.":"Drive","Dr":"Drive",
            "Blvd":"Boulevard","Fry":"Free way",'Fwy':"Free way",'Wy':"Way"
                        }

"""REGULAR EXPRESSION TO PICK OUT STREETS THAT END WITH THE APPREVATIONS IN street_mapping 
dictionary keys """

r= re.compile(r'St$|St.$|Rd$|Rd.$|Ave$|Ave.$|Pky$|Ct$|Dr.$|Dr$|Blvd$|Fry$|Fwy$|Wy$',re.I)

""" THIS FUNCTION CLEANS STREET NAMES"""

def clean_street(text,x): #x is dictionary
    #FUNCTION THAT TAKES A STRING AND A DICTIONARY X
            l=text.split()[-1] #TAKE THE LAST WORD OF THE STREET TO AVOID MISSMATCHING (eg,St,Ave,...etc)
            mm=r.search(text.split()[-1])
            if mm is None: 
                return text
            if mm is not None:
                mm=mm.group()
                m=mm
                if len(l)==len(m) and m in x.keys():  
              
                    text=text.replace(m,x[m],1) #replace once
                    return text
    
                elif len(l)==len(m) and m.capitalize() in x.keys(): #Considering lower case written strret types like st
                    #print m
                    text=text.replace(m,x[m.capitalize()],1)
                    return text 
                else:
                    return text
                
""" FUNCTION TO CLEAN CITY"""

def clean_city(city):
    city=city.split(",")
    city_with_state_country=city[0].capitalize()+','+'Texas'+','+'USA'
    return city_with_state_country



cleaned_node_tags=[]
with open (nodes_tags,"r") as f:
    reader=csv.DictReader(f)
    node_header=reader.fieldnames
    for i in range(5,55):
            l = reader.next() # Escaping field values written in other languages (Other than English)
            #print l
      
    for line in reader:#islice(reader, 51,None):
        
        #print line
        if line['key']=='street':  
            line['value']=clean_street(line['value'],street_mapping)
            cleaned_node_tags.append(line)
            #print line
        elif line['key']=='city':
            line['value']=clean_city(line['value'])
            #print line
            cleaned_node_tags.append(line)
        else:
            cleaned_node_tags.append(line)
            

            
cleaned_way_tags=[]

with open (ways_tags,"r") as f:
    reader=csv.DictReader(f)
    way_header=reader.fieldnames
      #No Need of Escaping lines in this case since everything is written in English
    for line in reader:
        
        #print line
        if line['key']=='street':  
            line['value']=clean_street(line['value'],street_mapping)
            cleaned_way_tags.append(line)
            #print line
        elif line['key']=='city':
            line['value']=clean_city(line['value'])
            #print line
            cleaned_way_tags.append(line)
        else:
            cleaned_way_tags.append(line)
            
"""WRITING THE CLEANED DATA IN TO A NEW FILE"""

with open('cleaned_nodetags.csv', 'w') as g: #print type(row["user"])
    writer = csv.DictWriter(g,node_header)
    writer.writeheader()
    for r in cleaned_node_tags:
        #print r
        writer.writerow(r) 
        
with open('cleaned_waytags.csv', 'w') as wg: #print type(row["user"])
    writer = csv.DictWriter(wg,way_header)
    writer.writeheader()
    for l in cleaned_way_tags:
        #print r
        writer.writerow(l)       
