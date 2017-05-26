import xml.etree.cElementTree as ET
import pprint
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH = "/Users/eyobe/Desktop/UDML/analysis/openstreet/houston.osm"

NODES_PATH = "test_nodes.csv"
NODE_TAGS_PATH = "test_nodes_tags.csv"
WAYS_PATH = "test_ways.csv"
WAY_NODES_PATH = "test_ways_nodes.csv"
WAY_TAGS_PATH = "test_ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)')
UPPER_COLON=re.compile(r'^([a-z]|_)+:([a-z]|_)+:([a-z]|_)+')

PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  
    way_tags=[]
    i=-1
      # Handle secondary tags the same way for both node and way elements
    #for _, element in ET.iterparse(filename):
        # YOUR CODE HERE
    if element.tag=='node': 
        node_attribs=element.attrib
        for key in node_attribs.keys():
            if key not in NODE_FIELDS:
                del(node_attribs[key])
            #print d
        for child in element:
            my_dict={}

            if child.tag=='tag':
                if PROBLEMCHARS.search(child.attrib['k']):
                    continue
                elif LOWER_COLON.search(child.attrib['k']):
                    tag_attr=child.attrib['k']
                    tag_attribute=tag_attr.split(":",1)
                    my_dict['id']=element.attrib['id']
                    my_dict['type']=tag_attribute[0]
                    #print my_dict['type']
                    my_dict['key']=tag_attribute[1]
                    my_dict['value']=child.attrib['v']
            
                else:
                    tag_attribute=child.attrib['k']
                    my_dict['id']=element.attrib['id']
                    my_dict['type']='regular'
                    #print my_dict['type']
                    my_dict['key']=tag_attribute
                    my_dict['value']=child.attrib['v']
            tags.append(my_dict)
        #print  {'node': node_attribs, 'node_tags': tags}         
        return {'node': node_attribs, 'node_tags': tags}
    #if element.tag == 'way':
    elif element.tag=='way': 
        way_attribs=element.attrib
        for key in way_attribs.keys():
            if key not in WAY_FIELDS:
                del(way_attribs[key])
            #print d
        for child in element:
            way_dict={}
            #nd_dict={}
            if child.tag=='tag': 
                
            #if child.tag=='tag'and element.attrib['id']=='209809850':
                if PROBLEMCHARS.search(child.attrib['k']):
                    continue
                elif LOWER_COLON.search(child.attrib['k']):
                    print "child.attrib['k']"
                    print child.attrib['k']
                    tag_attr=child.attrib['k']
                    #print 'tag_attr.group()'
                    #print tag_attr.group()
                    tag_attribute=tag_attr.split(":",1)
                    print 'tag_attribute'
                    print tag_attribute
                    way_dict['id']=element.attrib['id']
                    way_dict['type']=tag_attribute[0]
                        #print way_dict['type']
                    way_dict['key']=tag_attribute[1]
                    way_dict['value']=child.attrib['v']
                    way_tags.append(way_dict)
                else:
                    tag_attribute=child.attrib['k']
                    way_dict['id']=element.attrib['id']
                    way_dict['type']='regular'
                    #print my_dict['type']
                    way_dict['key']=tag_attribute
                    way_dict['value']=child.attrib['v']
                    way_tags.append(way_dict)
            #print way_tags
            nd_dict={}
            if child.tag=='nd':
                i=i+1
                nd_dict['id']=element.attrib['id']
                nd_dict['node_id']=child.attrib['ref']
                nd_dict['position']=i
                #position+=1
                #print nd_dict['position']
                way_nodes.append(nd_dict)  
            #else:
                #continue
        #way_tags.append(way_dict)
        print "Way-Tags="
        print way_tags
        #print tags
        #print way_nodes
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': way_tags}
    #else:
        #pass 

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
        codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)

