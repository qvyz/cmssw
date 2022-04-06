#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"

#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/Ref.h"

#include <cmath>
#include <cinttypes>
#include <memory>
#include <vector>
#include <optional>

#include <ap_int.h>

using namespace l1t;

class L1GTSingleObjectCond : public edm::stream::EDFilter<> {
public:
  explicit L1GTSingleObjectCond(const edm::ParameterSet&);
  ~L1GTSingleObjectCond() override = default;

  static void fillDescriptions(edm::ConfigurationDescriptions&);

  friend std::ostream& operator<<(std::ostream&, const L1GTSingleObjectCond&);

private:
  bool filter(edm::Event&, edm::EventSetup const&) override;
  bool checkObject(const P2GTCandidate&) const;

  const edm::InputTag colTag_;

  std::optional<ap_uint<16>> pt_cut_;
  std::optional<ap_int<14>> etaMin_cut_;
  std::optional<ap_int<14>> etaMax_cut_;
  std::optional<ap_int<13>> phiMin_cut_;
  std::optional<ap_int<13>> phiMax_cut_;
  std::optional<ap_int<10>> dZMin_cut_;
  std::optional<ap_int<10>> dZMax_cut_;
  std::optional<ap_uint<8>> qual_cut_;
  std::optional<ap_uint<2>> iso_cut_;
};

template <typename T>
static inline std::optional<T> getOptionalParam(const char* name, const edm::ParameterSet& config) {
  if (config.exists(name)) {
    return std::optional<T>(config.getParameter<T>(name));
  }
  return std::optional<T>();
}

L1GTSingleObjectCond::L1GTSingleObjectCond(const edm::ParameterSet& config)
    : colTag_(config.getParameter<edm::InputTag>("colTag")),
      pt_cut_(getOptionalParam<int>("pt_cut", config)),
      etaMin_cut_(getOptionalParam<int>("etaMin_cut", config)),
      etaMax_cut_(getOptionalParam<int>("etaMax_cut", config)),
      phiMin_cut_(getOptionalParam<int>("phiMin_cut", config)),
      phiMax_cut_(getOptionalParam<int>("phiMax_cut", config)),
      dZMin_cut_(getOptionalParam<int>("dZMin_cut", config)),
      dZMax_cut_(getOptionalParam<int>("dZMax_cut", config)),
      qual_cut_(getOptionalParam<int>("qual_cut", config)),
      iso_cut_(getOptionalParam<int>("iso_cut", config)) {
  consumes<P2GTCandidateCollection>(colTag_);

  produces<P2GTCandidateVectorRef>(colTag_.instance());
}

void L1GTSingleObjectCond::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("colTag");
  desc.addOptional<int>("pt_cut");
  desc.addOptional<int>("etaMin_cut");
  desc.addOptional<int>("etaMax_cut");
  desc.addOptional<int>("phiMin_cut");
  desc.addOptional<int>("phiMax_cut");
  desc.addOptional<int>("dZMin_cut");
  desc.addOptional<int>("dZMax_cut");
  desc.addOptional<int>("qual_cut");
  desc.addOptional<int>("iso_cut");

  descriptions.addWithDefaultLabel(desc);
}

bool L1GTSingleObjectCond::filter(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<P2GTCandidateCollection> col;
  event.getByLabel(colTag_, col);

  bool condition_result = false;

  std::unique_ptr<P2GTCandidateVectorRef> triggerCol = std::make_unique<P2GTCandidateVectorRef>();

  for (std::size_t idx = 0; idx < col->size(); ++idx) {
    bool pass{checkObject(col->at(idx))};
    condition_result |= pass;

    if (pass) {
      triggerCol->push_back(P2GTCandidateRef(col, idx));
    }
  }

  if (condition_result) {
    event.put(std::move(triggerCol), colTag_.instance());
  }

  return condition_result;
}

bool L1GTSingleObjectCond::checkObject(const P2GTCandidate& obj) const {
  bool res{true};
  res &= pt_cut_ ? (obj.hwPT() > pt_cut_) : true;
  res &= etaMin_cut_ ? (obj.hwEta() > etaMin_cut_) : true;
  res &= etaMax_cut_ ? (obj.hwEta() < etaMax_cut_) : true;
  res &= phiMin_cut_ ? (obj.hwPhi() > phiMin_cut_) : true;
  res &= phiMax_cut_ ? (obj.hwPhi() < phiMax_cut_) : true;
  res &= dZMin_cut_ ? (obj.hwDZ() > dZMin_cut_) : true;
  res &= dZMax_cut_ ? (obj.hwDZ() < dZMax_cut_) : true;
  res &= qual_cut_ ? (obj.hwQual() > qual_cut_) : true;
  res &= iso_cut_ ? (obj.hwIso() > iso_cut_) : true;

  return res;
}

DEFINE_FWK_MODULE(L1GTSingleObjectCond);
