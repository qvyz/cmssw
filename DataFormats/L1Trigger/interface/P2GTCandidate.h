#ifndef P2GTCandidate_h
#define P2GTCandidate_h

#include <vector>
#include <ap_int.h>

#include "DataFormats/L1Trigger/interface/BXVector.h"

#include "DataFormats/L1TCorrelator/interface/TkElectron.h"
#include "DataFormats/L1TCorrelator/interface/TkEm.h"

namespace l1t {

  class P2GTCandidate;
  typedef std::vector<P2GTCandidate> P2GTCandidateCollection;
  typedef edm::Ref<P2GTCandidateCollection> P2GTCandidateRef;
  typedef edm::RefVector<P2GTCandidateCollection> P2GTCandidateRefVector;
  typedef std::vector<P2GTCandidateRef> P2GTCandidateVectorRef;

  class P2GTCandidate {
  public:
    typedef ap_uint<16> hwPT_t;
    typedef ap_int<13> hwPhi_t;
    typedef ap_int<14> hwEta_t;
    typedef ap_uint<10> hwDZ_t;
    typedef ap_uint<11> hwIso_t;
    typedef ap_uint<8> hwQual_t;
    typedef ap_uint<1> hwCharge_t;
    typedef ap_int<12> hwDD_t;
    typedef ap_uint<4> hwBeta_t;
    typedef ap_uint<10> hwMass_t;
    typedef ap_uint<16> hwIndex_t;
    typedef ap_uint<10> hwSeed_pT_t;
    typedef ap_int<10> hwSeed_dZ_t;
    typedef ap_uint<16> hwSca_sum_t;
    typedef ap_int<16> hwPrimvertdz_t;
    typedef ap_uint<5> hwNumber_of_tracks_t;
    typedef ap_uint<12> hwSum_pT_pv_t;
    typedef ap_uint<2> hwType_t;
    typedef ap_uint<8> hwNumber_of_tracks_in_pv_t;
    typedef ap_uint<10> hwNumber_of_tracks_not_in_pv_t;

    P2GTCandidate();
    P2GTCandidate(const TkElectron&);
    P2GTCandidate(const TkEm&);

    void setHwPT(hwPT_t hwPT) { hwPT_ = hwPT; }
    void setHwPhi(hwPhi_t hwPhi) { hwPhi_ = hwPhi; }
    void setHwEta(hwEta_t hwEta) { hwEta_ = hwEta; }
    void setHwDZ(hwDZ_t hwDZ) { hwDZ_ = hwDZ; }
    void setHwIso(hwIso_t hwIso) { hwIso_ = hwIso; }
    void setHwQual(hwQual_t hwQual) { hwQual_ = hwQual; }
    void setHwCharge(hwCharge_t hwCharge) { hwCharge_ = hwCharge; }
    void setHwDD(hwDD_t hwDD) { hwDD_ = hwDD; }
    void setHwBeta(hwBeta_t hwBeta) { hwBeta_ = hwBeta; }
    void setHwMass(hwMass_t hwMass) { hwMass_ = hwMass; }
    void setHwIndex(hwIndex_t hwIndex) { hwIndex_ = hwIndex; }
    void setHwSeed_pT(hwSeed_pT_t hwSeed_pT) { hwSeed_pT_ = hwSeed_pT; }
    void setHwSeed_dZ(hwSeed_dZ_t hwSeed_dZ) { hwSeed_dZ_ = hwSeed_dZ; }
    void setHwSca_sum(hwSca_sum_t hwSca_sum) { hwSca_sum_ = hwSca_sum; }
    void setHwPrimvertdz(hwPrimvertdz_t hwPrimvertdz) { hwPrimvertdz_ = hwPrimvertdz; }
    void setHwNumber_of_tracks(hwNumber_of_tracks_t hwNumber_of_tracks) { hwNumber_of_tracks_ = hwNumber_of_tracks; }

    void setHwSum_pT_pv(hwSum_pT_pv_t hwSum_pT_pv) { hwSum_pT_pv_ = hwSum_pT_pv; }
    void setHwType(hwType_t hwType) { hwType_ = hwType; }
    void setHwNumber_of_tracks_in_pv(hwNumber_of_tracks_in_pv_t hwNumber_of_tracks_in_pv) {
      hwNumber_of_tracks_in_pv_ = hwNumber_of_tracks_in_pv;
    }
    void setHwNumber_of_tracks_not_in_pv(hwNumber_of_tracks_not_in_pv_t hwNumber_of_tracks_not_in_pv) {
      hwNumber_of_tracks_not_in_pv_ = hwNumber_of_tracks_not_in_pv;
    }

    hwPT_t hwPT() const { return hwPT_; }
    hwPhi_t hwPhi() const { return hwPhi_; }
    hwEta_t hwEta() const { return hwEta_; }
    hwDZ_t hwDZ() const { return hwDZ_; }
    hwIso_t hwIso() const { return hwIso_; }
    hwQual_t hwQual() const { return hwQual_; }
    hwCharge_t hwCharge() const { return hwCharge_; }
    hwDD_t hwDD() const { return hwDD_; }
    hwBeta_t hwBeta() const { return hwBeta_; }
    hwMass_t hwMass() const { return hwMass_; }
    hwIndex_t hwIndex() const { return hwIndex_; }
    hwSeed_pT_t hwSeed_pT() const { return hwSeed_pT_; }
    hwSeed_dZ_t hwSeed_dZ() const { return hwSeed_dZ_; }
    hwSca_sum_t hwSca_sum() const { return hwSca_sum_; }
    hwPrimvertdz_t hwPrimvertdz() const { return hwPrimvertdz_; }
    hwNumber_of_tracks_t hwNumber_of_tracks() const { return hwNumber_of_tracks_; }
    hwSum_pT_pv_t hwSum_pT_pv() const { return hwSum_pT_pv_; }
    hwType_t hwType() const { return hwType_; }
    hwNumber_of_tracks_in_pv_t hwNumber_of_tracks_in_pv() const { return hwNumber_of_tracks_in_pv_; }
    hwNumber_of_tracks_not_in_pv_t hwNumber_of_tracks_not_in_pv() const { return hwNumber_of_tracks_not_in_pv_; }

    bool operator==(const l1t::P2GTCandidate& rhs) const;
    bool operator!=(const l1t::P2GTCandidate& rhs) const;

  private:
    int hwPT_ = 0;
    int hwPhi_ = 0;
    int hwEta_ = 0;
    int hwDZ_ = 0;
    int hwIso_ = 0;
    int hwQual_ = 0;
    int hwCharge_ = 0;
    int hwDD_ = 0;
    int hwBeta_ = 0;
    int hwMass_ = 0;
    int hwIndex_ = 0;
    int hwSeed_pT_ = 0;
    int hwSeed_dZ_ = 0;
    int hwSca_sum_ = 0;
    int hwPrimvertdz_ = 0;
    int hwNumber_of_tracks_ = 0;

    // TODO ?
    int hwSum_pT_pv_ = 0;
    int hwType_ = 0;
    int hwNumber_of_tracks_in_pv_ = 0;
    int hwNumber_of_tracks_not_in_pv_ = 0;
  };

};  // namespace l1t

#endif
