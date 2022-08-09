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



def assignAlgoBits(obj):
    Algobitlist = obj.channelConfig.value().pop().getParameter('algoBits')
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
            filterlist.append(x)
    return filterlist
