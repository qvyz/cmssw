import FWCore.ParameterSet.Config as cms
############################################################
# L1 Global Trigger Emulation
############################################################

# Conditions
from L1Trigger.Phase2L1GT.l1tGTProducer_cff import *
from L1Trigger.Phase2L1GT.l1tGTSingleObjectCond_cfi import l1tGTSingleObjectCond
from L1Trigger.Phase2L1GT.l1tGTDoubleObjectCond_cfi import l1tGTDoubleObjectCond
from L1Trigger.Phase2L1GT.l1tGTTripleObjectCond_cfi import l1tGTTripleObjectCond
from L1Trigger.Phase2L1GT.l1tGTQuadObjectCond_cfi import l1tGTQuadObjectCond
from L1Trigger.Phase2L1GT.l1tGTQuadObjectCond_cfi import l1tGTQuadObjectCond

from L1Trigger.Phase2L1GT.l1tGTAlgoBlockProducer_cff import * # algorithms

####### SEED 1 ###########


SingleTkMuon22 = l1tGTSingleObjectCond.clone(
    tag =  cms.InputTag("L1GTProducer", "GMTTkMuons"),
    minPt = cms.double(22),
    minEta = cms.double(-2.4),
    maxEta = cms.double(2.4)
)
pSingleTkMuon22 = cms.Path(SingleTkMuon22)
algorithms.append(cms.PSet(expression = cms.string("pSingleTkMuon22")))

####### ALGOBLOCK ###########

p2gtAlgoBlock = l1tGTAlgoBlockProducer.clone(
    algorithms = algorithms
) 


menuTask = cms.Path(l1tGTProducer*p2gtAlgoBlock)
