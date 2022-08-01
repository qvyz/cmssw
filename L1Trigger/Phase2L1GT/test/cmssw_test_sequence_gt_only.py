import FWCore.ParameterSet.Config as cms

process = cms.Process('L1Test')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic50ns13TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


# Input source
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(100))


process.GTProducer = cms.EDProducer(
    "L1GTTestProducer",
    outputFilename=cms.string("inputPattern"),
    random_seed=cms.uint32(0),
    platform=cms.string("VU9P")
)

process.l1t_GTProducer = cms.Path(process.GTProducer)

from L1Trigger.Phase2L1GT.l1GTSingleInOutLUT import COSH_ETA_LUT, COS_PHI_LUT

COSH_ETA_LUT.export("coshEtaLUT.mem")
COS_PHI_LUT.export("cosPhiLUT.mem")

from L1Trigger.Phase2L1GT.l1GTSingleObjectCond_cfi import l1GTSingleObjectCond
from L1Trigger.Phase2L1GT.l1GTDoubleObjectCond_cfi import l1GTDoubleObjectCond
from L1Trigger.Phase2L1GT.l1GTTripleObjectCond_cfi import l1GTTripleObjectCond
from L1Trigger.Phase2L1GT.l1GTQuadObjectCond_cfi import l1GTQuadObjectCond

l1GTDoubleObjectCond.sanity_checks = cms.untracked.bool(True)

# Conditions
process.singleTkEle12 = l1GTSingleObjectCond.clone(
    colTag = cms.InputTag("GTProducer", "CL2 Electrons"),
    pt_cut = cms.double(12),
)

process.doubleTkEle11TkPho11 = l1GTDoubleObjectCond.clone(
    col1Tag = cms.InputTag("GTProducer", "CL2 Electrons"),
    col2Tag = cms.InputTag("GTProducer", "CL2 Photons"),
    pt1_cut = cms.double(11),
    pt2_cut = cms.double(11)
)

process.tripleTkEle20TkPho18Jet11 = l1GTTripleObjectCond.clone(
    col1Tag = cms.InputTag("GTProducer", "CL2 Electrons"),
    col2Tag = cms.InputTag("GTProducer", "CL2 Photons"),
    col3Tag = cms.InputTag("GTProducer", "CL2 Jets"),
    pt1_cut = cms.double(20),
    pt2_cut = cms.double(18),
    pt3_cut = cms.double(11),
)

process.quadTkEle20 = l1GTQuadObjectCond.clone(
    col1Tag = cms.InputTag("GTProducer", "CL2 Electrons"),
    col2Tag = cms.InputTag("GTProducer", "CL2 Electrons"),
    col3Tag = cms.InputTag("GTProducer", "CL2 Electrons"),
    col4Tag = cms.InputTag("GTProducer", "CL2 Electrons"),
    pt1_cut = cms.double(20),
    pt2_cut = cms.double(20),
    pt3_cut = cms.double(20),
    pt4_cut = cms.double(20),
)

process.l1t_singleTkEle12 = cms.Path(process.singleTkEle12)
process.l1t_doubleTkEle11TkPho11 = cms.Path(process.doubleTkEle11TkPho11)
process.l1t_tripleTkEle20TkPho18Jet11 = cms.Path(process.tripleTkEle20TkPho18Jet11)
process.l1t_quadTkEle20 = cms.Path(process.quadTkEle20)


# Algo bits
from L1Trigger.Phase2L1GT.l1GTAlgoChannelConfig import generate_channel_config 

process.BoardData = cms.EDAnalyzer("L1GTBoardWriter",
  outputFilename = cms.string("outputPattern"),
  channelConfig = generate_channel_config({
        9 : {0: "l1t_tripleTkEle20TkPho18Jet11", 2 : "l1t_singleTkEle12", 3: "l1t_quadTkEle20", 65 : "l1t_doubleTkEle11TkPho11"}
    })
)

process.l1t_BoardData = cms.EndPath(process.BoardData)
