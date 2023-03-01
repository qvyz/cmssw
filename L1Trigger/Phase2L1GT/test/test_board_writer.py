

import L1Trigger.Phase2L1GT.VHDLWriter.Conversions as conversions
import L1Trigger.Phase2L1GT.VHDLWriter.Writer as writer
from gt_firmware_evaluation import process as gt
from gt_firmware_evaluation import algobit_conf as algobitmap

knownfilters = dict()
logicalcombinations = dict()
distributedalgos = dict()
knownfilters = conversions.getConditionsfromConfig(gt)
logicalcombinations = conversions.getLogicalFilters(gt,knownfilters)
algoblocks = conversions.writeAlgoblocks(knownfilters,logicalcombinations)
distributedalgos = conversions.distributeAlgos(algoblocks,4)
conversions.writeAlgounits(distributedalgos,algobitmap,knownfilters,logicalcombinations)
distributed_algomap = conversions.getAlgobits(algobitmap,distributedalgos,[0,24,32,48])

for algo in distributedalgos:
  print(algo.ResourceUseage.printResources())


import FWCore.ParameterSet.Config as cms




process = cms.Process('L1Test2')

# Input source
process.source = cms.Source("PoolSource", fileNames=cms.untracked.vstring(("file:test_output.root")))


# Algo bits
from L1Trigger.Phase2L1GT.l1tGTAlgoChannelConfig import generate_channel_config

process.BoardData = cms.EDAnalyzer("L1GTBoardWriter",
  outputFilename = cms.string("outputPattern"),
  maxLines = cms.uint32(1024),
  processName = cms.string("L1Test"),
  channelConfig = generate_channel_config(
  distributed_algomap
    )
)
process.l1t_BoardData = cms.Path(process.BoardData)
