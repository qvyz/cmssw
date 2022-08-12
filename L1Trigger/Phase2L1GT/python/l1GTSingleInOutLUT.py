"""
This computes the most optimal COS_PHI_LUT and COSH_ETA_LUT. Call 
:func:`~l1GTSingleInOutLUT.L1TSingleInOutLUT.export` to export the
generated LUT.
"""

import FWCore.ParameterSet.Config as cms
from L1Trigger.Phase2L1GT.l1GTScales import *
from statistics import mean, median, stdev
import math


class L1TSingleInOutLUT:

    def __init__(self, width_in, unused_lsbs, lsb, output_scale_factor, operation, start_value=0, label=""):
        input_scale_factor = 2**unused_lsbs * lsb
        self.unused_lsbs = unused_lsbs
        self.lsb = lsb
        signed_output = min([operation(input_scale_factor * i + start_value)
                            for i in range(2**width_in)]) < 0

        self.width_out = math.ceil(math.log2(output_scale_factor *
                                             max([abs(operation(input_scale_factor * (i + 0.5) + start_value)) for i in range(2**width_in)])))

        if signed_output:
            self.width_out += 1

        if not "l1GTDoubleObjectCond_cfi" in __name__:
            print("***************************** {} LUT {} *****************************".format(operation.__name__, label))
            print("LUT depth: {} x {} (addr x data)".format(width_in, self.width_out))

        self.width_in = width_in
        self.output_scale_factor = output_scale_factor
        self.input_scale_factor = input_scale_factor
        self.operation = operation
        self.start_value = start_value
        self.lut = cms.vint32(
            *[round(output_scale_factor * operation(input_scale_factor * (i + 0.5) + start_value)) for i in range(2**width_in)])

        self.print_error()

    def config(self):
        return cms.PSet(
            output_scale_factor=cms.double(self.output_scale_factor),
            unused_lsbs=cms.uint32(self.unused_lsbs),
            lut=self.lut,
            max_error=cms.double(self.max_error)
        )

    def export(self, filename: str):
        with open(filename, "w") as file:
            for address, value in enumerate(self.lut):
                file.write("@{:x} {:x}\n".format(address, int(value) & ((1 << self.width_out) - 1)))

    @staticmethod
    def optimal_scale_factor(width_in, max_width_out, unused_lsbs, lsb, operation, start_value=0):
        input_scale_factor = 2**unused_lsbs * lsb
        scale_factor = (2**max_width_out - 1) / \
            max([abs(operation(input_scale_factor * (i + 0.5) + start_value)) for i in range(2**width_in)])
        if 'DEBUG' in globals() and DEBUG == True:
            print("{} LUT optimal scale factor:".format(operation.__name__), scale_factor)
        return scale_factor

    def print_error(self):
        errors = [abs(self.lut[int(i/(2**self.unused_lsbs))]/self.output_scale_factor -
                      self.operation(i * self.lsb + self.start_value)) for i in range(2**(self.width_in + self.unused_lsbs))]

        self.max_error = max(errors)

        if not "l1GTDoubleObjectCond_cfi" in __name__:
            print("LUT error: {:.5f} +/- {:.5f}, max: {:.5f}, total: {:.5f}, median: {:.5f}".format(
                mean(errors), stdev(errors), self.max_error, sum(errors), median(errors)))

        # mass_errors = [errors[i]/(2*self.operation(i * self.lsb + self.start_value)) for i in range(2**(self.width_in + self.unused_lsbs)) ]
        # print("inv mass error: {:.5f} +/- {:.5f}, max: {:.5f}, total: {:.5f}, median: {:.5f}".format(
        #       mean(mass_errors), stdev(mass_errors), max(mass_errors), sum(mass_errors), median(mass_errors)))


COS_PHI_IN_WIDTH = 11  # not using 2 lsb
COSH_ETA_IN_WIDTH = 11  # not using 2 lsb and 1 msb (splitted LUT)

# Since we calculate cosh(dEta) - cos(dPhi); both must be on the same scale
optimal_scale_factor = math.floor(min(L1TSingleInOutLUT.optimal_scale_factor(COS_PHI_IN_WIDTH, 17, 2, kPhi_lsb, math.cos),
                                      L1TSingleInOutLUT.optimal_scale_factor(COSH_ETA_IN_WIDTH, 17, 2, kEta_lsb, math.cosh)))

if 'DEBUG' in globals() and DEBUG == True:
    print("LUT combined optimal scale factor: ", optimal_scale_factor)

COS_PHI_LUT = L1TSingleInOutLUT(
    COS_PHI_IN_WIDTH, 2, kPhi_lsb, optimal_scale_factor, math.cos)

# eta in [0, 2pi)
COSH_ETA_LUT = L1TSingleInOutLUT(
    COSH_ETA_IN_WIDTH, 2, kEta_lsb, optimal_scale_factor, math.cosh, 0, "[0, 2pi)")

# eta in [2pi, 4pi)
COSH_ETA_LUT_2 = L1TSingleInOutLUT(
    COSH_ETA_IN_WIDTH, 2, kEta_lsb,
    L1TSingleInOutLUT.optimal_scale_factor(
        COSH_ETA_IN_WIDTH, 17, 2, kEta_lsb, math.cosh, 2**13 * kEta_lsb),
    math.cosh, 2**13 * kEta_lsb, "[2pi, 4pi)")
