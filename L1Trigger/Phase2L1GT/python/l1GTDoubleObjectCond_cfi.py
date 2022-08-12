import FWCore.ParameterSet.Config as cms
from L1Trigger.Phase2L1GT.l1GTScales import *
from L1Trigger.Phase2L1GT.l1GTSingleInOutLUT import COS_PHI_LUT, COSH_ETA_LUT, COSH_ETA_LUT_2


l1GTDoubleObjectCond = cms.EDFilter(
    "L1GTDoubleObjectCond",
    scales=cms.PSet(
        pT_lsb=cms.double(kPT_lsb),
        phi_lsb=cms.double(kPhi_lsb),
        eta_lsb=cms.double(kEta_lsb),
        dZ_lsb=cms.double(kDZ_lsb),
        #dD_lsb = cms.double(kDD_lsb),
        beta_lsb=cms.double(kBeta_lsb),
        mass_lsb=cms.double(kMass_lsb),
        seed_pT_lsb=cms.double(kSeed_pT_lsb),
        seed_dZ_lsb=cms.double(kSeed_dZ_lsb),
        sca_sum_lsb=cms.double(kSca_sum_lsb),
        primvertdz_lsb=cms.double(kPrimvertdz_lsb),
        sum_pT_pv_lsb=cms.double(kSum_pT_pv_lsb),
        pos_chg=cms.int32(kPos_chg),
        neg_chg=cms.int32(kNeg_chg)
    ),
    cosh_eta_lut=COSH_ETA_LUT.config(),
    cosh_eta_lut2=COSH_ETA_LUT_2.config(),
    cos_phi_lut=COS_PHI_LUT.config(),
    sanity_checks=cms.untracked.bool(False),
    inv_mass_checks=cms.untracked.bool(False)
)
