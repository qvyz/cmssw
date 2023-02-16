import FWCore.ParameterSet.VarParsing as VarParsing
import FWCore.ParameterSet.Config as cms

process = cms.Process('L1Test')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')


# Input source
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(72))

options = VarParsing.VarParsing()
options.register ("platform",
                  "VU13P",
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string)
# options.parseArguments()


process.l1tGTProducer = cms.EDProducer(
    "L1GTEvaluationProducer",
    outputFilename=cms.string("inputPattern"),
    random_seed=cms.uint32(0),
    maxLines=cms.uint32(1024),
    platform=cms.string(options.platform)
)

process.l1t_GTProducer = cms.Path(process.l1tGTProducer)

from L1Trigger.Phase2L1GT.l1tGTSingleInOutLUT import COSH_ETA_LUT, COSH_ETA_LUT_2, COS_PHI_LUT

COSH_ETA_LUT.export("coshEtaLUT.mem")
COSH_ETA_LUT_2.export("coshEtaLUT2.mem")
COS_PHI_LUT.export("cosPhiLUT.mem")

from L1Trigger.Phase2L1GT.l1tGTSingleObjectCond_cfi import l1tGTSingleObjectCond
from L1Trigger.Phase2L1GT.l1tGTDoubleObjectCond_cfi import l1tGTDoubleObjectCond
from L1Trigger.Phase2L1GT.l1tGTTripleObjectCond_cfi import l1tGTTripleObjectCond
from L1Trigger.Phase2L1GT.l1tGTQuadObjectCond_cfi import l1tGTQuadObjectCond

l1tGTDoubleObjectCond.sanity_checks = cms.untracked.bool(True)
l1tGTDoubleObjectCond.inv_mass_checks = cms.untracked.bool(True)

l1tGTTripleObjectCond.sanity_checks = cms.untracked.bool(True)
l1tGTTripleObjectCond.inv_mass_checks = cms.untracked.bool(True)

l1tGTQuadObjectCond.sanity_checks = cms.untracked.bool(True)
l1tGTQuadObjectCond.inv_mass_checks = cms.untracked.bool(True)

# Conditions
process._singleTkMu_14_er2p3 = l1tGTSingleObjectCond.clone(
    tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
    minPt=cms.double(14),
    minEta=cms.double(-2.3),
    maxEta=cms.double(2.3),
)

process._doubleJet_3_9_dEta_Max1p6_OS = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(9),
    ),
    maxDEta=cms.double(1.6),
)

process._doubleTau_5_9_q2_4_SS = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(5),
        # qual=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(9),
        # qual=cms.double(4),
    ),
    ss=cms.bool(True),
)

process._doubleMu_11_9_q2_4 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(11),
        # qual_cut=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(9),
        # qual_cut=cms.double(4),
    ),
)

process._doubleMuEl_11_9_q2_4_OS = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(11),
        # qual_cut=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(9),
        # qual_cut=cms.double(4),
    ),
    os=cms.bool(True),
)

process._doubleMu_11_9_combPt_19 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(11),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(9),
    ),
    minCombPt=cms.double(19)
)

process._doubleMuEl_11_9_SS = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(11),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(9),
    ),
    ss=cms.bool(True),
)

process._doubleJetGamma_11_9_pr_0p2to1p8_1to3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(11),
        minPhi=cms.double(0.2),
        maxPhi=cms.double(1.8),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(9),
        minPhi=cms.double(1),
        maxPhi=cms.double(3),
    ),
)

process._doubleMuTau_2_9_er_1to3_3to3p3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(2),
        minEta=cms.double(1),
        maxEta=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(9),
        minEta=cms.double(3),
        maxEta=cms.double(3.3),
    ),
)

process._doubleMuEl_2_9_dEtaMin2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(9),
    ),
    minDEta=cms.double(2),
)

process._doubleElGamma_2_9_dPhiMin2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(9),
    ),
    minDPhi=cms.double(2),
)

process._doubleMuEl_2_9_dRMin2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(9),
    ),
    minDR=cms.double(2),
)

process._doubleElTau_2_9_dEta0p2to2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(9),
    ),
    minDEta=cms.double(0.2),
    maxDEta=cms.double(2),
)

process._doubleMuJet_2_9_dPhi2to4 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(9),
    ),
    minDPhi=cms.double(2),
    maxDPhi=cms.double(4),
)

process._doubleMuEl_2_9_dR1to3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt=cms.double(9),
    )
    # minDR=cms.double(1),
    # maxDR=cms.double(3),
)

process._doubleMuGamma_11_9_massMax10 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(11),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt=cms.double(9),
    ),
    maxInvMass=cms.double(10),
)

process._doubleElMu_11_9_mass10to600 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(11),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(9),
    ),
    minInvMass=cms.double(10),
    maxInvMass=cms.double(600),
)

process._doubleTkMu_15_7_er2p4_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(15),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoEleStaEG_22_12_er2p4 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(22),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(12),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkEle_25_12_er2p4 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(25),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(12),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleStaEG_37_24_er2p4 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(37),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(24),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkIsoPhoton_22_12_er2p4 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(22),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(12),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleCaloTau_69_69_er2p1_drMin0p5 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(69),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(69),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doubleCaloTau_90_90_er2p1_drMin0p5 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(90),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(90),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPITau_36_36_er2p1_drMin0p5 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(36),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(36),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPITau_52_52_er2p1_drMin0p5 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(52),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(52),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPIJet_112_112_er2p4_dEtaMax1p6 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(112),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(112),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    maxDEta=cms.double(1.6),
)

process._tkMuonTkIsoEle_7_20_er2p4_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(20),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkMuonTkEle_7_23_er2p4_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(23),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkEleTkMuon_10_20_er2p4_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(20),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_27_18_er2p1_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(27),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(18),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_36_18_er2p1_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(36),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(18),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoElePUPPItau_22_29_er2p1_drMin0p3_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(22),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(29),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.3),
)

process._tkIsoElePUPPItau_22_39_er2p1_drMin0p3_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(22),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(39),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.3),
)

process._tkElePUPPIJet_28_40_er2p1_er2p4_dRmin0p3_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(28),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTPromptJets"),
        minPt=cms.double(40),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    minDR=cms.double(0.3),
)

process._doublePuppiJet_160_35_er5p0_massMin620 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(160),
        minEta=cms.double(-5),
        maxEta=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(35),
        minEta=cms.double(-5),
        maxEta=cms.double(5),
    ),
    minInvMass=cms.double(620),
)

process._doubleTkMuon_2_2_er1p5_drMax1p4_OS_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(2),
        minEta=cms.double(-1.5),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(2),
        minEta=cms.double(-1.5),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.4),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p4_drMax1p2_OS_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(4),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(4),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.2),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p0_massMin7_massMax18_OS_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(4),
        minEta=cms.double(-2.0),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(4),
        minEta=cms.double(-2.0),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    minInvMass=cms.double(7),
    maxInvMass=cms.double(18),
    os=cms.bool(True),
)

process._doubleEG_32_32_er2p5_Mt40 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(32),
        minEta=cms.double(-2.5),
        maxEta=cms.double(2.5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(32),
        minEta=cms.double(-2.5),
        maxEta=cms.double(2.5),
    ),
    minTransMass=cms.double(40),
)


process._triplePuppiJet_70_50_35 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(70)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(50)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(35)
    )
)

process._tripleTkEleTkMuPUPPIJet_30_40_25_er2p4 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(30),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(40),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(25),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    )
)

process._tripleTkMuTkEle_7_5_5_er3p4_SS = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(5),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    delta12=cms.PSet(
        ss=cms.bool(True)
    ),
    delta13=cms.PSet(
        ss=cms.bool(True)
    )
)

process._quadTkMuTkEle_5_5_5_7_er3p4_SS = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(7),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    delta12=cms.PSet(
        ss=cms.bool(True)
    ),
    delta13=cms.PSet(
        ss=cms.bool(True)
    ),
    delta14=cms.PSet(
        ss=cms.bool(True)
    )
)

process._quadTkEleTkMuPUPPIJet_30_40_25_25_er2p4 = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(30),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(40),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(25),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(25),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    )
)
process._singleTkMu_14_er2p3__1 = l1tGTSingleObjectCond.clone(
    tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
    minPt=cms.double(15),
    minEta=cms.double(-2.3),
    maxEta=cms.double(2.3),
)

process._doubleJet_3_9_dEta_Max1p6_OS__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(10),
    ),
    maxDEta=cms.double(1.6),
)

process._doubleTau_5_9_q2_4_SS__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(6),
        # qual=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(10),
        # qual=cms.double(4),
    ),
    ss=cms.bool(True),
)

process._doubleMu_11_9_q2_4__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(12),
        # qual_cut=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(10),
        # qual_cut=cms.double(4),
    ),
)

process._doubleMuEl_11_9_q2_4_OS__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(12),
        # qual_cut=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(10),
        # qual_cut=cms.double(4),
    ),
    os=cms.bool(True),
)

process._doubleMu_11_9_combPt_19__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(12),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
    ),
    minCombPt=cms.double(19)
)

process._doubleMuEl_11_9_SS__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(12),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(10),
    ),
    ss=cms.bool(True),
)

process._doubleJetGamma_11_9_pr_0p2to1p8_1to3__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(12),
        minPhi=cms.double(0.2),
        maxPhi=cms.double(1.8),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(10),
        minPhi=cms.double(1),
        maxPhi=cms.double(3),
    ),
)

process._doubleMuTau_2_9_er_1to3_3to3p3__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(3),
        minEta=cms.double(1),
        maxEta=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(10),
        minEta=cms.double(3),
        maxEta=cms.double(3.3),
    ),
)

process._doubleMuEl_2_9_dEtaMin2__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(10),
    ),
    minDEta=cms.double(2),
)

process._doubleElGamma_2_9_dPhiMin2__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(10),
    ),
    minDPhi=cms.double(2),
)

process._doubleMuEl_2_9_dRMin2__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(10),
    ),
    minDR=cms.double(2),
)

process._doubleElTau_2_9_dEta0p2to2__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(10),
    ),
    minDEta=cms.double(0.2),
    maxDEta=cms.double(2),
)

process._doubleMuJet_2_9_dPhi2to4__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(10),
    ),
    minDPhi=cms.double(2),
    maxDPhi=cms.double(4),
)

process._doubleMuEl_2_9_dR1to3__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt=cms.double(10),
    )
    # minDR=cms.double(1),
    # maxDR=cms.double(3),
)

process._doubleMuGamma_11_9_massMax10__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(12),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt=cms.double(10),
    ),
    maxInvMass=cms.double(10),
)

process._doubleElMu_11_9_mass10to600__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(12),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(10),
    ),
    minInvMass=cms.double(10),
    maxInvMass=cms.double(600),
)

process._doubleTkMu_15_7_er2p4_dzMax1p0__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(16),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoEleStaEG_22_12_er2p4__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(23),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(13),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkEle_25_12_er2p4__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(26),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(13),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleStaEG_37_24_er2p4__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(38),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(25),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkIsoPhoton_22_12_er2p4__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(23),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(13),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleCaloTau_69_69_er2p1_drMin0p5__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(70),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(70),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doubleCaloTau_90_90_er2p1_drMin0p5__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(91),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(91),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPITau_36_36_er2p1_drMin0p5__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(37),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(37),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPITau_52_52_er2p1_drMin0p5__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(53),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(53),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPIJet_112_112_er2p4_dEtaMax1p6__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(113),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(113),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    maxDEta=cms.double(1.6),
)

process._tkMuonTkIsoEle_7_20_er2p4_dzMax1p0__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(21),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkMuonTkEle_7_23_er2p4_dzMax1p0__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(24),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkEleTkMuon_10_20_er2p4_dzMax1p0__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(11),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(21),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_27_18_er2p1_dzMax1p0__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(28),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(19),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_36_18_er2p1_dzMax1p0__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(37),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(19),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoElePUPPItau_22_29_er2p1_drMin0p3_dzMax1p0__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(23),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(30),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.3),
)

process._tkIsoElePUPPItau_22_39_er2p1_drMin0p3_dzMax1p0__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(23),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(40),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.3),
)

process._tkElePUPPIJet_28_40_er2p1_er2p4_dRmin0p3_dzMax1p0__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(29),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTPromptJets"),
        minPt=cms.double(41),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    minDR=cms.double(0.3),
)

process._doublePuppiJet_160_35_er5p0_massMin620__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(161),
        minEta=cms.double(-5),
        maxEta=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(36),
        minEta=cms.double(-5),
        maxEta=cms.double(5),
    ),
    minInvMass=cms.double(620),
)

process._doubleTkMuon_2_2_er1p5_drMax1p4_OS_dzMax1p0__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(3),
        minEta=cms.double(-1.5),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(3),
        minEta=cms.double(-1.5),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.4),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p4_drMax1p2_OS_dzMax1p0__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.2),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p0_massMin7_massMax18_OS_dzMax1p0__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-2.0),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-2.0),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    minInvMass=cms.double(7),
    maxInvMass=cms.double(18),
    os=cms.bool(True),
)

process._doubleEG_32_32_er2p5_Mt40__1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(33),
        minEta=cms.double(-2.5),
        maxEta=cms.double(2.5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(33),
        minEta=cms.double(-2.5),
        maxEta=cms.double(2.5),
    ),
    minTransMass=cms.double(40),
)


process._triplePuppiJet_70_50_35__1 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(71)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(51)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(36)
    )
)

process._tripleTkEleTkMuPUPPIJet_30_40_25_er2p4__1 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(31),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(41),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(26),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    )
)

process._tripleTkMuTkEle_7_5_5_er3p4_SS__1 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(6),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    delta12=cms.PSet(
        ss=cms.bool(True)
    ),
    delta13=cms.PSet(
        ss=cms.bool(True)
    )
)

process._quadTkMuTkEle_5_5_5_7_er3p4_SS__1 = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(8),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    delta12=cms.PSet(
        ss=cms.bool(True)
    ),
    delta13=cms.PSet(
        ss=cms.bool(True)
    ),
    delta14=cms.PSet(
        ss=cms.bool(True)
    )
)

process._quadTkEleTkMuPUPPIJet_30_40_25_25_er2p4__1 = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(31),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(41),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(26),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(26),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    )
)
process._singleTkMu_14_er2p3__2 = l1tGTSingleObjectCond.clone(
    tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
    minPt=cms.double(16),
    minEta=cms.double(-2.3),
    maxEta=cms.double(2.3),
)

process._doubleJet_3_9_dEta_Max1p6_OS__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(11),
    ),
    maxDEta=cms.double(1.6),
)

process._doubleTau_5_9_q2_4_SS__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(7),
        # qual=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(11),
        # qual=cms.double(4),
    ),
    ss=cms.bool(True),
)

process._doubleMu_11_9_q2_4__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(13),
        # qual_cut=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(11),
        # qual_cut=cms.double(4),
    ),
)

process._doubleMuEl_11_9_q2_4_OS__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(13),
        # qual_cut=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(11),
        # qual_cut=cms.double(4),
    ),
    os=cms.bool(True),
)

process._doubleMu_11_9_combPt_19__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(13),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(11),
    ),
    minCombPt=cms.double(19)
)

process._doubleMuEl_11_9_SS__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(13),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(11),
    ),
    ss=cms.bool(True),
)

process._doubleJetGamma_11_9_pr_0p2to1p8_1to3__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(13),
        minPhi=cms.double(0.2),
        maxPhi=cms.double(1.8),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(11),
        minPhi=cms.double(1),
        maxPhi=cms.double(3),
    ),
)

process._doubleMuTau_2_9_er_1to3_3to3p3__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(4),
        minEta=cms.double(1),
        maxEta=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(11),
        minEta=cms.double(3),
        maxEta=cms.double(3.3),
    ),
)

process._doubleMuEl_2_9_dEtaMin2__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(11),
    ),
    minDEta=cms.double(2),
)

process._doubleElGamma_2_9_dPhiMin2__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(11),
    ),
    minDPhi=cms.double(2),
)

process._doubleMuEl_2_9_dRMin2__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(11),
    ),
    minDR=cms.double(2),
)

process._doubleElTau_2_9_dEta0p2to2__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(11),
    ),
    minDEta=cms.double(0.2),
    maxDEta=cms.double(2),
)

process._doubleMuJet_2_9_dPhi2to4__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(11),
    ),
    minDPhi=cms.double(2),
    maxDPhi=cms.double(4),
)

process._doubleMuEl_2_9_dR1to3__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt=cms.double(11),
    )
    # minDR=cms.double(1),
    # maxDR=cms.double(3),
)

process._doubleMuGamma_11_9_massMax10__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(13),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt=cms.double(11),
    ),
    maxInvMass=cms.double(10),
)

process._doubleElMu_11_9_mass10to600__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(13),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(11),
    ),
    minInvMass=cms.double(10),
    maxInvMass=cms.double(600),
)

process._doubleTkMu_15_7_er2p4_dzMax1p0__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(17),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(9),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoEleStaEG_22_12_er2p4__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(24),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(14),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkEle_25_12_er2p4__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(27),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(14),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleStaEG_37_24_er2p4__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(39),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(26),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkIsoPhoton_22_12_er2p4__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(24),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(14),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleCaloTau_69_69_er2p1_drMin0p5__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(71),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(71),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doubleCaloTau_90_90_er2p1_drMin0p5__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(92),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(92),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPITau_36_36_er2p1_drMin0p5__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(38),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(38),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPITau_52_52_er2p1_drMin0p5__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(54),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(54),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPIJet_112_112_er2p4_dEtaMax1p6__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(114),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(114),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    maxDEta=cms.double(1.6),
)

process._tkMuonTkIsoEle_7_20_er2p4_dzMax1p0__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(9),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(22),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkMuonTkEle_7_23_er2p4_dzMax1p0__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(9),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(25),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkEleTkMuon_10_20_er2p4_dzMax1p0__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(12),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(22),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_27_18_er2p1_dzMax1p0__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(29),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(20),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_36_18_er2p1_dzMax1p0__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(38),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(20),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoElePUPPItau_22_29_er2p1_drMin0p3_dzMax1p0__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(24),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(31),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.3),
)

process._tkIsoElePUPPItau_22_39_er2p1_drMin0p3_dzMax1p0__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(24),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(41),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.3),
)

process._tkElePUPPIJet_28_40_er2p1_er2p4_dRmin0p3_dzMax1p0__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(30),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTPromptJets"),
        minPt=cms.double(42),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    minDR=cms.double(0.3),
)

process._doublePuppiJet_160_35_er5p0_massMin620__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(162),
        minEta=cms.double(-5),
        maxEta=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(37),
        minEta=cms.double(-5),
        maxEta=cms.double(5),
    ),
    minInvMass=cms.double(620),
)

process._doubleTkMuon_2_2_er1p5_drMax1p4_OS_dzMax1p0__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(4),
        minEta=cms.double(-1.5),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(4),
        minEta=cms.double(-1.5),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.4),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p4_drMax1p2_OS_dzMax1p0__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.2),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p0_massMin7_massMax18_OS_dzMax1p0__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-2.0),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-2.0),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    minInvMass=cms.double(7),
    maxInvMass=cms.double(18),
    os=cms.bool(True),
)

process._doubleEG_32_32_er2p5_Mt40__2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(34),
        minEta=cms.double(-2.5),
        maxEta=cms.double(2.5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(34),
        minEta=cms.double(-2.5),
        maxEta=cms.double(2.5),
    ),
    minTransMass=cms.double(40),
)


process._triplePuppiJet_70_50_35__2 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(72)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(52)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(37)
    )
)

process._tripleTkEleTkMuPUPPIJet_30_40_25_er2p4__2 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(32),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(42),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(27),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    )
)

process._tripleTkMuTkEle_7_5_5_er3p4_SS__2 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(9),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(7),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    delta12=cms.PSet(
        ss=cms.bool(True)
    ),
    delta13=cms.PSet(
        ss=cms.bool(True)
    )
)

process._quadTkMuTkEle_5_5_5_7_er3p4_SS__2 = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(9),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    delta12=cms.PSet(
        ss=cms.bool(True)
    ),
    delta13=cms.PSet(
        ss=cms.bool(True)
    ),
    delta14=cms.PSet(
        ss=cms.bool(True)
    )
)

process._quadTkEleTkMuPUPPIJet_30_40_25_25_er2p4__2 = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(32),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(42),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(27),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(27),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    )
)



process._singleTkMu_14_er2p3__3 = l1tGTSingleObjectCond.clone(
    tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
    minPt=cms.double(17),
    minEta=cms.double(-2.3),
    maxEta=cms.double(2.3),
)

process._doubleJet_3_9_dEta_Max1p6_OS__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(6),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(12),
    ),
    maxDEta=cms.double(1.6),
)

process._doubleTau_5_9_q2_4_SS__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(8),
        # qual=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(12),
        # qual=cms.double(4),
    ),
    ss=cms.bool(True),
)

process._doubleMu_11_9_q2_4__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(14),
        # qual_cut=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(12),
        # qual_cut=cms.double(4),
    ),
)

process._doubleMuEl_11_9_q2_4_OS__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(14),
        # qual_cut=cms.double(2),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(12),
        # qual_cut=cms.double(4),
    ),
    os=cms.bool(True),
)

process._doubleMu_11_9_combPt_19__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(14),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(12),
    ),
    minCombPt=cms.double(19)
)

process._doubleMuEl_11_9_SS__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(14),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(12),
    ),
    ss=cms.bool(True),
)

process._doubleJetGamma_11_9_pr_0p2to1p8_1to3__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(14),
        minPhi=cms.double(0.2),
        maxPhi=cms.double(1.8),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(12),
        minPhi=cms.double(1),
        maxPhi=cms.double(3),
    ),
)

process._doubleMuTau_2_9_er_1to3_3to3p3__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(5),
        minEta=cms.double(1),
        maxEta=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(12),
        minEta=cms.double(3),
        maxEta=cms.double(3.3),
    ),
)

process._doubleMuEl_2_9_dEtaMin2__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(12),
    ),
    minDEta=cms.double(2),
)

process._doubleElGamma_2_9_dPhiMin2__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(12),
    ),
    minDPhi=cms.double(2),
)

process._doubleMuEl_2_9_dRMin2__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(12),
    ),
    minDR=cms.double(2),
)

process._doubleElTau_2_9_dEta0p2to2__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(12),
    ),
    minDEta=cms.double(0.2),
    maxDEta=cms.double(2),
)

process._doubleMuJet_2_9_dPhi2to4__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(12),
    ),
    minDPhi=cms.double(2),
    maxDPhi=cms.double(4),
)

process._doubleMuEl_2_9_dR1to3__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt=cms.double(12),
    )
    # minDR=cms.double(1),
    # maxDR=cms.double(3),
)

process._doubleMuGamma_11_9_massMax10__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(14),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt=cms.double(12),
    ),
    maxInvMass=cms.double(10),
)

process._doubleElMu_11_9_mass10to600__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(14),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(12),
    ),
    minInvMass=cms.double(10),
    maxInvMass=cms.double(600),
)

process._doubleTkMu_15_7_er2p4_dzMax1p0__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(18),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoEleStaEG_22_12_er2p4__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(25),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(15),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkEle_25_12_er2p4__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(28),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(15),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleStaEG_37_24_er2p4__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(40),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(27),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkIsoPhoton_22_12_er2p4__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(25),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(15),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
)

process._doubleCaloTau_69_69_er2p1_drMin0p5__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(72),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(72),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doubleCaloTau_90_90_er2p1_drMin0p5__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(93),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(93),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPITau_36_36_er2p1_drMin0p5__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(39),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(39),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPITau_52_52_er2p1_drMin0p5__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(55),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(55),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPIJet_112_112_er2p4_dEtaMax1p6__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(115),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(115),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
    ),
    maxDEta=cms.double(1.6),
)

process._tkMuonTkIsoEle_7_20_er2p4_dzMax1p0__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(23),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkMuonTkEle_7_23_er2p4_dzMax1p0__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(26),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkEleTkMuon_10_20_er2p4_dzMax1p0__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(13),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(23),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_27_18_er2p1_dzMax1p0__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(30),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(21),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_36_18_er2p1_dzMax1p0__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(39),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(21),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoElePUPPItau_22_29_er2p1_drMin0p3_dzMax1p0__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(25),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(32),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.3),
)

process._tkIsoElePUPPItau_22_39_er2p1_drMin0p3_dzMax1p0__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(25),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(42),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.3),
)

process._tkElePUPPIJet_28_40_er2p1_er2p4_dRmin0p3_dzMax1p0__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(31),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTPromptJets"),
        minPt=cms.double(43),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    minDR=cms.double(0.3),
)

process._doublePuppiJet_160_35_er5p0_massMin620__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(163),
        minEta=cms.double(-5),
        maxEta=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(38),
        minEta=cms.double(-5),
        maxEta=cms.double(5),
    ),
    minInvMass=cms.double(620),
)

process._doubleTkMuon_2_2_er1p5_drMax1p4_OS_dzMax1p0__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-1.5),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-1.5),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.4),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p4_drMax1p2_OS_dzMax1p0__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.2),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p0_massMin7_massMax18_OS_dzMax1p0__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.0),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.0),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    minInvMass=cms.double(7),
    maxInvMass=cms.double(18),
    os=cms.bool(True),
)

process._doubleEG_32_32_er2p5_Mt40__3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(35),
        minEta=cms.double(-2.5),
        maxEta=cms.double(2.5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(35),
        minEta=cms.double(-2.5),
        maxEta=cms.double(2.5),
    ),
    minTransMass=cms.double(40),
)


process._triplePuppiJet_70_50_35__3 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(73)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(53)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(38)
    )
)

process._tripleTkEleTkMuPUPPIJet_30_40_25_er2p4__3 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(33),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(43),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(28),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    )
)

process._tripleTkMuTkEle_7_5_5_er3p4_SS__3 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(8),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    delta12=cms.PSet(
        ss=cms.bool(True)
    ),
    delta13=cms.PSet(
        ss=cms.bool(True)
    )
)

process._quadTkMuTkEle_5_5_5_7_er3p4_SS__3 = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(10),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    delta12=cms.PSet(
        ss=cms.bool(True)
    ),
    delta13=cms.PSet(
        ss=cms.bool(True)
    ),
    delta14=cms.PSet(
        ss=cms.bool(True)
    )
)

process._quadTkEleTkMuPUPPIJet_30_40_25_25_er2p4__3 = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(33),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(43),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(28),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(28),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    )
)


process._tkIsoElePUPPItau_22_39_er2p1_drMin0p3_dzMax1p0__ext = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(28),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(45),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.3),
)

process._tkElePUPPIJet_28_40_er2p1_er2p4_dRmin0p3_dzMax1p0__ext = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(34),
        minEta=cms.double(-2.1),
        maxEta=cms.double(2.1),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTPromptJets"),
        minPt=cms.double(46),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    minDR=cms.double(0.3),
)

process._doublePuppiJet_160_35_er5p0_massMin620__ext = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(166),
        minEta=cms.double(-5),
        maxEta=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(41),
        minEta=cms.double(-5),
        maxEta=cms.double(5),
    ),
    minInvMass=cms.double(620),
)

process._doubleTkMuon_2_2_er1p5_drMax1p4_OS_dzMax1p0__ext = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-1.5),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-1.5),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.4),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p4_drMax1p2_OS_dzMax1p0__ext = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.2),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p0_massMin7_massMax18_OS_dzMax1p0__ext = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.0),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.0),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    minInvMass=cms.double(7),
    os=cms.bool(True),
)

process._doubleEG_32_32_er2p5_Mt40__ext = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(38),
        minEta=cms.double(-2.5),
        maxEta=cms.double(2.5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(38),
        minEta=cms.double(-2.5),
        maxEta=cms.double(2.5),
    ),
    minTransMass=cms.double(40),
)


process._triplePuppiJet_70_50_35__ext = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(76)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(56)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(41)
    )
)

process._tripleTkEleTkMuPUPPIJet_30_40_25_er2p4__ext = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(36),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(46),
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(31),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    )
)

process._tripleTkMuTkEle_7_5_5_er3p4_SS__ext = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(13),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(11),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(11),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    delta12=cms.PSet(
        ss=cms.bool(True)
    )
)

process._quadTkMuTkEle_5_5_5_7_er3p4_SS__ext = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(11),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(11),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(11),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(13),
        minEta=cms.double(-3.4),
        maxEta=cms.double(3.4)
    )
)

process._quadTkEleTkMuPUPPIJet_30_40_25_25_er2p4__ext = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(36),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(46),
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(31),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(31),
        minEta=cms.double(-2.4),
        maxEta=cms.double(2.4)
    )
)
algobit_conf = {}
idx = 0
# remove '_', since it is not allowed for module names
for filt_name in process.filters:
    if filt_name[:1] != '_':
        continue
    new_name = filt_name.replace('_', '')
    setattr(process, new_name, getattr(process, filt_name).clone())
    delattr(process, filt_name)
    algobit_conf[idx] = 'l1t' + filt_name
    setattr(process, 'l1t' + filt_name, cms.Path(getattr(process, new_name)))
    idx += 1

# Algo bits
from L1Trigger.Phase2L1GT.l1tGTAlgoChannelConfig import generate_channel_config

if options.platform == "VU13P":
    channel_conf = generate_channel_config({
        0: algobit_conf,
        24: algobit_conf,
        32: algobit_conf,
        48: algobit_conf
    })
else:
    channel_conf = generate_channel_config({
        0: algobit_conf,
        28: algobit_conf,
        46: algobit_conf
    })


process.BoardData = cms.EDAnalyzer("L1GTBoardWriter",
  outputFilename = cms.string("outputPattern"),
  maxLines = cms.uint32(1024),
  channelConfig = channel_conf
)

process.l1t_BoardData = cms.EndPath(process.BoardData)

process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('file:test_output.root'),
    outputCommands = cms.untracked.vstring('keep *'),
    splitLevel = cms.untracked.int32(0)
)

process.output_step = cms.EndPath(process.output)
