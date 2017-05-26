import csv
from itertools import islice

def node_cleaner(row): 
    row["id"]= int(row["id"])
    row["lat"]=float(row["lat"])
    row["lon"]=float(row["lon"])
    row["user"]=str(row["user"])                       
    row["uid"]=int(row["uid"])
    row["version"]=int(row["version"])
    row["changeset"]=int(row["changeset"])
    row["timestamp"]=str(row["timestamp"])
    return row 
def way_cleaner(row):
    row["version"]=str(row["version"])
    return row

nodes_file="nodes.csv"
rows=[]
with open(nodes_file, "r") as f:
        reader = csv.DictReader(f)
        header= reader.fieldnames
        #CHANGE THE FIELD values INTO PROPER DATA FORMATS IN A WAY CONSISTENT TO MY SQL TABLE'S SCHEMA 
        for row in islice(reader, 0, None):
            row=node_cleaner(row)
            rows.append(row)
with open('new_node.csv', 'w') as g: #print type(row["user"])
    writer = csv.DictWriter(g,header)
    writer.writeheader()
    for r in rows:
        #print r
        writer.writerow(r)   
way_file="ways.csv"
way_rows=[]
with open(way_file, "r") as f:
        reader = csv.DictReader(f)
        header= reader.fieldnames
        #CHANGE THE FIELD values INTO PROPER DATA FORMATS IN A WAY CONSISTENT TO MY SQL TABLE'S SCHEMA 
        
        for row in islice(reader, 0, None):
            row=way_cleaner(row)
            way_rows.append(row)
with open('new_way.csv', 'w') as g: #print type(row["user"])
    writer = csv.DictWriter(g,header)
    writer.writeheader()
    for r in way_rows:
        #print r
        writer.writerow(r)   