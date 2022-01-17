import FWCore.ParameterSet.Config as cms
import HLTrigger.HLTfilters.triggerResultsFilter as hlt
import GT_translationfunctions as gt
process = cms.Process("HLTX")
globtrig = gt.GlobalTrigger("test")
### Load all ESSources, ESProducers and PSets
# process.load("HLTrigger.Configuration.Phase2.hltPhase2Setup_cff")

### GlobalTag
# process.load("Configuration.StandardSequences.CondDBESSource_cff")
# process.GlobalTag.globaltag = "112X_mcRun4_realistic_T15_v2"
looplist = []
for i in range(0,20):
	loopkey = 'HLTtestfilt{}'.format(i)	
	#print(loopkey)	
	test = cms.EDFilter(
		"P2GTDoubleObjFilterMuEle",
        	saveTags = cms.bool(True),
        	inputTag1 = cms.InputTag('L1TkMuons'),
        	inputTag2 = cms.InputTag("L1TkElectronsEllipticMatchCrystal", "EG"),
        	MinPtfirst = gt.pt_to_HW(i + 5),
        	MinPtsecond = gt.pt_to_HW(7),
        	MinEtafirst = gt.eta_to_HW(0),
        	MinEtasecond = gt.eta_to_HW(0),
        	MaxEtafirst =  gt.eta_to_HW(2.4),
        	MaxEtasecond = gt.eta_to_HW(3.4),
        	MinN = cms.int32(1)
	)
	setattr(process,loopkey,test)
	looplist.append(loopkey)	

for i in range(0,20):
	a = getattr(process,'HLTtestfilt{}'.format(i))
	setattr(process,'HLT_path{}'.format(i),cms.Path(a))
	globtrig.addAlgo('HLT_path{}'.format(i))

keylist = []
for i in range (0,20):
	key = 'trf{}'.format(i)	
	test = hlt.triggerResultsFilter.clone(
    		usePathStatus = True,
    		triggerConditions = cms.vstring( "HLT_path{}".format(i)+ " OR "+ "HLT_path{}".format((19-i))),
    		l1tResults = '',
    		throw = True
    		)
		
	setattr(process,key,test)
	keylist.append(key)
	


process.test_trf      = cms.Path(process.trf0)
process.test_trf1      = cms.Path(process.trf1)
process.test_trf2      = cms.Path(process.trf2)
process.test_trf3      = cms.Path(process.trf3)
process.test_trf4     = cms.Path(process.trf4)
globtrig.addAlgo(process.test_trf)
globtrig.addAlgo(process.test_trf1)
globtrig.addAlgo(process.test_trf2)
globtrig.addAlgo(process.test_trf3)


process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(
      #  "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FF7BF0E2-1380-2D48-BB19-F79E6907CD5D.root",
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/SingleElectron_PT2to200/FEVT/PU200_111X_mcRun4_realistic_T15_v1_ext2-v1/270000/0064D31F-F48B-3144-8CB9-17F820065E01.root",
    ),
)

process.maxEvents.input = cms.untracked.int32(-1)
process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))

