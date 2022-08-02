#ifndef L1GTScales_h
#define L1GTScales_h

#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include <cmath>
#include <cinttypes>

namespace l1t {
  class L1GTScales {
  public:
    L1GTScales(double pT_lsb,
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
               uint32_t lut_scale);

    L1GTScales(const edm::ParameterSet &, uint32_t lut_scale = 1);

    static void fillDescriptions(edm::ParameterSetDescription &);

    int to_hw_pT(double value) const { return std::round(value / pT_lsb_); };
    int to_hw_phi(double value) const { return std::round(value / phi_lsb_); };
    int to_hw_eta(double value) const { return std::round(value / eta_lsb_); };
    int to_hw_dZ(double value) const { return std::round(value / dZ_lsb_); };
    //int to_hw_dD(double value) const { return std::round(value / dD_lsb_); };
    int to_hw_beta(double value) const { return std::round(value / beta_lsb_); };
    int to_hw_mass(double value) const { return std::round(value / mass_lsb_); };
    int to_hw_seed_pT(double value) const { return std::round(value / seed_pT_lsb_); };
    int to_hw_seed_dZ(double value) const { return std::round(value / seed_dZ_lsb_); };
    int to_hw_sca_sum(double value) const { return std::round(value / sca_sum_lsb_); };
    int to_hw_primvertdz(double value) const { return std::round(value / primvertdz_lsb_); };
    int to_hw_sum_pT_pv(double value) const { return std::round(value / sum_pT_pv_lsb_); };

    int to_hw_RSquared(double value) const { return std::round(value / (eta_lsb_ * eta_lsb_ + phi_lsb_ * phi_lsb_)); }

    int to_hw_InvMass(double value) const { return std::round(value / (pT_lsb_ * pT_lsb_)) * lut_scale_; }
    int to_hw_TransMass(double value) const { return std::round(value / (pT_lsb_ * pT_lsb_)) * lut_scale_; }

    double pT_lsb() const { return pT_lsb_; }
    double phi_lsb() const { return phi_lsb_; }
    double eta_lsb() const { return eta_lsb_; }
    double dZ_lsb() const { return dZ_lsb_; }
    //const double dD_lsb_;
    double beta_lsb() const { return beta_lsb_; }
    double mass_lsb() const { return mass_lsb_; }
    double seed_pT_lsb() const { return seed_pT_lsb_; }
    double seed_dZ_lsb() const { return seed_dZ_lsb_; }
    double sca_sum_lsb() const { return sca_sum_lsb_; }
    double primvertdz_lsb() const { return primvertdz_lsb_; }
    double sum_pT_pv_lsb() const { return sum_pT_pv_lsb_; }
    int pos_chg() const { return pos_chg_; }
    int neg_chg() const { return neg_chg_; }
    uint32_t lut_scale() const { return lut_scale_; }

  private:
    const double pT_lsb_;
    const double phi_lsb_;
    const double eta_lsb_;
    const double dZ_lsb_;
    //const double dD_lsb_;
    const double beta_lsb_;
    const double mass_lsb_;
    const double seed_pT_lsb_;
    const double seed_dZ_lsb_;
    const double sca_sum_lsb_;
    const double primvertdz_lsb_;
    const double sum_pT_pv_lsb_;
    const int pos_chg_;
    const int neg_chg_;
    const uint32_t lut_scale_;
  };
}  // namespace l1t

#endif  // L1GTScales.h
