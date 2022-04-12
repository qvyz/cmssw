
import FWCore.ParameterSet.Config as cms
import json
from cmssw_marias_sequence_with_gt import process
from FWCore.ParameterSet.Modules import EDFilter
propathdict = process.paths
profiltdict = process.filters
moduleset = set()
filters = dict()

def get_dict_from_json(path):
    with open (path,'r') as f:
        data = json.load(f)
    x = data['Conditions']
    for key,value in x.items():
        conddict[key] = Condition_from_template(key,value)
        print(key)
    return conddict

def make_condobject_from_path(self,process):
    for key,value in process.pahts: #get names from individual modules
        moduleset |= (value.moduleNames())
        # print(value.directDepend
        # for modulename in moduleset:
        #     print(profiltdict[modulename].type_)
    for modulename in moduleset:
        if modulename in profiltdict:
            if profiltdict[modulename].type_() in conditionsdict:
                filters[modulename] = process.filters[modulename]

    return filters
# for key,value in profiltdict.items():




class Cut_from_template(object):
    def __init__(self,**kwargs):
        self.type = kwargs.get("type")
        self.bitwidth = kwargs.get("bitwidth")
        if(kwargs["value"]):
            self.value = kwargs.get("value")
        else: 
            self.value
       


class GT_menu(object):
    knownConditions = dict()
    Filterobjects = {EDFilter}
    def __init__(self):
        self.knownConditions = dict()
        self.Filterobjects =  dict()
        self.ToTemplate = dict()

    def set_knownConditions(self,path):
        """
        reads json given in path
        stores file in knownConditions
        """
        with open (path,'r') as f:
            data = json.load(f)
        x = data['Conditions']
        for key,value in x.items():
            self.knownConditions[key] = Condition_from_template(key,value)
   
   
   
    def get_filters_from_config(self,process):
        """
        reads config files and stores filters found in json config
        """
        process_paths = process.paths
        process_filters = process.filters
        moduleset = set()
        for key,value in process_paths.items(): #get names from individual modules
            moduleset |= (value.moduleNames())
        for modulename in moduleset:
            if modulename in process_filters:
                if profiltdict[modulename].type_() in self.knownConditions:
                    self.Filterobjects[modulename] = process.filters[modulename]

    # def write_template_object(self):
    #     for key,value in self.Filterobjects:




    # def write_template








class Condition_from_template(object):
    def __init__(self,label,values):
        self.label = label
        self.vhdl_template = values.pop("vhdl_template")
        self.vhdl_name = values.pop("vhdl_name") 
        self.Cuts = values.pop("Cuts")
        if(values):
            self.Additional = values
        




    # def set_Cuts_from_template()
    

