import FWCore.ParameterSet.Config as cms

l1GTBoardWriter = cms.EDAnalyzer("L1GTBoardWriter",
  maxLines = cms.uint32(1024),
  outputFilename = cms.string("outputPatterns")
)

def _clone(self, **kwargs):
    print('Clone called')
    return super(self).clone(kwargs)

l1GTBoardWriter.clone = _clone
