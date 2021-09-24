import FWCore.ParameterSet.Config as cms
import GT_translationfunctions as gt
import test_Phase2L1THLT
import inspect
from test_Phase2L1THLT import globtrig
from test_Phase2L1THLT import process

globtrig.importjson("GT_config_to_vhdl.json")
globtrig.getParameters(process)
globtrig.printvhdl()

