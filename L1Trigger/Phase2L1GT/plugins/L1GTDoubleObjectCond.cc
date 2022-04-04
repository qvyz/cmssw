#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"

#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/Ref.h"

#include "FWCore/Framework/interface/MakerMacros.h"

#include <cmath>
#include <cinttypes>
#include <memory>
#include <vector>
#include <optional>

#include <ap_int.h>

using namespace l1t;

class L1GTDoubleObjectCond : public edm::stream::EDFilter<> {
public:
  explicit L1GTDoubleObjectCond(const edm::ParameterSet&);
  ~L1GTDoubleObjectCond() override = default;

  static void fillDescriptions(edm::ConfigurationDescriptions&);

  friend std::ostream& operator<<(std::ostream&, const L1GTDoubleObjectCond&);

private:
  bool filter(edm::Event&, edm::EventSetup const&) override;
  bool checkObjects(const P2GTCandidate&, const P2GTCandidate&) const;

  const edm::InputTag col1Tag_;
  const edm::InputTag col2Tag_;

  std::optional<ap_uint<16>> pt1_cut_;
  std::optional<ap_uint<16>> pt2_cut_;
  std::optional<ap_int<14>> eta1Min_cut_;
  std::optional<ap_int<14>> eta1Max_cut_;
  std::optional<ap_int<14>> eta2Min_cut_;
  std::optional<ap_int<14>> eta2Max_cut_;
  std::optional<ap_int<13>> phi1Min_cut_;
  std::optional<ap_int<13>> phi1Max_cut_;
  std::optional<ap_int<13>> phi2Min_cut_;
  std::optional<ap_int<13>> phi2Max_cut_;
  std::optional<ap_int<10>> dZ1Min_cut_;
  std::optional<ap_int<10>> dZ1Max_cut_;
  std::optional<ap_int<10>> dZ2Min_cut_;
  std::optional<ap_int<10>> dZ2Max_cut_;
  std::optional<ap_uint<8>> qual1_cut_;
  std::optional<ap_uint<8>> qual2_cut_;
  std::optional<ap_uint<2>> iso1_cut_;
  std::optional<ap_uint<2>> iso2_cut_;
  std::optional<ap_uint<14>> dEtaMin_cut_;
  std::optional<ap_uint<14>> dEtaMax_cut_;
  std::optional<ap_uint<13>> dPhiMin_cut_;
  std::optional<ap_uint<13>> dPhiMax_cut_;

  std::optional<ap_uint<28>> dRSquaredMin_cut_;
  std::optional<ap_uint<28>> dRSquaredMax_cut_;
  std::optional<ap_uint<28>> invMassDiv2Min_cut_;
  std::optional<ap_uint<28>> invMassDiv2Max_cut_;

  bool os_cut_;
  bool ss_cut_;
};

template <typename T>
static inline std::optional<T> getOptionalParam(const char* name, const edm::ParameterSet& config) {
  if (config.exists(name)) {
    return std::optional<T>(config.getParameter<T>(name));
  }
  return std::optional<T>();
}

L1GTDoubleObjectCond::L1GTDoubleObjectCond(const edm::ParameterSet& config)
    : col1Tag_(config.getParameter<edm::InputTag>("col1Tag")),
      col2Tag_(config.getParameter<edm::InputTag>("col2Tag")),
      pt1_cut_(getOptionalParam<int>("pt1_cut", config)),
      pt2_cut_(getOptionalParam<int>("pt2_cut", config)),
      eta1Min_cut_(getOptionalParam<int>("eta1Min_cut", config)),
      eta1Max_cut_(getOptionalParam<int>("eta1Max_cut", config)),
      eta2Min_cut_(getOptionalParam<int>("eta2Min_cut", config)),
      eta2Max_cut_(getOptionalParam<int>("eta2Max_cut", config)),
      phi1Min_cut_(getOptionalParam<int>("phi1Min_cut", config)),
      phi1Max_cut_(getOptionalParam<int>("phi1Max_cut", config)),
      phi2Min_cut_(getOptionalParam<int>("phi2Min_cut", config)),
      phi2Max_cut_(getOptionalParam<int>("phi2Max_cut", config)),
      dZ1Min_cut_(getOptionalParam<int>("dZ1Min_cut", config)),
      dZ1Max_cut_(getOptionalParam<int>("dZ1Max_cut", config)),
      dZ2Min_cut_(getOptionalParam<int>("dZ2Min_cut", config)),
      dZ2Max_cut_(getOptionalParam<int>("dZ2Max_cut", config)),
      qual1_cut_(getOptionalParam<int>("qual1_cut", config)),
      qual2_cut_(getOptionalParam<int>("qual2_cut", config)),
      iso1_cut_(getOptionalParam<int>("iso1_cut", config)),
      iso2_cut_(getOptionalParam<int>("iso2_cut", config)),
      dEtaMin_cut_(getOptionalParam<int>("dEtaMin_cut", config)),
      dEtaMax_cut_(getOptionalParam<int>("dEtaMax_cut", config)),
      dPhiMin_cut_(getOptionalParam<int>("dPhiMin_cut", config)),
      dPhiMax_cut_(getOptionalParam<int>("dPhiMax_cut", config)),
      dRSquaredMin_cut_(getOptionalParam<int>("dRSquaredMin_cut", config)),
      dRSquaredMax_cut_(getOptionalParam<int>("dRSquaredMax_cut", config)),
      invMassDiv2Min_cut_(getOptionalParam<int>("invMassDiv2Min_cut", config)),
      invMassDiv2Max_cut_(getOptionalParam<int>("invMassDiv2Max_cut", config)),
      os_cut_(config.exists("os_cut") ? config.getParameter<bool>("os_cut") : false),
      ss_cut_(config.exists("ss_cut") ? config.getParameter<bool>("ss_cut") : false) {
  consumes<P2GTCandidateCollection>(col1Tag_);
  consumes<P2GTCandidateCollection>(col2Tag_);

  produces<P2GTCandidateVectorRef>(col1Tag_.instance());
  produces<P2GTCandidateVectorRef>(col2Tag_.instance());
}

void L1GTDoubleObjectCond::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("col1Tag");
  desc.add<edm::InputTag>("col2Tag");
  desc.addOptional<int>("pt1_cut");
  desc.addOptional<int>("pt2_cut");
  desc.addOptional<int>("eta1Min_cut");
  desc.addOptional<int>("eta1Max_cut");
  desc.addOptional<int>("eta2Min_cut");
  desc.addOptional<int>("eta2Max_cut");
  desc.addOptional<int>("phi1Min_cut");
  desc.addOptional<int>("phi1Max_cut");
  desc.addOptional<int>("phi2Min_cut");
  desc.addOptional<int>("phi2Max_cut");
  desc.addOptional<int>("dZ1Min_cut");
  desc.addOptional<int>("dZ1Max_cut");
  desc.addOptional<int>("dZ2Min_cut");
  desc.addOptional<int>("dZ2Max_cut");
  desc.addOptional<int>("qual1_cut");
  desc.addOptional<int>("qual2_cut");
  desc.addOptional<int>("iso1_cut");
  desc.addOptional<int>("iso2_cut");
  desc.addOptional<int>("dEtaMin_cut");
  desc.addOptional<int>("dEtaMax_cut");
  desc.addOptional<int>("dPhiMin_cut");
  desc.addOptional<int>("dPhiMax_cut");
  desc.addOptional<int>("dRSquaredMin_cut");
  desc.addOptional<int>("dRSquaredMax_cut");
  desc.addOptional<int>("invMassDiv2Min_cut");
  desc.addOptional<int>("invMassDiv2Max_cut");
  desc.addOptional<bool>("os_cut", false);
  desc.addOptional<bool>("ss_cut", false);

  descriptions.addWithDefaultLabel(desc);
}

bool L1GTDoubleObjectCond::filter(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<P2GTCandidateCollection> col1;
  edm::Handle<P2GTCandidateCollection> col2;
  event.getByLabel(col1Tag_, col1);
  event.getByLabel(col2Tag_, col2);

  bool condition_result = false;

  std::unique_ptr<P2GTCandidateVectorRef> triggerCol1 = std::make_unique<P2GTCandidateVectorRef>();
  std::unique_ptr<P2GTCandidateVectorRef> triggerCol2 = std::make_unique<P2GTCandidateVectorRef>();

  for (std::size_t idx1 = 0; idx1 < col1->size(); ++idx1) {
    for (std::size_t idx2 = 0; idx2 < col2->size(); ++idx2) {
      // If we're looking at the same collection then we shouldn't use the same object in one comparison.
      if (col1.product() == col2.product()) {
        if (idx1 == idx2) {
          continue;
        }
      }

      bool pass{checkObjects(col1->at(idx1), col2->at(idx2))};
      condition_result |= pass;

      if (pass) {
        triggerCol1->push_back(P2GTCandidateRef(col1, idx1));
        if (col1.product() != col2.product()) {
          triggerCol2->push_back(P2GTCandidateRef(col2, idx2));
        }
      }
    }
  }

  if (condition_result) {
    event.put(std::move(triggerCol1), col1Tag_.instance());
    if (col1.product() != col2.product()) {
      event.put(std::move(triggerCol2), col2Tag_.instance());
    }
  }

  return condition_result;
}

bool L1GTDoubleObjectCond::checkObjects(const P2GTCandidate& obj1, const P2GTCandidate& obj2) const {
  bool res{true};
  res &= pt1_cut_ ? (obj1.hwPT() > pt1_cut_) : true;
  res &= pt2_cut_ ? (obj2.hwPT() > pt2_cut_) : true;
  res &= eta1Min_cut_ ? (obj1.hwEta() > eta1Min_cut_) : true;
  res &= eta1Max_cut_ ? (obj1.hwEta() < eta1Max_cut_) : true;
  res &= eta2Min_cut_ ? (obj2.hwEta() > eta2Min_cut_) : true;
  res &= eta2Max_cut_ ? (obj2.hwEta() < eta2Max_cut_) : true;
  res &= phi1Min_cut_ ? (obj1.hwPhi() > phi1Min_cut_) : true;
  res &= phi1Max_cut_ ? (obj1.hwPhi() < phi1Max_cut_) : true;
  res &= phi2Min_cut_ ? (obj2.hwPhi() > phi2Min_cut_) : true;
  res &= phi2Max_cut_ ? (obj2.hwPhi() < phi2Max_cut_) : true;
  res &= dZ1Min_cut_ ? (obj1.hwDZ() > dZ1Min_cut_) : true;
  res &= dZ1Max_cut_ ? (obj1.hwDZ() < dZ1Max_cut_) : true;
  res &= dZ2Min_cut_ ? (obj2.hwDZ() > dZ2Min_cut_) : true;
  res &= dZ2Max_cut_ ? (obj2.hwDZ() < dZ2Max_cut_) : true;
  // res &= (qual1_cut_ == 0) || (obj1.qual == qual1_cut_);
  // res &= (qual2_cut_ == 0) || (obj2.qual == qual2_cut_);
  // TODO: Missing iso cuts!
  int64_t dEta{(obj1.hwEta() > obj2.hwEta()) ? obj1.hwEta() - obj2.hwEta() : obj2.hwEta() - obj1.hwEta()};
  res &= dEtaMin_cut_ ? dEta > dEtaMin_cut_ : true;
  res &= dEtaMax_cut_ ? dEta < dEtaMax_cut_ : true;
  int64_t dPhi{(obj1.hwPhi() > obj2.hwPhi()) ? obj1.hwPhi() - obj2.hwPhi() : obj2.hwPhi() - obj1.hwPhi()};
  res &= dPhiMin_cut_ ? dPhi > dPhiMin_cut_ : true;
  res &= dPhiMax_cut_ ? dPhi < dPhiMax_cut_ : true;
  int64_t dRSquared{static_cast<int64_t>(std::pow(dEta, 2)) + static_cast<int64_t>(std::pow(dPhi, 2))};
  res &= dRSquaredMin_cut_ ? dRSquared > dRSquaredMin_cut_ : true;
  res &= dRSquaredMax_cut_ ? dRSquared < dRSquaredMax_cut_ : true;
  res &= os_cut_ ? obj1.hwCharge() != obj2.hwCharge() : true;
  res &= ss_cut_ ? obj1.hwCharge() == obj2.hwCharge() : true;
  int64_t invMassDiv2{obj1.hwPT().to_int64() * obj2.hwPT().to_int64()};
  //*(coshLUT_.get_result(dEta) - cosLUT_.get_result(dPhi))};
  // if (invMassDiv2Max_cut_ != 999999999) {
  //   std::cout << "mass: " << invMassDiv2 << " coshLUT: " << coshLUT_.get_result(dEta) << " cosLUT: " << cosLUT_.get_result(dPhi)
  //             << "ptPRod: " << static_cast<int64_t>(obj1.pt) * static_cast<int64_t>(obj2.pt) << "\n";
  //   std::cout << "cut: " << invMassDiv2Max_cut_ << " result: " << (invMassDiv2Max_cut_ == 999999999 ? true : invMassDiv2 < invMassDiv2Max_cut_) << "\n";
  // }
  res &= invMassDiv2Min_cut_ ? invMassDiv2 > invMassDiv2Min_cut_ : true;
  res &= invMassDiv2Max_cut_ ? invMassDiv2 < invMassDiv2Max_cut_ : true;

  return res;
}

DEFINE_FWK_MODULE(L1GTDoubleObjectCond);
