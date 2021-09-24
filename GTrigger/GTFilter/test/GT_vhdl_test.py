import FWCore.ParameterSet.Config as cms
import GT_translationfunctions as gt
import inspect
from GT_config_test import globtrig
from GT_config_test import process

globtrig.importjson("GT_config_to_vhdl.json")
globtrig.getParameters(process)
globtrig.printvhdl()

