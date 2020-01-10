#nantong's osm data for the liu big result 
import osmium as osm
import pandas as pd
import numpy as np 

class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_data = []
        self.osm_node_raw = []
        self.osm_node_data  = []
        self.osm_way_data = []
        self.osm_way_raw = []
        self.osm_relation_data = []
        self.osm_relation_raw = []
        self.dict_way_id = dict()
        self.dict_node_id = dict()
        self.dict_relation_id = dict()
        

    def tag_inventory(self, elem, elem_type):
        data = dict()
        data['elem_type'] = elem_type 
        data['elem_id'] = elem.id
        data['elem_version'] = elem.version 
        data['timestemp'] = pd.Timestamp(elem.timestamp)
        data['elem_uid'] = elem.uid 
        data['elem_user'] = elem.user 
        data['elem_changeset'] = elem.changeset
        data['elem_tags'] = dict(elem.tags)
#         data['elem_location']= elem.location 
        if elem_type=='node':
            self.dict_node_id[elem.id] = len(self.osm_node_data) 
            self.osm_node_data.append(data)
#             self.osm_node_raw.append(elem)
           
        elif elem_type == 'way':
            self.dict_way_id[elem.id] = len(self.osm_way_data) 
            data['elem_nodes'] = [en.ref for en in list(elem.nodes)]
            self.osm_way_data.append(data)
#             self.osm_way_raw.append(elem)
        
        elif elem_type == 'relation':
#             print(elem)
            self.dict_relation_id[elem.id] = len(self.osm_relation_data) 
            data['elem_members'] = [ em.ref for em in  list(elem.members)]
            data['elem_members_type'] = [ em.type for em in list(elem.members)]
#             self.osm_relation_raw.append(elem)
            self.osm_relation_data.append(data) 
        
#         for tag in elem.tags:
            
#             data['elem_tag_s'] = tag
#             self.osm_data.append([elem_type, 
#                                    elem.id, 
# #                                    elem.lat,
# #                                    elem.lon,
#                                    elem.version,
#                                    pd.Timestamp(elem.timestamp),
#                                    elem.uid,
#                                    elem.user,
#                                    elem.changeset,
#                                    elem.tags,
#                                    tag.k,
#                                    tag.v])

    def node(self, n):
        self.tag_inventory(n, "node")

    def way(self, w):
        self.tag_inventory(w, "way")

    def relation(self, r):
        self.tag_inventory(r, "relation")
osmhandler = OSMHandler()
# scan the input file and fills the handler list accordingly
osmhandler.apply_file("./data/nantong.osm")
nodes = osmhandler.osm_node_data
ways = osmhandler.osm_way_data
relations = osmhandler.osm_relation_data

def get_node_index(idx):
    return osmhandler.dict_node_id[idx]
def get_way_index(idx):
    return osmhandler.dict_way_id[idx]
def get_trijectory(elem):
    ways_members = elem['elem_members']
    ways = []
    paths = []
    for wm in ways_members:
        print(wm)
        if  wm in osmhandler.dict_way_id :
#         print(osmhandler.dict_way_id.keys())
            way = osmhandler.osm_way_data[osmhandler.dict_way_id[wm]]
#             print(way)
            path = []
            for i in way['elem_nodes']:
                if i in osmhandler.dict_node_id:
#                     node = osmhandler.osm_node_data[osmhandler.dict_node_id[i]]
                    path.append(osmhandler.dict_node_id[i])
            paths.append(path)
    return paths
            

get_trijectory(relations[0])