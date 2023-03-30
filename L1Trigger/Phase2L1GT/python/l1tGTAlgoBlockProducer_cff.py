import FWCore.ParameterSet.Config as cms
import re

algorithms = cms.VPSet()

l1tGTAlgoBlockProducer = cms.EDProducer(
    "L1GTAlgoBlockProducer",
    algorithms = algorithms
)

def collectAlgorithmPaths(process) -> tuple[cms.Path]:
    str_paths = set()
    for algorithm in algorithms:
        algo_paths = re.findall(r"(?i)(?!(?:not|and|or|xor))\b\w+", algorithm.expression.value())
        str_paths.add(*algo_paths)

    paths = set()

    for str_path in str_paths:
        paths.add(getattr(process, str_path))

    return tuple(paths)
