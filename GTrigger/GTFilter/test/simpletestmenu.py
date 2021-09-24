import FWCore.ParameterSet.Config as cms
import HLTrigger.HLTfilters.triggerResultsFilter_cfi as hlt
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
        	MinPtfirst = gt.pt_to_HW(i + 1),
        	MinPtsecond = gt.pt_to_HW(9),
        	MinEtafirst = gt.eta_to_HW(3),
        	MinEtasecond = gt.eta_to_HW(3),
        	MaxEtafirst =  gt.eta_to_HW(88),
        	MaxEtasecond = gt.eta_to_HW(33),
        	MinN = cms.int32(1)
	)
	setattr(process,loopkey,test)
	looplist.append(loopkey)	

for i in range(0,20):
	a = getattr(process,'HLTtestfilt{}'.format(i))
	setattr(process,'HLT_path{}'.format(i),cms.Path(a))
	globtrig.addAlgo('HLT_path{}'.format(i))



process.filter_any_star = hlt.triggerResultsFilter.clone(
    usePathStatus = True,

    triggerConditions = ( '*', ),
    l1tResults = '',
    throw = False
    )



process.filter_any_or = hlt.triggerResultsFilter.clone(

    usePathStatus = True,
    triggerConditions = ( 'HLT_path0', 'HLT_path19' ),
    l1tResults = '',
    throw = True
    )

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
globtrig.addAlgolabel(process.test_trf)
globtrig.addAlgolabel(process.test_trf1)
globtrig.addAlgolabel(process.test_trf2)
globtrig.addAlgolabel(process.test_trf3)
process.path_any_or   = cms.Path( process.filter_any_or )
process.path_any_star = cms.Path( process.filter_any_star )

"""

for ls,key in zip(looplist,loopdict):
	process.ls = cms.Path(process.key)
	#process.key.addLabel("test{}".format(key))	

fotfilt0 i in range(0,20):
	
	loopkeyfilter = "testfilt{}".format(i)	
	loopkeypath = "testpath{}".format(i)
	process.a   = cms.Path(process.loopkeyfilter)

process.GTTest = cms.EDFilter(
	"P2GTDoubleObjFilter",
	saveTags = cms.bool(True),
	MinPtMuon = cms.double(7.0),
        MinPtEle  = cms.double(7.0),
	inputTag1 = cms.InputTag("L1TkMuons"),
	inputTag2 = cms.InputTag("L1TkElectronsEllipticMatchCrystal", "EG"),
	MinEtaMuon = cms.double(-2.4),
	MinEtaEle = cms.double(-2.4),
	MaxEtaMuon = cms.double(0),
	MaxEtaEle = cms.double(2.4),
	MinN = cms.int32(1)
)
process.GTTestT = cms.EDFilter(
	"P2GTDoubleObjFilterMuEle",

	saveTags = cms.bool(True),
	inputTag1 = cms.InputTag("L1TkMuons"),
	inputTag2 = cms.InputTag("L1TkElectronsEllipticMatchCrystal", "EG"),
	MinPtfirst = cms.double(7.0),
	MinPtsecond = cms.double(7.0),
	MinEtafirst = cms.double(-2.4),
	MinEtasecond = cms.double(-2.4),
	MaxEtafirst =  cms.double(0),
 	MaxEtasecond = cms.double(2.4),
	MinN = cms.int32(1)
)

	

process.filter_any_or = hlt.triggerResultsFilter.clone(
    usePathStatus = True,
    triggerConditions = ( 'GTTest','GTTestT',),
    l1tResults = '',
    throw = True
)

process.filter_any_or_2 = hlt.triggerResultsFilter.clone(
    usePathStatus = True,
    triggerConditions = ( 'HLT_Muonele','HLT_MuoneleT'),
    l1tResults = '',
    throw = True
)




process.filter_all_explicit = hlt.triggerResultsFilter.clone(
    usePathStatus = True,
    triggerConditions = cms.vstring('HLT_Muonele AND HLT_MuoneleT'),
    l1tResults = '',
    throw = True
)
process.filter_any_star = hlt.triggerResultsFilter.clone(
    usePathStatus = True,

    triggerConditions = ( '*', ),
    l1tResults = '',
    throw = True
    )
process.HLT_Muonele = cms.Path(process.GTTest)
process.HLT_MuoneleT = cms.Path(process.GTTestT)

process.path_any_star = cms.EndPath( process.filter_any_star )
#process.path_any_or   = cms.Path( process.filter_any_or )
process.path_any_or_2   = cms.Path( process.filter_any_or_2 )
process.path_all_explicit = cms.Path( process.filter_all_explicit )
"""
process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(
        "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FF7BF0E2-1380-2D48-BB19-F79E6907CD5D.root",
      #   "/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/SingleElectron_PT2to200/FEVT/PU200_111X_mcRun4_realistic_T15_v1_ext2-v1/270000/0064D31F-F48B-3144-8CB9-17F820065E01.root",
    ),
)

process.maxEvents.input = cms.untracked.int32(-1)
process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))

