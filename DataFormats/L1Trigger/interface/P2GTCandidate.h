#ifndef P2GTCandidate_h
#define P2GTCandidate_h

#include <vector>
#include <ap_int.h>

#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/L1Trigger/interface/BXVector.h"

#include "DataFormats/L1TCorrelator/interface/TkElectron.h"
#include "DataFormats/L1TCorrelator/interface/TkEm.h"

namespace l1t {

  class P2GTCandidate;
  typedef std::vector<P2GTCandidate> P2GTCandidateCollection;
  typedef edm::Ref<P2GTCandidateCollection> P2GTCandidateRef;
  typedef edm::RefVector<P2GTCandidateCollection> P2GTCandidateRefVector;
  typedef std::vector<P2GTCandidateRef> P2GTCandidateVectorRef;

  class P2GTCandidate : public reco::LeafCandidate {
  public:
    P2GTCandidate();
    P2GTCandidate(const TkElectron&);
    P2GTCandidate(const TkEm&);

    ~P2GTCandidate() override;

    void setHwPT(ap_uint<16> hwPT) { hwPT_ = hwPT; }
    void setHwPhi(ap_int<13> hwPhi) { hwPhi_ = hwPhi; }
    void setHwEta(ap_int<14> hwEta) { hwEta_ = hwEta; }
    void setHwDZ(ap_uint<10> hwDZ) { hwDZ_ = hwDZ; }
    void setHwIso(ap_uint<11> hwIso) { hwIso_ = hwIso; }
    void setHwQual(ap_uint<8> hwQual) { hwQual_ = hwQual; }
    void setHwCharge(ap_uint<1> hwCharge) { hwCharge_ = hwCharge; }
    void setHwDD(ap_int<12> hwDD) { hwDD_ = hwDD; }
    void setHwBeta(ap_uint<4> hwBeta) { hwBeta_ = hwBeta; }
    void setHwMass(ap_uint<10> hwMass) { hwMass_ = hwMass; }
    void setHwIndex(ap_uint<16> hwIndex) { hwIndex_ = hwIndex; }
    void setHwSeed_pT(ap_uint<10> hwSeed_pT) { hwSeed_pT_ = hwSeed_pT; }
    void setHwSeed_dZ(ap_int<10> hwSeed_dZ) { hwSeed_dZ_ = hwSeed_dZ; }
    void setHwSca_sum(ap_uint<16> hwSca_sum) { hwSca_sum_ = hwSca_sum; }
    void setHwPrimvertdz(ap_int<16> hwPrimvertdz) { hwPrimvertdz_ = hwPrimvertdz; }
    void setHwNumber_of_tracks(ap_uint<5> hwNumber_of_tracks) { hwNumber_of_tracks_ = hwNumber_of_tracks; }

    void setHwSum_pT_pv(ap_uint<12> hwSum_pT_pv) { hwSum_pT_pv_ = hwSum_pT_pv; }
    void setHwType(ap_uint<2> hwType) { hwType_ = hwType; }
    void setHwNumber_of_tracks_in_pv(ap_uint<8> hwNumber_of_tracks_in_pv) {
      hwNumber_of_tracks_in_pv_ = hwNumber_of_tracks_in_pv;
    }
    void setHwNumber_of_tracks_not_in_pv(ap_uint<10> hwNumber_of_tracks_not_in_pv) {
      hwNumber_of_tracks_not_in_pv_ = hwNumber_of_tracks_not_in_pv;
    }

    ap_uint<16> hwPT() const { return hwPT_; }
    ap_int<13> hwPhi() const { return hwPhi_; }
    ap_int<14> hwEta() const { return hwEta_; }
    ap_uint<10> hwDZ() const { return hwDZ_; }
    ap_uint<11> hwIso() const { return hwIso_; }
    ap_uint<8> hwQual() const { return hwQual_; }
    ap_uint<1> hwCharge() const { return hwCharge_; }
    ap_int<12> hwDD() const { return hwDD_; }
    ap_uint<4> hwBeta() const { return hwBeta_; }
    ap_uint<10> hwMass() const { return hwMass_; }
    ap_uint<16> hwIndex() const { return hwIndex_; }
    ap_uint<10> hwSeed_pT() const { return hwSeed_pT_; }
    ap_int<10> hwSeed_dZ() const { return hwSeed_dZ_; }
    ap_uint<16> hwSca_sum() const { return hwSca_sum_; }
    ap_int<16> hwPrimvertdz() const { return hwPrimvertdz_; }
    ap_uint<5> hwNumber_of_tracks() const { return hwNumber_of_tracks_; }
    ap_uint<12> hwSum_pT_pv() const { return hwSum_pT_pv_; }
    ap_uint<2> hwType() const { return hwType_; }
    ap_uint<8> hwNumber_of_tracks_in_pv() const { return hwNumber_of_tracks_in_pv_; }
    ap_uint<10> hwNumber_of_tracks_not_in_pv() const { return hwNumber_of_tracks_not_in_pv_; }

    virtual bool operator==(const l1t::P2GTCandidate& rhs) const;
    virtual bool operator!=(const l1t::P2GTCandidate& rhs) const;

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
