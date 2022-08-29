import FWCore.ParameterSet.Config as cms
import L1Trigger.Phase2L1GT.Conditions as cond




def checkFilter(obj):
    knownConditions = [cond.SingleObjCond, cond.DoubleObjCond]
    Condit = None
    for Condition in knownConditions:
        try:
            if obj.type_() == Condition.Label:
                Condit = Condition()
        except:
            pass
    

    if Condit == None:
        return 0
    knowncuts = Condit.getPossibleCuts()
    for knowncut in knowncuts:
        if obj.hasParameter(knowncut):
            Condit.setCut(knowncut,obj.getParameter(knowncut).value())
    for Collection in Condit._InputTags:
        param = obj.getParameter(Collection)
        Condit._setInputObject(Collection,param.productInstanceLabel)
    return Condit



def assignAlgoBits(obj,name):
    Algobitlist = obj.analyzers[name].channelConfig.value().pop().getParameter('algoBits')
    algos = cond.DefineAlgoBits()
    for Bititem in Algobitlist:
        name = Bititem.bitPos.value()
        value = Bititem.path.value()
        algos.SetBit(value,name)
    return algos




def getConditionsfromConfig(obj):
    filterlist = []
    for key,value in  obj.filters.items():
        x = checkFilter(value)
        if x != 0:
            x.setName(key)
            x.setPath(findPaths(obj,key))
            filterlist.append(x)
    return filterlist

def findPaths(obj,modulename):
    pathlist = []
    for path in obj.paths.values():
        if modulename in path.moduleNames():
            pathlist.append(path.label())
            print(path.label())
    return pathlist


def getModulesfromPath(gt,algobits):
    modules = {}
    for key,value in algobits.Assignment.items():
        print(key)
        modules[key] = gt.paths[key].moduleNames()
    return modules


def checkiflogicalcombination(filterlist,algobits):
    filterpaths =  [path for filt in filterlist for path in filt.Path]
    print(filterpaths)
    combinatorialpath = []
    for algopath in algobits.keys():     
        if algopath not in filterpaths:
            combinatorialpath.append(algopath)
    return combinatorialpath


def addcombinationalgobits(gt,combinatorialpath):
    combinatorialfilters = []
    for path in combinatorialpath:
        pathmodules = gt.paths[path].moduleNames()
        for module in pathmodules:
            if gt.filters[module].type_() == "PathStatusFilter":
                expression = gt.filters[module].getParameter("logicalExpression").value()
                containsmodules = getModules(gt,expression)
                print(containsmodules)
                combinatorialfilters.append(cond.LogicalFilter(expression,containsmodules))

    return combinatorialfilters
def getModules(obj,expression):
    words = expression.split()
    modulelist = []
    moduleset = {}
    for word in words:
        print(word)
        try:
            moduleset = (obj.paths[word].moduleNames())
        except:
            pass
        if moduleset != set():
            modulelist.append(moduleset.pop())
        if moduleset != set():
            print("warning %s is part of a combinatorial logic and its path contains more than 1 modules, this will lead to undefined behaviour".format(word))
        print(modulelist)
    return modulelist
            

