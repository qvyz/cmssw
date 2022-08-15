import argparse

import ROOT
import L1Trigger.Phase2L1GT.l1GTScales as scales

from DataFormats.FWLite import Events, Handle


def get_pathfilters(event, procname):

    if not hasattr(ROOT, "getPathNames"):
        ROOT.gInterpreter.Declare("""
#include "FWCore/ParameterSet/interface/ParameterSet.h"
std::vector<std::string> getPathNames(edm::ParameterSet& pset){
   const auto& pathPSet = pset.getParameterSet("@trigger_paths");
   if(pathPSet.exists("@trigger_paths")){
     return pathPSet.getParameter<std::vector<std::string>>("@trigger_paths");
   }else{
     return std::vector<std::string>();
   }
}
                """)

    if not hasattr(ROOT, "getFiltModules"):
        ROOT.gInterpreter.Declare("""
#include "FWCore/ParameterSet/interface/ParameterSet.h"
std::vector<std::string> getFiltModules(edm::ParameterSet& pset,const std::string& pathName){
   std::vector<std::string> filtMods;
   const auto& pathPSet = pset.getParameterSet("@trigger_paths");
   if(pset.existsAs<std::vector<std::string> >(pathName,true)){
     const auto& modules = pset.getParameter<std::vector<std::string>>(pathName);
     for(const auto& mod : modules){
        //ignored modules will start with - and this needs to be removed if present            
        if(pset.exists(mod.front()!=std::string("-") ? mod : mod.substr(1))){
           const auto& modPSet = pset.getParameterSet(mod.front()!=std::string("-") ? mod : mod.substr(1));
           if(modPSet.getParameter<std::string>("@module_edm_type")=="EDFilter") {
             if (modPSet.getParameter<std::string>("@module_type") == "L1GTDoubleObjectCond") {
               filtMods.push_back(mod + "::" + modPSet.getParameter<edm::InputTag>("col1Tag").instance());
               if (modPSet.getParameter<edm::InputTag>("col1Tag").instance() != modPSet.getParameter<edm::InputTag>("col2Tag").instance()) {
                 filtMods.push_back(mod + "::" + modPSet.getParameter<edm::InputTag>("col2Tag").instance());
               }
             }
             else if (modPSet.getParameter<std::string>("@module_type") == "L1GTSingleObjectCond"){
               filtMods.push_back(mod + "::" + modPSet.getParameter<edm::InputTag>("colTag").instance());
             }
           }
        }
     }
   }
   return filtMods;
}
                """)

    cfg = ROOT.edm.ProcessConfiguration()
    proc_hist = event.object().processHistory()
    proc_hist.getConfigurationForProcess(procname, cfg)
    cfg_pset = event.object().parameterSet(cfg.parameterSetID())
    pathnames = ROOT.getPathNames(cfg_pset)
    path_filters = {}
    for path in pathnames:
        path_filters[str(path)] = [str(filt) for filt in ROOT.getFiltModules(cfg_pset, path)]

    return {path: modules for path, modules in path_filters.items() if len(modules) > 0}, pathnames


class TrigResults:
    """
    class acts as a name cache to allow the trigger results to be accessed
    by trigger name

    it takes as input the list of specific triggers to look for rather than 
    reading all possible triggers
    """

    def __init__(self, trigs, process, pathnames):
        self.process = process
        self.trig_indices = {x: [] for x in trigs}
        self.trig_res = {x: False for x in trigs}
        self._set_trig_indices(pathnames)

    def _set_trig_indices(self, pathNames):
        for name in self.trig_indices:
            self.trig_indices[name] = []

        for idx, trig_name in enumerate(pathNames):
            if str(trig_name) in self.trig_indices:
                self.trig_indices[str(trig_name)].append(idx)

    def _fill_trig_res(self, trig_res):
        for trig in self.trig_res:
            self.trig_res[str(trig)] = False  # resetting it
            for idx in self.trig_indices[str(trig)]:
                if trig_res[idx].accept():
                    self.trig_res[str(trig)] = True
                    break

    def fill(self, event):
        handle = Handle("edm::TriggerResults")
        event.getByLabel("TriggerResults", "", self.process, handle)
        self._fill_trig_res(handle.product())

    def result(self, trig):
        if trig in self.trig_res:
            return self.trig_res[trig]
        else:
            return False

def writeBoardData(config, fileNames, process):
    events = Events(fileNames)

    l1_res = None
    for event in events:

        if l1_res == None:
            path_filters, pathnames = get_pathfilters(event, process)
            l1_res = TrigResults(path_filters.keys(), process, pathnames)

        l1_res.fill(event)

        for path, filters in path_filters.items():
            # TODO
            pass
