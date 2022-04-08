import FWCore.ParameterSet.Config as cms
from L1Trigger.Phase2L1GT.l1GTScales import *

l1GTSingleObjectCond = cms.EDFilter(
    "L1GTSingleObjectCond",
    scales=cms.PSet(
        pT_lsb=cms.double(kPT_lsb),
        phi_lsb=cms.double(kPhi_lsb),
        eta_lsb=cms.double(kEta_lsb),
        dZ_lsb=cms.double(kDZ_lsb),
        #dD_lsb=cms.double(kDD_lsb),
        beta_lsb=cms.double(kBeta_lsb),
        mass_lsb=cms.double(kMass_lsb),
        seed_pT_lsb=cms.double(kSeed_pT_lsb),
        seed_dZ_lsb=cms.double(kSeed_dZ_lsb),
        sca_sum_lsb=cms.double(kSca_sum_lsb),
        primvertdz_lsb=cms.double(kPrimvertdz_lsb),
        sum_pT_pv_lsb=cms.double(kSum_pT_pv_lsb),
        pos_chg=cms.int32(kPos_chg),
        neg_chg=cms.int32(kNeg_chg)
    )
)
