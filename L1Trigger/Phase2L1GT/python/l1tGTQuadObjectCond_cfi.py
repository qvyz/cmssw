import FWCore.ParameterSet.Config as cms
from L1Trigger.Phase2L1GT.l1tGTScales import scale_parameter

l1tGTQuadObjectCond = cms.EDFilter(
    "L1GTQuadObjectCond",
    scales=scale_parameter
)
