#include "L1GTScales.h"

namespace l1t {
  L1GTScales::L1GTScales(double pT_lsb,
                         double phi_lsb,
                         double eta_lsb,
                         double dZ_lsb,
                         //double dD_lsb,
                         double beta_lsb,
                         double mass_lsb,
                         double seed_pT_lsb,
                         double seed_dZ_lsb,
                         double sca_sum_lsb,
                         double primvertdz_lsb,
                         double sum_pT_pv_lsb,
                         int pos_chg,
                         int neg_chg,
                         uint32_t lut_scale)
      : pT_lsb_(pT_lsb),
        phi_lsb_(phi_lsb),
        eta_lsb_(eta_lsb),
        dZ_lsb_(dZ_lsb),
        //dD_lsb_(dD_lsb),
        beta_lsb_(beta_lsb),
        mass_lsb_(mass_lsb),
        seed_pT_lsb_(seed_pT_lsb),
        seed_dZ_lsb_(seed_dZ_lsb),
        sca_sum_lsb_(sca_sum_lsb),
        primvertdz_lsb_(primvertdz_lsb),
        sum_pT_pv_lsb_(sum_pT_pv_lsb),
        pos_chg_(pos_chg),
        neg_chg_(neg_chg),
        lut_scale_(lut_scale) {}

  L1GTScales::L1GTScales(const edm::ParameterSet& config, uint32_t lut_scale)
      : pT_lsb_(config.getParameter<double>("pT_lsb")),
        phi_lsb_(config.getParameter<double>("phi_lsb")),
        eta_lsb_(config.getParameter<double>("eta_lsb")),
        dZ_lsb_(config.getParameter<double>("dZ_lsb")),
        //dD_lsb_(config.getParameter<double>("dD_lsb")),
        beta_lsb_(config.getParameter<double>("beta_lsb")),
        mass_lsb_(config.getParameter<double>("mass_lsb")),
        seed_pT_lsb_(config.getParameter<double>("seed_pT_lsb")),
        seed_dZ_lsb_(config.getParameter<double>("seed_dZ_lsb")),
        sca_sum_lsb_(config.getParameter<double>("sca_sum_lsb")),
        primvertdz_lsb_(config.getParameter<double>("primvertdz_lsb")),
        sum_pT_pv_lsb_(config.getParameter<double>("sum_pT_pv_lsb")),
        pos_chg_(config.getParameter<int>("pos_chg")),
        neg_chg_(config.getParameter<int>("neg_chg")),
        lut_scale_(lut_scale) {}

  void L1GTScales::fillDescriptions(edm::ParameterSetDescription& desc) {
    desc.add<double>("pT_lsb");
    desc.add<double>("phi_lsb");
    desc.add<double>("eta_lsb");
    desc.add<double>("dZ_lsb");
    //desc.add<double>("dD_lsb");
    desc.add<double>("beta_lsb");
    desc.add<double>("mass_lsb");
    desc.add<double>("seed_pT_lsb");
    desc.add<double>("seed_dZ_lsb");
    desc.add<double>("sca_sum_lsb");
    desc.add<double>("primvertdz_lsb");
    desc.add<double>("sum_pT_pv_lsb");
    desc.add<int>("pos_chg");
    desc.add<int>("neg_chg");
  }

}  // namespace l1t
