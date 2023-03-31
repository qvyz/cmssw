import FWCore.ParameterSet.Config as cms

def customisePhase2TTNoMC(process):
    process.L1TrackTrigger.replace(process.L1PromptExtendedHybridTracksWithAssociators, process.L1PromptExtendedHybridTracks)
    process.L1TrackTrigger.remove(process.TrackTriggerAssociatorClustersStubs)
    process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')

    return process

def addHcalTriggerPrimitives(process):
    process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')

    return process


def runGTemulator(process):

    process.load('L1Trigger.Phase2L1GT.l1tGTMenu_cfi')

    process.GToutput = cms.OutputModule("PoolOutputModule",
         outputCommands = cms.untracked.vstring('drop *',
        'keep *P2GT*_*_*_L1TEmulation',
        #'keep *_l1tGTProducer_*_L1TEmulation',
        #'keep *_l1tGTAlgoBlockProducer_*_L1TEmulation'
    ),
    fileName=cms.untracked.string("l1t_emulation.root")
    )

    process.pGToutput = cms.EndPath(process.GToutput) 

    return process


