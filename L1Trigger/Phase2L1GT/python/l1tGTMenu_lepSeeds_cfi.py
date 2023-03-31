import FWCore.ParameterSet.Config as cms

############################################################
# L1 Global Trigger Emulation
############################################################

# Conditions

from L1Trigger.Phase2L1GT.l1tGTProducer_cff import l1tGTProducer

from L1Trigger.Phase2L1GT.l1tGTSingleObjectCond_cfi import l1tGTSingleObjectCond
from L1Trigger.Phase2L1GT.l1tGTDoubleObjectCond_cfi import l1tGTDoubleObjectCond
from L1Trigger.Phase2L1GT.l1tGTTripleObjectCond_cfi import l1tGTTripleObjectCond
from L1Trigger.Phase2L1GT.l1tGTQuadObjectCond_cfi import l1tGTQuadObjectCond

from L1Trigger.Phase2L1GT.l1tGTAlgoBlockProducer_cff import algorithms

####### MUON SEEDS ###########

SingleTkMuon22 = l1tGTSingleObjectCond.clone(
    tag =  cms.InputTag("l1tGTProducer", "GMTTkMuons"),
    minPt = cms.double(20),
    minEta = cms.double(-2.4),
    maxEta = cms.double(2.4)
)
pSingleTkMuon22 = cms.Path(SingleTkMuon22)
algorithms.append(cms.PSet(expression = cms.string("pSingleTkMuon22")))

DoubleTkMuon157 = l1tGTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt = cms.double(14),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt = cms.double(6),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    maxDz = cms.double(1),
)
pDoubleTkMuon15_7 = cms.Path(DoubleTkMuon157)
algorithms.append(cms.PSet(expression = cms.string("pDoubleTkMuon15_7")))

TripleTkMuon533 = l1tGTTripleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt = cms.double(5),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt = cms.double(3),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    collection3 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt = cms.double(3),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    delta12 = cms.PSet(
        maxDz = cms.double(1)
    ),
    delta13 = cms.PSet(
        maxDz = cms.double(1)
    ),
    delta23 = cms.PSet(
        maxDz = cms.double(1)
    )
)
pTripleTkMuon5_3_3 = cms.Path(TripleTkMuon533)
algorithms.append(cms.PSet(expression = cms.string("pTripleTkMuon5_3_3")))

####### TK EG and PHO seeds ###########

SingleTkEle36 = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    minPt = cms.double(30),
    minEta = cms.double(-2.4),
    maxEta = cms.double(2.4)
)
pSingleTkEle36 = cms.Path(SingleTkEle36) #quality missing
algorithms.append(cms.PSet(expression = cms.string("pSingleTkEle36")))

SingleIsoTkEle28 = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
    minPt = cms.double(23),
    minEta = cms.double(-2.4),
    maxEta = cms.double(2.4)
)
pSingleIsoTkEle28 = cms.Path(SingleIsoTkEle28) #quality and isolation missing
algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkEle28")))

SingleIsoTkPho36 = l1tGTSingleObjectCond.clone(
    tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
    minPt = cms.double(23), #doublecheck
    minEta = cms.double(-2.4),
    maxEta = cms.double(2.4)
)
pSingleIsoTkPho36 = cms.Path(SingleIsoTkPho36) #quality and isolation missing
algorithms.append(cms.PSet(expression = cms.string("pSingleIsoTkPho36")))


DoubleTkIsoPho2212 = l1tGTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt = cms.double(21), #doublecheck
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt = cms.double(10),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    maxDz = cms.double(1),
)
#pDoubleTkIsoPho22_12 = cms.Path(DoubleTkIsoPho2212) #quality missing
#algorithms.append(cms.PSet(expression = cms.string("pDoubleTkIsoPho22_12")))


DoubleTkEle2512 = l1tGTDoubleObjectCond.clone(
    collection1 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt = cms.double(21),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    collection2 = cms.PSet(
        tag = cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt = cms.double(10),
        minEta = cms.double(-2.4),
        maxEta = cms.double(2.4)
    ),
    maxDz = cms.double(1),
)
pDoubleTkEle25_12 = cms.Path(DoubleTkEle2512) #quality missing
algorithms.append(cms.PSet(expression = cms.string("pDoubleTkEle25_12")))



