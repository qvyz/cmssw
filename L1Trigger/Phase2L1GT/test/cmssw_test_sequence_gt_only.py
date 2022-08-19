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
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(288))


process.GTProducer = cms.EDProducer(
    "L1GTTestProducer",
    outputFilename=cms.string("inputPattern"),
    random_seed=cms.uint32(0),
    maxLines=cms.uint32(4096),
    platform=cms.string("VU9P")
)

process.l1t_GTProducer = cms.Path(process.GTProducer)

from L1Trigger.Phase2L1GT.l1GTSingleInOutLUT import COSH_ETA_LUT, COSH_ETA_LUT_2, COS_PHI_LUT

COSH_ETA_LUT.export("coshEtaLUT.mem")
COSH_ETA_LUT_2.export("coshEtaLUT2.mem")
COS_PHI_LUT.export("cosPhiLUT.mem")

from L1Trigger.Phase2L1GT.l1GTSingleObjectCond_cfi import l1GTSingleObjectCond
from L1Trigger.Phase2L1GT.l1GTDoubleObjectCond_cfi import l1GTDoubleObjectCond
from L1Trigger.Phase2L1GT.l1GTTripleObjectCond_cfi import l1GTTripleObjectCond
from L1Trigger.Phase2L1GT.l1GTQuadObjectCond_cfi import l1GTQuadObjectCond

l1GTDoubleObjectCond.sanity_checks = cms.untracked.bool(True)
l1GTDoubleObjectCond.inv_mass_checks = cms.untracked.bool(True)

# Conditions

process._singleTkMu_14_er2p3 = l1GTSingleObjectCond.clone(
    pt_cut=cms.double(14),
    minEta_cut=cms.double(-2.3),
    maxEta_cut=cms.double(2.3),
    colTag=cms.InputTag("GTProducer", "GMT TkMuons"),
)

# process._doubleMu_11_11 = l1GTDoubleObjectCond.clone(
#     pt1_cut=cut_offset + i + 11,
#     pt2_cut=cms.double(11),
#     col1Tag=cms.InputTag("GTProducer", "GMT Tk Muons"),
# )

process._doubleJet_3_9_dEta_Max1p6_OS = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(3),
    pt2_cut=cms.double(9),
    dEtaMax_cut=cms.double(1.6),
    os_cut=cms.bool(True),
    col1Tag=cms.InputTag("GTProducer", "GCT Jets"),
    col2Tag=cms.InputTag("GTProducer", "GCT Jets"),
)

process._doubleTau_5_9_q2_4_SS = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(5),
    pt2_cut=cms.double(9),
    # qual1_cut         = 2,
    # qual2_cut         = 4,
    ss_cut=cms.bool(True),
    col1Tag=cms.InputTag("GTProducer", "CL2 Taus"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Taus"),
)

process._doubleMu_11_9_q2_4 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(11),
    pt2_cut=cms.double(9),
    # qual1_cut         = 2,
    # qual2_cut         = 4,
    col1Tag=cms.InputTag("GTProducer", "GMT SaPromptMuons"),
    col2Tag=cms.InputTag("GTProducer", "GMT SaPromptMuons"),
)

process._doubleMuEl_11_9_q2_4_OS = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(11),
    pt2_cut=cms.double(9),
    # qual1_cut         = 2,
    # qual2_cut         = 4,
    os_cut=cms.bool(True),
    col1Tag=cms.InputTag("GTProducer", "GMT SaPromptMuons"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Electrons"),
)

process._doubleMuGamma_11_9_OS = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(11),
    pt2_cut=cms.double(9),
    os_cut=cms.bool(True),
    col1Tag=cms.InputTag("GTProducer", "GMT TkMuons"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Electrons"),
)

process._doubleMuEl_11_9_SS = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(11),
    pt2_cut=cms.double(9),
    ss_cut=cms.bool(True),
    col1Tag=cms.InputTag("GTProducer", "GMT TkMuons"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Electrons"),
)
# TODO: Make sure this trigger fires sometimes (not) due to phi cut!!

process._doubleJetGamma_11_9_pr_0p2to1p8_1to3 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(11),
    pt2_cut=cms.double(9),
    minPhi1_cut=cms.double(0.2),
    maxPhi1_cut=cms.double(1.8),
    minPhi2_cut=cms.double(1),
    maxPhi2_cut=cms.double(3),
    col1Tag=cms.InputTag("GTProducer", "GCT IsoEg"),
    col2Tag=cms.InputTag("GTProducer", "GCT Jets"),
)

process._doubleMuTau_2_9_er_1to3_3to3p3 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(2),
    pt2_cut=cms.double(9),
    minEta1_cut=cms.double(1),
    maxEta1_cut=cms.double(3),
    minEta2_cut=cms.double(3),
    maxEta2_cut=cms.double(3.3),
    col1Tag=cms.InputTag("GTProducer", "GMT SaPromptMuons"),
    col2Tag=cms.InputTag("GTProducer", "GCT Jets"),
)

process._doubleMuEl_2_9_dEtaMin2 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(2),
    pt2_cut=cms.double(9),
    dEtaMin_cut=cms.double(2),
    col1Tag=cms.InputTag("GTProducer", "GMT SaPromptMuons"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Electrons"),
)

process._doubleElGamma_2_9_dPhiMin2 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(2),
    pt2_cut=cms.double(9),
    dPhiMin_cut=cms.double(2),
    col1Tag=cms.InputTag("GTProducer", "GCT IsoEg"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Taus"),
)

process._doubleMuEl_2_9_dRMin2 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(2),
    pt2_cut=cms.double(9),
    dRMin_cut=cms.double(2),
    col1Tag=cms.InputTag("GTProducer", "GMT SaPromptMuons"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Electrons"),
)

process._doubleElTau_2_9_dEta0p2to2 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(2),
    pt2_cut=cms.double(9),
    dEtaMin_cut=cms.double(0.2),
    dEtaMax_cut=cms.double(2),
    col1Tag=cms.InputTag("GTProducer", "GCT Taus"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Electrons"),
)

process._doubleMuJet_2_9_dPhi2to4 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(2),
    pt2_cut=cms.double(9),
    dPhiMin_cut=cms.double(2),
    dPhiMax_cut=cms.double(4),
    col1Tag=cms.InputTag("GTProducer", "GMT SaPromptMuons"),
    col2Tag=cms.InputTag("GTProducer", "GCT Jets"),
)

process._doubleMuEl_2_9_dR1to3 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(2),
    pt2_cut=cms.double(9),
    dRMin_cut=cms.double(1),
    dRMax_cut=cms.double(3),
    col1Tag=cms.InputTag("GTProducer", "GMT SaPromptMuons"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Photons"),
)

process._doubleMuGamma_11_9_massMax10 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(11),
    pt2_cut=cms.double(9),
    invMassMax_cut=cms.double(10),
    col1Tag=cms.InputTag("GTProducer", "GMT SaPromptMuons"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Photons"),
)

process._doubleElMu_11_9_mass10to600 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(11),
    pt2_cut=cms.double(9),
    invMassMin_cut=cms.double(10),
    invMassMax_cut=cms.double(600),
    col1Tag=cms.InputTag("GTProducer", "CL2 Electrons"),
    col2Tag=cms.InputTag("GTProducer", "GMT SaPromptMuons"),
)

process._doubleTkMu_15_7_er2p4_dzMax1p0 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(15),
    pt2_cut=cms.double(7),
    minEta1_cut=cms.double(-2.4),
    maxEta1_cut=cms.double(2.4),
    minEta2_cut=cms.double(-2.4),
    maxEta2_cut=cms.double(2.4),
    maxDz1_cut=cms.double(1.0),
    maxDz2_cut=cms.double(1.0),
    col1Tag=cms.InputTag("GTProducer", "GMT TkMuons"),
    col2Tag=cms.InputTag("GTProducer", "GMT TkMuons"),
)

process._tkIsoEleStaEG_22_12_er2p4 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(22),
    pt2_cut=cms.double(12),
    minEta1_cut=cms.double(-2.4),
    maxEta1_cut=cms.double(2.4),
    minEta2_cut=cms.double(-2.4),
    maxEta2_cut=cms.double(2.4),
    col1Tag=cms.InputTag("GTProducer", "GCT IsoEg"),
    col2Tag=cms.InputTag("GTProducer", "GCT NonIsoEg"),
)

process._doubleTkEle_25_12_er2p4 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(25),
    pt2_cut=cms.double(12),
    minEta1_cut=cms.double(-2.4),
    maxEta1_cut=cms.double(2.4),
    minEta2_cut=cms.double(-2.4),
    maxEta2_cut=cms.double(2.4),
    col1Tag=cms.InputTag("GTProducer", "GCT NonIsoEg"),
    col2Tag=cms.InputTag("GTProducer", "GCT NonIsoEg"),
)

process._doubleStaEG_37_24_er2p4 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(37),
    pt2_cut=cms.double(24),
    minEta1_cut=cms.double(-2.4),
    maxEta1_cut=cms.double(2.4),
    minEta2_cut=cms.double(-2.4),
    maxEta2_cut=cms.double(2.4),
    col1Tag=cms.InputTag("GTProducer", "GTT BsCandidates"),
    col2Tag=cms.InputTag("GTProducer", "GTT BsCandidates"),
)

process._doubleTkIsoPhoton_22_12_er2p4 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(22),
    pt2_cut=cms.double(12),
    minEta1_cut=cms.double(-2.4),
    maxEta1_cut=cms.double(2.4),
    minEta2_cut=cms.double(-2.4),
    maxEta2_cut=cms.double(2.4),
    col1Tag=cms.InputTag("GTProducer", "GCT IsoEg"),
    col2Tag=cms.InputTag("GTProducer", "GCT IsoEg"),
)

process._doubleCaloTau_69_69_er2p1_drMin0p5 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(69),
    pt2_cut=cms.double(69),
    minEta1_cut=cms.double(-2.1),
    maxEta1_cut=cms.double(2.1),
    minEta2_cut=cms.double(-2.1),
    maxEta2_cut=cms.double(2.1),
    dRMin_cut=cms.double(0.5),
    col1Tag=cms.InputTag("GTProducer", "GCT Taus"),
    col2Tag=cms.InputTag("GTProducer", "GCT Taus"),
)

process._doubleCaloTau_90_90_er2p1_drMin0p5 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(90),
    pt2_cut=cms.double(90),
    minEta1_cut=cms.double(-2.1),
    maxEta1_cut=cms.double(2.1),
    minEta2_cut=cms.double(-2.1),
    maxEta2_cut=cms.double(2.1),
    dRMin_cut=cms.double(0.5),
    col1Tag=cms.InputTag("GTProducer", "GCT Taus"),
    col2Tag=cms.InputTag("GTProducer", "GCT Taus"),
)

process._doublePUPPITau_36_36_er2p1_drMin0p5 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(36),
    pt2_cut=cms.double(36),
    minEta1_cut=cms.double(-2.1),
    maxEta1_cut=cms.double(2.1),
    minEta2_cut=cms.double(-2.1),
    maxEta2_cut=cms.double(2.1),
    dRMin_cut=cms.double(0.5),
    col1Tag=cms.InputTag("GTProducer", "CL2 Taus"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Taus"),
)

process._doublePUPPITau_52_52_er2p1_drMin0p5 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(52),
    pt2_cut=cms.double(52),
    minEta1_cut=cms.double(-2.1),
    maxEta1_cut=cms.double(2.1),
    minEta2_cut=cms.double(-2.1),
    maxEta2_cut=cms.double(2.1),
    dRMin_cut=cms.double(0.5),
    col1Tag=cms.InputTag("GTProducer", "CL2 Taus"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Taus"),
)

process._doublePUPPIJet_112_112_er2p4_dEtaMax1p6 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(112),
    pt2_cut=cms.double(112),
    minEta1_cut=cms.double(-2.4),
    maxEta1_cut=cms.double(2.4),
    minEta2_cut=cms.double(-2.4),
    maxEta2_cut=cms.double(2.4),
    dEtaMax_cut=cms.double(1.6),
    col1Tag=cms.InputTag("GTProducer", "CL2 Jets"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Jets"),
)

process._tkMuonTkIsoEle_7_20_er2p4_dzMax1p0 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(7),
    pt2_cut=cms.double(20),
    minEta1_cut=cms.double(-2.4),
    maxEta1_cut=cms.double(2.4),
    minEta2_cut=cms.double(-2.4),
    maxEta2_cut=cms.double(2.4),
    maxDz1_cut=cms.double(1.0),
    maxDz2_cut=cms.double(1.0),
    col1Tag=cms.InputTag("GTProducer", "GMT SaPromptMuons"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Electrons"),
)

process._tkMuonTkEle_7_23_er2p4_dzMax1p0 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(7),
    pt2_cut=cms.double(23),
    minEta1_cut=cms.double(-2.4),
    maxEta1_cut=cms.double(2.4),
    minEta2_cut=cms.double(-2.4),
    maxEta2_cut=cms.double(2.4),
    maxDz1_cut=cms.double(1.0),
    maxDz2_cut=cms.double(1.0),
    col1Tag=cms.InputTag("GTProducer", "GMT SaPromptMuons"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Electrons"),
)

process._tkEleTkMuon_10_20_er2p4_dzMax1p0 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(10),
    pt2_cut=cms.double(20),
    minEta1_cut=cms.double(-2.4),
    maxEta1_cut=cms.double(2.4),
    minEta2_cut=cms.double(-2.4),
    maxEta2_cut=cms.double(2.4),
    maxDz1_cut=cms.double(1.0),
    maxDz2_cut=cms.double(1.0),
    col1Tag=cms.InputTag("GTProducer", "CL2 Electrons"),
    col2Tag=cms.InputTag("GTProducer", "GMT TkMuons"),
)

process._puppiTauTkMuon_27_18_er2p1_dzMax1p0 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(27),
    pt2_cut=cms.double(18),
    minEta1_cut=cms.double(-2.1),
    maxEta1_cut=cms.double(2.1),
    minEta2_cut=cms.double(-2.1),
    maxEta2_cut=cms.double(2.1),
    minDz2_cut=cms.double(-1.0),
    maxDz2_cut=cms.double(1.0),
    col1Tag=cms.InputTag("GTProducer", "CL2 Taus"),
    col2Tag=cms.InputTag("GTProducer", "GMT SaPromptMuons"),
)

process._puppiTauTkMuon_36_18_er2p1_dzMax1p0 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(36),
    pt2_cut=cms.double(18),
    minEta1_cut=cms.double(-2.1),
    maxEta1_cut=cms.double(2.1),
    minEta2_cut=cms.double(-2.1),
    maxEta2_cut=cms.double(2.1),
    minDz2_cut=cms.double(-1.0),
    maxDz2_cut=cms.double(1.0),
    col1Tag=cms.InputTag("GTProducer", "CL2 Taus"),
    col2Tag=cms.InputTag("GTProducer", "GMT SaPromptMuons"),
)

process._tkIsoElePUPPItau_22_29_er2p1_drMin0p3_dzMax1p0 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(22),
    pt2_cut=cms.double(29),
    minEta1_cut=cms.double(-2.1),
    maxEta1_cut=cms.double(2.1),
    minEta2_cut=cms.double(-2.1),
    maxEta2_cut=cms.double(2.1),
    dRMin_cut=cms.double(0.3),
    minDz1_cut=cms.double(-1.0),
    maxDz1_cut=cms.double(1.0),
    col1Tag=cms.InputTag("GTProducer", "CL2 Electrons"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Taus"),
)

process._tkIsoElePUPPItau_22_39_er2p1_drMin0p3_dzMax1p0 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(22),
    pt2_cut=cms.double(39),
    minEta1_cut=cms.double(-2.1),
    maxEta1_cut=cms.double(2.1),
    minEta2_cut=cms.double(-2.1),
    maxEta2_cut=cms.double(2.1),
    dRMin_cut=cms.double(0.3),
    minDz1_cut=cms.double(-1.0),
    maxDz1_cut=cms.double(1.0),
    col1Tag=cms.InputTag("GTProducer", "CL2 Electrons"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Taus"),
)

process._tkElePUPPIJet_28_40_er2p1_er2p4_dRmin0p3_dzMax1p0 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(28),
    pt2_cut=cms.double(40),
    minEta1_cut=cms.double(-2.1),
    maxEta1_cut=cms.double(2.1),
    minEta2_cut=cms.double(-2.4),
    maxEta2_cut=cms.double(2.4),
    dRMin_cut=cms.double(0.3),
    maxDz1_cut=cms.double(1.0),
    maxDz2_cut=cms.double(1.0),
    col1Tag=cms.InputTag("GTProducer", "CL2 Electrons"),
    col2Tag=cms.InputTag("GTProducer", "GTT PromptJets"),
)

process._doublePuppiJet_160_35_er5p0_massMin620 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(160),
    pt2_cut=cms.double(35),
    minEta1_cut=cms.double(-5.0),
    maxEta1_cut=cms.double(5.0),
    minEta2_cut=cms.double(-5.0),
    maxEta2_cut=cms.double(5.0),
    invMassMin_cut=cms.double(620),
    col1Tag=cms.InputTag("GTProducer", "CL2 Jets"),
    col2Tag=cms.InputTag("GTProducer", "CL2 Jets"),
)

process._doubleTkMuon_2_2_er1p5_drMax1p4_OS_dzMax1p0 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(2),
    pt2_cut=cms.double(2),
    minEta1_cut=cms.double(-1.5),
    maxEta1_cut=cms.double(1.5),
    minEta2_cut=cms.double(-1.5),
    maxEta2_cut=cms.double(1.5),
    dRMax_cut=cms.double(1.4),
    os_cut=cms.bool(True),
    maxDz1_cut=cms.double(1.0),
    maxDz2_cut=cms.double(1.0),
    col1Tag=cms.InputTag("GTProducer", "GMT TkMuons"),
    col2Tag=cms.InputTag("GTProducer", "GMT TkMuons"),
)

process._doubleTkMuon_4_4_er2p4_drMax1p2_OS_dzMax1p0 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(4),
    pt2_cut=cms.double(4),
    minEta1_cut=cms.double(-2.4),
    maxEta1_cut=cms.double(2.4),
    minEta2_cut=cms.double(-2.4),
    maxEta2_cut=cms.double(2.4),
    dRMax_cut=cms.double(1.2),
    os_cut=cms.bool(True),
    maxDz1_cut=cms.double(1.0),
    maxDz2_cut=cms.double(1.0),
    col1Tag=cms.InputTag("GTProducer", "GMT TkMuons"),
    col2Tag=cms.InputTag("GTProducer", "GMT TkMuons"),
)

process._doubleTkMuon_4_4_er2p0_massMin7_massMax18_OS_dzMax1p0 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(4),
    pt2_cut=cms.double(4),
    minEta1_cut=cms.double(-2.0),
    maxEta1_cut=cms.double(2.0),
    minEta2_cut=cms.double(-2.0),
    maxEta2_cut=cms.double(2.0),
    invMassMin_cut=cms.double(7),
    invMassMax_cut=cms.double(18),
    os_cut=cms.bool(True),
    maxDz1_cut=cms.double(1.0),
    maxDz2_cut=cms.double(1.0),
    col1Tag=cms.InputTag("GTProducer", "GMT TkMuons"),
    col2Tag=cms.InputTag("GTProducer", "GMT TkMuons"),
)

process._doubleEG_32_32_er2p5_Mt40 = l1GTDoubleObjectCond.clone(
    pt1_cut=cms.double(32),
    pt2_cut=cms.double(32),
    minEta1_cut=cms.double(-2.5),
    maxEta1_cut=cms.double(2.5),
    transMassMin_cut=cms.double(40),
    col1Tag=cms.InputTag("GTProducer", "GCT IsoEg"),
    col2Tag=cms.InputTag("GTProducer", "GCT IsoEg"),
)


channel_conf = {}
idx = 0
# remove '_', since it are not allowed for module names
for filt_name in process.filters:
    if filt_name[:1] != '_':
        continue
    new_name = filt_name.replace('_', '')
    setattr(process, new_name, getattr(process, filt_name).clone())
    delattr(process, filt_name)
    channel_conf[idx] = 'l1t' + filt_name
    setattr(process, 'l1t' + filt_name, cms.Path(getattr(process, new_name)))
    idx += 1

# process.tripleTkEle20TkPho18Jet11 = l1GTTripleObjectCond.clone(
#     col1Tag = cms.InputTag("GTProducer", "CL2 Electrons"),
#     col2Tag = cms.InputTag("GTProducer", "CL2 Photons"),
#     col3Tag = cms.InputTag("GTProducer", "CL2 Jets"),
#     pt1_cut = cms.double(20),
#     pt2_cut = cms.double(18),
#     pt3_cut = cms.double(11),
# )

# process.quadTkEle20 = l1GTQuadObjectCond.clone(
#     col1Tag = cms.InputTag("GTProducer", "CL2 Electrons"),
#     col2Tag = cms.InputTag("GTProducer", "CL2 Electrons"),
#     col3Tag = cms.InputTag("GTProducer", "CL2 Electrons"),
#     col4Tag = cms.InputTag("GTProducer", "CL2 Electrons"),
#     pt1_cut = cms.double(20),
#     pt2_cut = cms.double(20),
#     pt3_cut = cms.double(20),
#     pt4_cut = cms.double(20),
# )


# Algo bits
from L1Trigger.Phase2L1GT.l1GTAlgoChannelConfig import generate_channel_config


process.BoardData = cms.EDAnalyzer("L1GTBoardWriter",
  outputFilename = cms.string("outputPattern"),
  maxLines = cms.uint32(4096),
  channelConfig = generate_channel_config({
        0 : channel_conf
    })
)

process.l1t_BoardData = cms.EndPath(process.BoardData)

process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('file:test_output.root'),
    outputCommands = cms.untracked.vstring('keep *'),
    splitLevel = cms.untracked.int32(0)
)

process.output_step = cms.EndPath(process.output)
