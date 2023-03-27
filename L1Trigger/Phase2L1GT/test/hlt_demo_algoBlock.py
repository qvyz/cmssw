import FWCore.ParameterSet.Config as cms

#from Configuration.Eras.Era_Phase2_cff import Phase2

#process = cms.Process('L1TEmulation', Phase2)

from Configuration.Eras.Era_Phase2C17I13M9_cff import Phase2C17I13M9

process = cms.Process('L1',Phase2C17I13M9)


############################################################
# import standard configurations
############################################################


process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag

process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.INFO.limit = cms.untracked.int32(0)  # default: 0

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

############################################################
# Source
############################################################

process.source = cms.Source("PoolSource",
                            fileNames=cms.untracked.vstring(
                                '/store/mc/Phase2Fall22DRMiniAOD/MinBias_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30007/017df0e0-4fae-4f31-aae6-2c4915423b0c.root',
                            ),
                            inputCommands = cms.untracked.vstring("keep *","drop l1tTkPrimaryVertexs_L1TkPrimaryVertex_*_*")
)

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(30))


############################################################
# Upstream Emulators
############################################################

process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff') # needed to read HCal TPs

process.load('L1Trigger.TrackTrigger.TrackTrigger_cff')
process.load("L1Trigger.TrackFindingTracklet.L1HybridEmulationTracks_cff") 
process.load("L1Trigger.TrackerDTC.ProducerES_cff") 
process.load("L1Trigger.TrackerDTC.ProducerED_cff")

process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')

process.raw2digi_step = cms.Path(process.RawToDigi)
#process.L1TrackTrigger_step = cms.Path(process.L1TrackTrigger)
process.L1simulation_step = cms.Path(process.SimL1Emulator)

#process.UpstreamEmulators = cms.Path(
#    process.RawToDigi,
#    process.SimL1Emulator
#)
 
#process.pUpstreamEmulators = cms.Path(process.UpstreamEmulators)

	
#process.UpstreamEmulators = cms.Task(
#    process.TrackerDTCProducer,
#    process.TTClustersFromPhase2TrackerDigis,
#    process.TTStubsFromPhase2TrackerDigis,
#    process.offlineBeamSpot,
#    process.l1tTTTracksFromTrackletEmulation,
#    process.l1tTTTracksFromExtendedTrackletEmulation,
    #process.L1simulation_step #SimL1EmulatorTask
#)
 
#process.pUpstreamEmulators = cms.Path(process.UpstreamEmulators)

############################################################
# L1 Global Trigger Emulation
############################################################

# Conditions
from L1Trigger.Phase2L1GT.l1tGTSingleObjectCond_cfi import l1tGTSingleObjectCond
from L1Trigger.Phase2L1GT.l1tGTDoubleObjectCond_cfi import l1tGTDoubleObjectCond
from L1Trigger.Phase2L1GT.l1tGTTripleObjectCond_cfi import l1tGTTripleObjectCond
from L1Trigger.Phase2L1GT.l1tGTQuadObjectCond_cfi import l1tGTQuadObjectCond

from L1Trigger.Phase2L1GT.l1tGTAlgoBlockProducer_cff import algorithms

####### SEED 1 ###########

process.SingleTkMuon22 = l1tGTSingleObjectCond.clone(
    tag =  cms.InputTag("l1tGTProducer", "GMTTkMuons"),
    minPt = cms.double(2),
    minEta = cms.double(-2.4),
    maxEta = cms.double(2.4)
)
process.pSingleTkMuon22 = cms.Path(process.SingleTkMuon22)
algorithms.append(cms.PSet(expression = cms.string("pSingleTkMuon22")))

from L1Trigger.Phase2L1GT.l1tGTAlgoBlockProducer_cff import *
process.p2gtAlgoBlock = l1tGTAlgoBlockProducer.clone(
    algorithms = algorithms
) 

process.pp2gtAlgoBlock = cms.Path(process.p2gtAlgoBlock)


############################################################
# Analyzable output
############################################################

process.out = cms.OutputModule("PoolOutputModule",
outputCommands = cms.untracked.vstring('drop *',
        'keep *_l1tGTProducer_*_L1TEmulation',
        'keep l1tP2GTCandidatesl1tP2GTCandidatel1tP2GTCandidatesl1tP2GTCandidateedmrefhelperFindUsingAdvanceedmRefs_*_*_L1TEmulation',
        'keep *_l1tGTAlgoBlockProducer_*_L1TEmulation',
        'keep *_TriggerResults_*_L1TEmulation'
    ),
    fileName=cms.untracked.string("l1t_emulation.root")
)

process.pOut = cms.EndPath(process.out)

#process.schedule = cms.Schedule(process.raw2digi_step,process.L1simulation_step,process.pSingleTkMuon22,process.pp2gtAlgoBlock,process.pOut)
	

