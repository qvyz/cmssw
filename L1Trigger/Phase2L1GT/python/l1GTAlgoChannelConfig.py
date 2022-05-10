import FWCore.ParameterSet.Config as cms

def generate_channel_config(algosDict: 'dict[int, dict[int, str]]') -> cms.VPSet:
    config = []
    for channel, algos in algosDict.items():
        algoBits = []
        for bit, path in algos.items():
            algoBits += [
                cms.PSet(
                    bit=cms.uint32(bit),
                    path=cms.string(path)
                )]
                
        config += [cms.PSet(
            channel=cms.uint32(channel),
            algoBits=cms.VPSet(*algoBits)
        )]

    return cms.VPSet(*config)
