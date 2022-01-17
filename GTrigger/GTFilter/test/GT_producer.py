import FWCore.ParameterSet.Config as cms
#import HLTrigger.HLTfilters.triggerResultsFilter as hlt
import GT_translationfunctions as gt
process = cms.Process("TEST")
### Load all ESSources, ESProducers and PSets
# process.load("HLTrigger.Configuration.Phase2.hltPhase2Setup_cff")

### GlobalTag
# process.load("Configuration.StandardSequences.CondDBESSource_cff")
# process.GlobalTag.globaltag = "112X_mcRun4_realistic_T15_v2"

process = cms.Process("OWNPARTICLES")

process.load("FWCore.MessageService.MessageLogger_cfi")



process.MuonGTProd = cms.EDProducer('P2GT_TkmuonProd',
	src    =cms.InputTag('L1TkMuons')
)







process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('myOutputFile.root')
    ,outputCommands = cms.untracked.vstring('drop *',
      "keep *P2GTColl*")

)



process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FF7BF0E2-1380-2D48-BB19-F79E6907CD5D.root",    
),
)

process.maxEvents.input = cms.untracked.int32(20)
process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))
process.test = cms.Path(process.MuonGTProd)
process.end = cms.EndPath(process.out)

