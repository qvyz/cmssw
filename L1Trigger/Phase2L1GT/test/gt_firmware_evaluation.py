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
    minEta=cms.double(-2.093),
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
    maxDEta=cms.double(2.6),
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
        minEta=cms.double(1.2),
        maxEta=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(9),
        minEta=cms.double(3.3),
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
    minDR=cms.double(0.38),
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
    # minDR=cms.double(0.2),
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
    maxInvMass=cms.double(1.40),
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
    minInvMass=cms.double(1.26),
    maxInvMass=cms.double(1.44),
)

process._doubleTkMu_15_7_er2p4_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(15),
        minEta=cms.double(-2),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-1.9),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoEleStaEG_22_12_er2p4 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(22),
        minEta=cms.double(-1.7),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(12),
        minEta=cms.double(-1.7),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkEle_25_12_er2p4 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(25),
        minEta=cms.double(-1.5),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(12),
        minEta=cms.double(-1.5),
        maxEta=cms.double(2.4),
    ),
)

process._doubleStaEG_37_24_er2p4 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(37),
        minEta=cms.double(-2.3),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(24),
        minEta=cms.double(-2.29),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkIsoPhoton_22_12_er2p4 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(22),
        minEta=cms.double(-2.28),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(12),
        minEta=cms.double(-2.27),
        maxEta=cms.double(2.4),
    ),
)

process._doubleCaloTau_69_69_er2p1_drMin0p5 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(69),
        minEta=cms.double(-1.96),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(69),
        minEta=cms.double(-1.95),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.3),
)

process._doubleCaloTau_90_90_er2p1_drMin0p5 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(90),
        minEta=cms.double(-1.94),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(90),
        minEta=cms.double(-1.93),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.4),
)

process._doublePUPPITau_36_36_er2p1_drMin0p5 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(36),
        minEta=cms.double(-1.92),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(36),
        minEta=cms.double(-1.910),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.5),
)

process._doublePUPPITau_52_52_er2p1_drMin0p5 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(52),
        minEta=cms.double(-1.900),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(52),
        minEta=cms.double(-1.890),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.6),
)

process._doublePUPPIJet_112_112_er2p4_dEtaMax1p6 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(112),
        minEta=cms.double(-2.17),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(112),
        minEta=cms.double(-2.17),
        maxEta=cms.double(2.4),
    ),
    maxDEta=cms.double(3.6),
)

process._tkMuonTkIsoEle_7_20_er2p4_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.16),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(20),
        minEta=cms.double(-2.15),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkMuonTkEle_7_23_er2p4_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.13),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(23),
        minEta=cms.double(-2.13),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkEleTkMuon_10_20_er2p4_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.12),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(20),
        minEta=cms.double(-2.11),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_27_18_er2p1_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(27),
        minEta=cms.double(-1.8),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(18),
        minEta=cms.double(-1.79),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_36_18_er2p1_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(36),
        minEta=cms.double(-1.78),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(18),
        minEta=cms.double(-1.77),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoElePUPPItau_22_29_er2p1_drMin0p3_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(22),
        minEta=cms.double(-1.76),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(29),
        minEta=cms.double(-1.75),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.7),
)

process._tkIsoElePUPPItau_22_39_er2p1_drMin0p3_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(22),
        minEta=cms.double(-1.74),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(39),
        minEta=cms.double(-1.73),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.8),
)

process._tkElePUPPIJet_28_40_er2p1_er2p4_dRmin0p3_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(28),
        minEta=cms.double(-1.72),
        maxEta=cms.double(2.1),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTPromptJets"),
        minPt=cms.double(40),
        minEta=cms.double(-2.01),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    minDR=cms.double(0.9),
)

process._doublePuppiJet_160_35_er5p0_massMin620 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(160),
        minEta=cms.double(-2.6),
        maxEta=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(35),
        minEta=cms.double(-2.59),
        maxEta=cms.double(3),
    ),
    minInvMass=cms.double(1.624),
)

process._doubleTkMuon_2_2_er1p5_drMax1p4_OS_dzMax1p0 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(2),
        minEta=cms.double(-1.08),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(2),
        minEta=cms.double(-1.07),
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
        minEta=cms.double(-1.96),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(4),
        minEta=cms.double(-1.95),
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
        minEta=cms.double(-1.54),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(4),
        minEta=cms.double(-1.53),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    minInvMass=cms.double(1.12),
    maxInvMass=cms.double(1.48),
    os=cms.bool(True),
)

process._doubleEG_32_32_er2p5_Mt40 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(32),
        minEta=cms.double(-2.02),
        maxEta=cms.double(2.5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(32),
        minEta=cms.double(-2.01),
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
        minEta=cms.double(-1.9),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(40),
        minEta=cms.double(-1.89),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(25),
        minEta=cms.double(-1.88),
        maxEta=cms.double(2.4)
    )
)

process._tripleTkMuTkEle_7_5_5_er3p4_SS = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.87),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-2.86),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(5),
        minEta=cms.double(-2.84),
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
        minEta=cms.double(-2.84),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-2.83),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-2.82),
        maxEta=cms.double(3.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.81),
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
        minEta=cms.double(-1.7),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(40),
        minEta=cms.double(-1.79),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(25),
        minEta=cms.double(-1.77),
        maxEta=cms.double(2.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(25),
        minEta=cms.double(-1.77),
        maxEta=cms.double(2.4)
    )
)
process._singleTkMu_14_er2p3_xxx_1 = l1tGTSingleObjectCond.clone(
    tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
    minPt=cms.double(15),
    minEta=cms.double(-1.65),
    maxEta=cms.double(2.3),
)

process._doubleJet_3_9_dEta_Max1p6_OS_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTJets"),
        minPt=cms.double(10),
    ),
    maxDEta=cms.double(0.6),
)

process._doubleTau_5_9_q2_4_SS_xxx_1 = l1tGTDoubleObjectCond.clone(
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

process._doubleMu_11_9_q2_4_xxx_1 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuEl_11_9_q2_4_OS_xxx_1 = l1tGTDoubleObjectCond.clone(
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

process._doubleMu_11_9_combPt_19_xxx_1 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuEl_11_9_SS_xxx_1 = l1tGTDoubleObjectCond.clone(
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

process._doubleJetGamma_11_9_pr_0p2to1p8_1to3_xxx_1 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuTau_2_9_er_1to3_3to3p3_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(3),
        minEta=cms.double(1.65),
        maxEta=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(10),
        minEta=cms.double(3.66),
        maxEta=cms.double(3.3),
    ),
)

process._doubleMuEl_2_9_dEtaMin2_xxx_1 = l1tGTDoubleObjectCond.clone(
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

process._doubleElGamma_2_9_dPhiMin2_xxx_1 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuEl_2_9_dRMin2_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(10),
    ),
    minDR=cms.double(0.10),
)

process._doubleElTau_2_9_dEta0p2to2_xxx_1 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuJet_2_9_dPhi2to4_xxx_1 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuEl_2_9_dR1to3_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt=cms.double(10),
    )
    # minDR=cms.double(0.11),
    # maxDR=cms.double(3),
)

process._doubleMuGamma_11_9_massMax10_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(12),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt=cms.double(10),
    ),
    maxInvMass=cms.double(1.52),
)

process._doubleElMu_11_9_mass10to600_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(12),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(10),
    ),
    minInvMass=cms.double(1.16),
    maxInvMass=cms.double(1.56),
)

process._doubleTkMu_15_7_er2p4_dzMax1p0_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(16),
        minEta=cms.double(-1.73),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-1.71),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoEleStaEG_22_12_er2p4_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(23),
        minEta=cms.double(-1.71),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(13),
        minEta=cms.double(-1.7),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkEle_25_12_er2p4_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(26),
        minEta=cms.double(-1.69),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(13),
        minEta=cms.double(-1.68),
        maxEta=cms.double(2.4),
    ),
)

process._doubleStaEG_37_24_er2p4_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(38),
        minEta=cms.double(-1.67),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(25),
        minEta=cms.double(-1.66),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkIsoPhoton_22_12_er2p4_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(23),
        minEta=cms.double(-1.65),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(13),
        minEta=cms.double(-1.64),
        maxEta=cms.double(2.4),
    ),
)

process._doubleCaloTau_69_69_er2p1_drMin0p5_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(70),
        minEta=cms.double(-1.33),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(70),
        minEta=cms.double(-1.32),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.12),
)

process._doubleCaloTau_90_90_er2p1_drMin0p5_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(91),
        minEta=cms.double(-1.31),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(91),
        minEta=cms.double(-1.3),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.13),
)

process._doublePUPPITau_36_36_er2p1_drMin0p5_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(37),
        minEta=cms.double(-1.29),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(37),
        minEta=cms.double(-1.28),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.14),
)

process._doublePUPPITau_52_52_er2p1_drMin0p5_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(53),
        minEta=cms.double(-1.27),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(53),
        minEta=cms.double(-1.26),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.15),
)

process._doublePUPPIJet_112_112_er2p4_dEtaMax1p6_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(113),
        minEta=cms.double(-1.54),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(113),
        minEta=cms.double(-1.54),
        maxEta=cms.double(2.4),
    ),
    maxDEta=cms.double(1.16),
)

process._tkMuonTkIsoEle_7_20_er2p4_dzMax1p0_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-1.52),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(21),
        minEta=cms.double(-1.52),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkMuonTkEle_7_23_er2p4_dzMax1p0_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-1.50),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(24),
        minEta=cms.double(-1.5),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkEleTkMuon_10_20_er2p4_dzMax1p0_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(11),
        minEta=cms.double(-1.48),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(21),
        minEta=cms.double(-1.48),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_27_18_er2p1_dzMax1p0_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(28),
        minEta=cms.double(-1.17),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(19),
        minEta=cms.double(-1.160),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_36_18_er2p1_dzMax1p0_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(37),
        minEta=cms.double(-1.150),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(19),
        minEta=cms.double(-1.140),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoElePUPPItau_22_29_er2p1_drMin0p3_dzMax1p0_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(23),
        minEta=cms.double(-1.130),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(30),
        minEta=cms.double(-1.12),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.16),
)

process._tkIsoElePUPPItau_22_39_er2p1_drMin0p3_dzMax1p0_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(23),
        minEta=cms.double(-1.11),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(40),
        minEta=cms.double(-2),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.17),
)

process._tkElePUPPIJet_28_40_er2p1_er2p4_dRmin0p3_dzMax1p0_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(29),
        minEta=cms.double(-1.999),
        maxEta=cms.double(2.1),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTPromptJets"),
        minPt=cms.double(41),
        minEta=cms.double(-2.298),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    minDR=cms.double(0.18),
)

process._doublePuppiJet_160_35_er5p0_massMin620_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(161),
        minEta=cms.double(-4.897),
        maxEta=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(36),
        minEta=cms.double(-4.896),
        maxEta=cms.double(3),
    ),
    minInvMass=cms.double(1.627),
)

process._doubleTkMuon_2_2_er1p5_drMax1p4_OS_dzMax1p0_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(3),
        minEta=cms.double(-1.395),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(3),
        minEta=cms.double(-1.394),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.4),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p4_drMax1p2_OS_dzMax1p0_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-2.29),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-2.292),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.2),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p0_massMin7_massMax18_OS_dzMax1p0_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-1.891),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-1.89),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    minInvMass=cms.double(1.15),
    maxInvMass=cms.double(1.60),
    os=cms.bool(True),
)

process._doubleEG_32_32_er2p5_Mt40_xxx_1 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(33),
        minEta=cms.double(-2.389),
        maxEta=cms.double(2.5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(33),
        minEta=cms.double(-2.388),
        maxEta=cms.double(2.5),
    ),
    minTransMass=cms.double(40),
)


process._triplePuppiJet_70_50_35_xxx_1 = l1tGTTripleObjectCond.clone(
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

process._tripleTkEleTkMuPUPPIJet_30_40_25_er2p4_xxx_1 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(31),
        minEta=cms.double(-2.287),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(41),
        minEta=cms.double(-2.286),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(26),
        minEta=cms.double(-2.28),
        maxEta=cms.double(2.4)
    )
)

process._tripleTkMuTkEle_7_5_5_er3p4_SS_xxx_1 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-3.284),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-3.283),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(6),
        minEta=cms.double(-3.282),
        maxEta=cms.double(3.4)
    ),
    delta12=cms.PSet(
        ss=cms.bool(True)
    ),
    delta13=cms.PSet(
        ss=cms.bool(True)
    )
)

process._quadTkMuTkEle_5_5_5_7_er3p4_SS_xxx_1 = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-3.28),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-3.28),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-3.279),
        maxEta=cms.double(3.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(8),
        minEta=cms.double(-3.278),
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

process._quadTkEleTkMuPUPPIJet_30_40_25_25_er2p4_xxx_1 = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(31),
        minEta=cms.double(-2.277),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(41),
        minEta=cms.double(-2.276),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(26),
        minEta=cms.double(-2.275),
        maxEta=cms.double(2.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(26),
        minEta=cms.double(-2.274),
        maxEta=cms.double(2.4)
    )
)
process._singleTkMu_14_er2p3_xxx_2 = l1tGTSingleObjectCond.clone(
    tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
    minPt=cms.double(16),
    minEta=cms.double(-2.173),
    maxEta=cms.double(2.3),
)

process._doubleJet_3_9_dEta_Max1p6_OS_xxx_2 = l1tGTDoubleObjectCond.clone(
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

process._doubleTau_5_9_q2_4_SS_xxx_2 = l1tGTDoubleObjectCond.clone(
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

process._doubleMu_11_9_q2_4_xxx_2 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuEl_11_9_q2_4_OS_xxx_2 = l1tGTDoubleObjectCond.clone(
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

process._doubleMu_11_9_combPt_19_xxx_2 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuEl_11_9_SS_xxx_2 = l1tGTDoubleObjectCond.clone(
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

process._doubleJetGamma_11_9_pr_0p2to1p8_1to3_xxx_2 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuTau_2_9_er_1to3_3to3p3_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(4),
        minEta=cms.double(1.128),
        maxEta=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(11),
        minEta=cms.double(3.129),
        maxEta=cms.double(3.3),
    ),
)

process._doubleMuEl_2_9_dEtaMin2_xxx_2 = l1tGTDoubleObjectCond.clone(
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

process._doubleElGamma_2_9_dPhiMin2_xxx_2 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuEl_2_9_dRMin2_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(11),
    ),
    minDR=cms.double(0.19),
)

process._doubleElTau_2_9_dEta0p2to2_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(11),
    ),
    minDEta=cms.double(1.23),
    maxDEta=cms.double(2),
)

process._doubleMuJet_2_9_dPhi2to4_xxx_2 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuEl_2_9_dR1to3_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt=cms.double(11),
    )
    # minDR=cms.double(0.20),
    # maxDR=cms.double(3),
)

process._doubleMuGamma_11_9_massMax10_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(13),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt=cms.double(11),
    ),
    maxInvMass=cms.double(1.64),
)

process._doubleElMu_11_9_mass10to600_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(13),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(11),
    ),
    minInvMass=cms.double(1.19),
    maxInvMass=cms.double(1.68),
)

process._doubleTkMu_15_7_er2p4_dzMax1p0_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(17),
        minEta=cms.double(-2.27),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(9),
        minEta=cms.double(-2.269),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoEleStaEG_22_12_er2p4_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(24),
        minEta=cms.double(-2.268),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(14),
        minEta=cms.double(-2.267),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkEle_25_12_er2p4_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(27),
        minEta=cms.double(-2.266),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(14),
        minEta=cms.double(-2.26),
        maxEta=cms.double(2.4),
    ),
)

process._doubleStaEG_37_24_er2p4_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(39),
        minEta=cms.double(-2.264),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(26),
        minEta=cms.double(-2.263),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkIsoPhoton_22_12_er2p4_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(24),
        minEta=cms.double(-2.262),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(14),
        minEta=cms.double(-2.261),
        maxEta=cms.double(2.4),
    ),
)

process._doubleCaloTau_69_69_er2p1_drMin0p5_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(71),
        minEta=cms.double(-1.96),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(71),
        minEta=cms.double(-1.959),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.21),
)

process._doubleCaloTau_90_90_er2p1_drMin0p5_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(92),
        minEta=cms.double(-1.958),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(92),
        minEta=cms.double(-1.957),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.22),
)

process._doublePUPPITau_36_36_er2p1_drMin0p5_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(38),
        minEta=cms.double(-1.956),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(38),
        minEta=cms.double(-1.955),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.23),
)

process._doublePUPPITau_52_52_er2p1_drMin0p5_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(54),
        minEta=cms.double(-1.954),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(54),
        minEta=cms.double(-1.953),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.24),
)

process._doublePUPPIJet_112_112_er2p4_dEtaMax1p6_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(114),
        minEta=cms.double(-2.252),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(114),
        minEta=cms.double(-2.251),
        maxEta=cms.double(2.4),
    ),
    maxDEta=cms.double(1.6),
)

process._tkMuonTkIsoEle_7_20_er2p4_dzMax1p0_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(9),
        minEta=cms.double(-2.25),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(22),
        minEta=cms.double(-2.249),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkMuonTkEle_7_23_er2p4_dzMax1p0_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(9),
        minEta=cms.double(-2.247),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(25),
        minEta=cms.double(-2.247),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkEleTkMuon_10_20_er2p4_dzMax1p0_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(12),
        minEta=cms.double(-2.246),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(22),
        minEta=cms.double(-2.245),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_27_18_er2p1_dzMax1p0_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(29),
        minEta=cms.double(-1.944),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(20),
        minEta=cms.double(-1.943),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_36_18_er2p1_dzMax1p0_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(38),
        minEta=cms.double(-1.942),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(20),
        minEta=cms.double(-1.941),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoElePUPPItau_22_29_er2p1_drMin0p3_dzMax1p0_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(24),
        minEta=cms.double(-1.94),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(31),
        minEta=cms.double(-1.939),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.25),
)

process._tkIsoElePUPPItau_22_39_er2p1_drMin0p3_dzMax1p0_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(24),
        minEta=cms.double(-1.938),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(41),
        minEta=cms.double(-1.937),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.26),
)

process._tkElePUPPIJet_28_40_er2p1_er2p4_dRmin0p3_dzMax1p0_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(30),
        minEta=cms.double(-1.936),
        maxEta=cms.double(2.1),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTPromptJets"),
        minPt=cms.double(42),
        minEta=cms.double(-2.235),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    minDR=cms.double(0.27),
)

process._doublePuppiJet_160_35_er5p0_massMin620_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(162),
        minEta=cms.double(-4.834),
        maxEta=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(37),
        minEta=cms.double(-4.833),
        maxEta=cms.double(3),
    ),
    minInvMass=cms.double(1.630),
)

process._doubleTkMuon_2_2_er1p5_drMax1p4_OS_dzMax1p0_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(4),
        minEta=cms.double(-1.332),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(4),
        minEta=cms.double(-1.331),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.4),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p4_drMax1p2_OS_dzMax1p0_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-2.23),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-2.229),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.2),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p0_massMin7_massMax18_OS_dzMax1p0_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-1.828),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(6),
        minEta=cms.double(-1.827),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    minInvMass=cms.double(1.18),
    maxInvMass=cms.double(1.72),
    os=cms.bool(True),
)

process._doubleEG_32_32_er2p5_Mt40_xxx_2 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(34),
        minEta=cms.double(-2.326),
        maxEta=cms.double(2.5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(34),
        minEta=cms.double(-2.325),
        maxEta=cms.double(2.5),
    ),
    minTransMass=cms.double(40),
)


process._triplePuppiJet_70_50_35_xxx_2 = l1tGTTripleObjectCond.clone(
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

process._tripleTkEleTkMuPUPPIJet_30_40_25_er2p4_xxx_2 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(32),
        minEta=cms.double(-2.223),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(42),
        minEta=cms.double(-2.223),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(27),
        minEta=cms.double(-2.222),
        maxEta=cms.double(2.4)
    )
)

process._tripleTkMuTkEle_7_5_5_er3p4_SS_xxx_2 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(9),
        minEta=cms.double(-3.221),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-3.21),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(7),
        minEta=cms.double(-3.219),
        maxEta=cms.double(3.4)
    ),
    delta12=cms.PSet(
        ss=cms.bool(True)
    ),
    delta13=cms.PSet(
        ss=cms.bool(True)
    )
)

process._quadTkMuTkEle_5_5_5_7_er3p4_SS_xxx_2 = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-3.218),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-3.217),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-3.21),
        maxEta=cms.double(3.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(9),
        minEta=cms.double(-3.215),
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

process._quadTkEleTkMuPUPPIJet_30_40_25_25_er2p4_xxx_2 = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(32),
        minEta=cms.double(-2.214),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(42),
        minEta=cms.double(-2.213),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(27),
        minEta=cms.double(-2.21),
        maxEta=cms.double(2.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(27),
        minEta=cms.double(-2.211),
        maxEta=cms.double(2.4)
    )
)



process._singleTkMu_14_er2p3_xxx_3 = l1tGTSingleObjectCond.clone(
    tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
    minPt=cms.double(17),
    minEta=cms.double(-2.11),
    maxEta=cms.double(2.3),
)

process._doubleJet_3_9_dEta_Max1p6_OS_xxx_3 = l1tGTDoubleObjectCond.clone(
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

process._doubleTau_5_9_q2_4_SS_xxx_3 = l1tGTDoubleObjectCond.clone(
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

process._doubleMu_11_9_q2_4_xxx_3 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuEl_11_9_q2_4_OS_xxx_3 = l1tGTDoubleObjectCond.clone(
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

process._doubleMu_11_9_combPt_19_xxx_3 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuEl_11_9_SS_xxx_3 = l1tGTDoubleObjectCond.clone(
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

process._doubleJetGamma_11_9_pr_0p2to1p8_1to3_xxx_3 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuTau_2_9_er_1to3_3to3p3_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(5),
        minEta=cms.double(1.191),
        maxEta=cms.double(3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(12),
        minEta=cms.double(3.192),
        maxEta=cms.double(3.3),
    ),
)

process._doubleMuEl_2_9_dEtaMin2_xxx_3 = l1tGTDoubleObjectCond.clone(
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

process._doubleElGamma_2_9_dPhiMin2_xxx_3 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuEl_2_9_dRMin2_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(12),
    ),
    minDR=cms.double(0.28),
)

process._doubleElTau_2_9_dEta0p2to2_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(12),
    ),
    minDEta=cms.double(0.21),
    maxDEta=cms.double(2),
)

process._doubleMuJet_2_9_dPhi2to4_xxx_3 = l1tGTDoubleObjectCond.clone(
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

process._doubleMuEl_2_9_dR1to3_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt=cms.double(12),
    )
    # minDR=cms.double(0.29),
    # maxDR=cms.double(3),
)

process._doubleMuGamma_11_9_massMax10_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(14),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Photons"),
        minPt=cms.double(12),
    ),
    maxInvMass=cms.double(1.76),
)

process._doubleElMu_11_9_mass10to600_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(14),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(12),
    ),
    minInvMass=cms.double(1.22),
    maxInvMass=cms.double(1.80),
)

process._doubleTkMu_15_7_er2p4_dzMax1p0_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(18),
        minEta=cms.double(-2.207),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.206),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoEleStaEG_22_12_er2p4_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(25),
        minEta=cms.double(-2.205),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(15),
        minEta=cms.double(-2.20),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkEle_25_12_er2p4_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(28),
        minEta=cms.double(-2.203),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTNonIsoEg"),
        minPt=cms.double(15),
        minEta=cms.double(-2.202),
        maxEta=cms.double(2.4),
    ),
)

process._doubleStaEG_37_24_er2p4_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(40),
        minEta=cms.double(-2.201),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTBsCandidates"),
        minPt=cms.double(27),
        minEta=cms.double(-2.19),
        maxEta=cms.double(2.4),
    ),
)

process._doubleTkIsoPhoton_22_12_er2p4_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(25),
        minEta=cms.double(-2.199),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(15),
        minEta=cms.double(-2.198),
        maxEta=cms.double(2.4),
    ),
)

process._doubleCaloTau_69_69_er2p1_drMin0p5_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(72),
        minEta=cms.double(-1.897),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(72),
        minEta=cms.double(-1.896),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.30),
)

process._doubleCaloTau_90_90_er2p1_drMin0p5_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(93),
        minEta=cms.double(-1.895),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTTaus"),
        minPt=cms.double(93),
        minEta=cms.double(-1.894),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.31),
)

process._doublePUPPITau_36_36_er2p1_drMin0p5_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(39),
        minEta=cms.double(-2),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(39),
        minEta=cms.double(-1.892),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.32),
)

process._doublePUPPITau_52_52_er2p1_drMin0p5_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(55),
        minEta=cms.double(-1.891),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(55),
        minEta=cms.double(-1.890),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.33),
)

process._doublePUPPIJet_112_112_er2p4_dEtaMax1p6_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(115),
        minEta=cms.double(-2.189),
        maxEta=cms.double(2.4),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(115),
        minEta=cms.double(-2.18),
        maxEta=cms.double(2.4),
    ),
    maxDEta=cms.double(2.6),
)

process._tkMuonTkIsoEle_7_20_er2p4_dzMax1p0_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.187),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(23),
        minEta=cms.double(-2.186),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkMuonTkEle_7_23_er2p4_dzMax1p0_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.185),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(26),
        minEta=cms.double(-2.18),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._tkEleTkMuon_10_20_er2p4_dzMax1p0_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(13),
        minEta=cms.double(-2.183),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(23),
        minEta=cms.double(-2.182),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_27_18_er2p1_dzMax1p0_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(30),
        minEta=cms.double(-1.881),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(21),
        minEta=cms.double(-1.880),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._puppiTauTkMuon_36_18_er2p1_dzMax1p0_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(39),
        minEta=cms.double(-1.879),
        maxEta=cms.double(2.1),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTSaPromptMuons"),
        minPt=cms.double(21),
        minEta=cms.double(-1.878),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
)

process._tkIsoElePUPPItau_22_29_er2p1_drMin0p3_dzMax1p0_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(25),
        minEta=cms.double(-1.877),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(32),
        minEta=cms.double(-1.876),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.34),
)

process._tkIsoElePUPPItau_22_39_er2p1_drMin0p3_dzMax1p0_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(25),
        minEta=cms.double(-1.875),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(42),
        minEta=cms.double(-1.874),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.35),
)

process._tkElePUPPIJet_28_40_er2p1_er2p4_dRmin0p3_dzMax1p0_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(31),
        minEta=cms.double(-1.873),
        maxEta=cms.double(2.1),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTPromptJets"),
        minPt=cms.double(43),
        minEta=cms.double(-2.17),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    minDR=cms.double(0.36),
)

process._doublePuppiJet_160_35_er5p0_massMin620_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(163),
        minEta=cms.double(-4.771),
        maxEta=cms.double(2.3),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(38),
        minEta=cms.double(-4.77),
        maxEta=cms.double(2.3),
    ),
    minInvMass=cms.double(1.633),
)

process._doubleTkMuon_2_2_er1p5_drMax1p4_OS_dzMax1p0_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-1.269),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(5),
        minEta=cms.double(-1.268),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.4),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p4_drMax1p2_OS_dzMax1p0_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.167),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-2.166),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.2),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p0_massMin7_massMax18_OS_dzMax1p0_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-1.765),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(7),
        minEta=cms.double(-1.764),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    minInvMass=cms.double(1.21),
    maxInvMass=cms.double(1.84),
    os=cms.bool(True),
)

process._doubleEG_32_32_er2p5_Mt40_xxx_3 = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(35),
        minEta=cms.double(-2.263),
        maxEta=cms.double(2.5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(35),
        minEta=cms.double(-2.262),
        maxEta=cms.double(2.5),
    ),
    minTransMass=cms.double(40),
)


process._triplePuppiJet_70_50_35_xxx_3 = l1tGTTripleObjectCond.clone(
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

process._tripleTkEleTkMuPUPPIJet_30_40_25_er2p4_xxx_3 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(33),
        minEta=cms.double(-2.161),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(43),
        minEta=cms.double(-2.16),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(28),
        minEta=cms.double(-2.159),
        maxEta=cms.double(2.4)
    )
)

process._tripleTkMuTkEle_7_5_5_er3p4_SS_xxx_3 = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-3.158),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-3.157),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(8),
        minEta=cms.double(-3.15),
        maxEta=cms.double(3.4)
    ),
    delta12=cms.PSet(
        ss=cms.bool(True)
    ),
    delta13=cms.PSet(
        ss=cms.bool(True)
    )
)

process._quadTkMuTkEle_5_5_5_7_er3p4_SS_xxx_3 = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-3.155),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-3.154),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-3.153),
        maxEta=cms.double(3.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(10),
        minEta=cms.double(-3.152),
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

process._quadTkEleTkMuPUPPIJet_30_40_25_25_er2p4_xxx_3 = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(33),
        minEta=cms.double(-2.151),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(43),
        minEta=cms.double(-2.15),
        maxEta=cms.double(2.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(28),
        minEta=cms.double(-2.149),
        maxEta=cms.double(2.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(28),
        minEta=cms.double(-2.14),
        maxEta=cms.double(2.4)
    )
)


process._tkIsoElePUPPItau_22_39_er2p1_drMin0p3_dzMax1p0_xxx_ext = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(28),
        minEta=cms.double(-1.847),
        maxEta=cms.double(2.1),
        minZ0=cms.double(-1.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(45),
        minEta=cms.double(-1.846),
        maxEta=cms.double(2.1),
    ),
    minDR=cms.double(0.37),
)

process._tkElePUPPIJet_28_40_er2p1_er2p4_dRmin0p3_dzMax1p0_xxx_ext = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(34),
        minEta=cms.double(-1.845),
        maxEta=cms.double(2.1),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GTTPromptJets"),
        minPt=cms.double(46),
        minEta=cms.double(-2.144),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    minDR=cms.double(0.1),
)

process._doublePuppiJet_160_35_er5p0_massMin620_xxx_ext = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(166),
        minEta=cms.double(-4.743),
        maxEta=cms.double(1.5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(41),
        minEta=cms.double(-4.742),
        maxEta=cms.double(1.5),
    ),
    minInvMass=cms.double(1.635),
)

process._doubleTkMuon_2_2_er1p5_drMax1p4_OS_dzMax1p0_xxx_ext = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-1.241),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(8),
        minEta=cms.double(-1.24),
        maxEta=cms.double(1.5),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.4),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p4_drMax1p2_OS_dzMax1p0_xxx_ext = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.139),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-2.138),
        maxEta=cms.double(2.4),
        maxZ0=cms.double(1.0),
    ),
    maxDR=cms.double(1.2),
    os=cms.bool(True),
)

process._doubleTkMuon_4_4_er2p0_massMin7_massMax18_OS_dzMax1p0_xxx_ext = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-1.737),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(10),
        minEta=cms.double(-1.736),
        maxEta=cms.double(2.0),
        maxZ0=cms.double(1.0),
    ),
    minInvMass=cms.double(1.10),
    os=cms.bool(True),
)

process._doubleEG_32_32_er2p5_Mt40_xxx_ext = l1tGTDoubleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(38),
        minEta=cms.double(-2.235),
        maxEta=cms.double(2.5),
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GCTIsoEg"),
        minPt=cms.double(38),
        minEta=cms.double(-2.234),
        maxEta=cms.double(2.5),
    ),
    minTransMass=cms.double(40),
)


process._triplePuppiJet_70_50_35_xxx_ext = l1tGTTripleObjectCond.clone(
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

process._tripleTkEleTkMuPUPPIJet_30_40_25_er2p4_xxx_ext = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(36),
        minEta=cms.double(-2.133),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(46),
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(31),
        minEta=cms.double(-2.13),
        maxEta=cms.double(2.4)
    )
)

process._tripleTkMuTkEle_7_5_5_er3p4_SS_xxx_ext = l1tGTTripleObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(13),
        minEta=cms.double(-3.131),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(11),
        minEta=cms.double(-3.13),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(11),
        minEta=cms.double(-3.129),
        maxEta=cms.double(3.4)
    ),
    delta12=cms.PSet(
        ss=cms.bool(True)
    )
)

process._quadTkMuTkEle_5_5_5_7_er3p4_SS_xxx_ext = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(11),
        minEta=cms.double(-3.128),
        maxEta=cms.double(3.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(11),
        minEta=cms.double(-3.127),
        maxEta=cms.double(3.4)
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(11),
        minEta=cms.double(-3.126),
        maxEta=cms.double(3.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(13),
        minEta=cms.double(-3.125),
        maxEta=cms.double(3.4)
    )
)

process._quadTkEleTkMuPUPPIJet_30_40_25_25_er2p4_xxx_ext = l1tGTQuadObjectCond.clone(
    collection1=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Electrons"),
        minPt=cms.double(36),
        minEta=cms.double(-2.12),
        maxEta=cms.double(2.4)
    ),
    collection2=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "GMTTkMuons"),
        minPt=cms.double(46),
    ),
    collection3=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Jets"),
        minPt=cms.double(31),
        minEta=cms.double(-2.122),
        maxEta=cms.double(2.4)
    ),
    collection4=cms.PSet(
        tag=cms.InputTag("l1tGTProducer", "CL2Taus"),
        minPt=cms.double(31),
        minEta=cms.double(-2.122),
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
