#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"

#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/Ref.h"

#include "L1GTScales.h"

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

private:
  bool filter(edm::Event&, edm::EventSetup const&) override;
  bool checkObject(const P2GTCandidate&) const;

  const edm::InputTag colTag_;

  L1GTScales scales_;

  std::optional<ap_uint<16>> pt_cut_;
  std::optional<ap_int<14>> minEta_cut_;
  std::optional<ap_int<14>> maxEta_cut_;
  std::optional<ap_int<13>> minPhi_cut_;
  std::optional<ap_int<13>> maxPhi_cut_;
  std::optional<ap_int<10>> minDz_cut_;
  std::optional<ap_int<10>> maxDz_cut_;
  std::optional<ap_uint<8>> qual_cut_;
  std::optional<ap_uint<2>> iso_cut_;
};

template <typename T, typename K>
static inline std::optional<T> getOptionalParam(const std::string& name,
                                                const edm::ParameterSet& config,
                                                std::function<T(K)> conv) {
  if (config.exists(name)) {
    return std::optional<T>(conv(config.getParameter<K>(name)));
  }
  return std::optional<T>();
}

template <typename T>
static inline std::optional<T> getOptionalParam(const std::string& name, const edm::ParameterSet& config) {
  if (config.exists(name)) {
    return std::optional<T>(config.getParameter<T>(name));
  }
  return std::optional<T>();
}

L1GTSingleObjectCond::L1GTSingleObjectCond(const edm::ParameterSet& config)
    : colTag_(config.getParameter<edm::InputTag>("colTag")),
      scales_(config.getParameter<edm::ParameterSet>("scales")),
      pt_cut_(getOptionalParam<int, double>(
          "pt_cut", config, std::bind(&L1GTScales::to_hw_pT, scales_, std::placeholders::_1))),
      minEta_cut_(getOptionalParam<int, double>(
          "minEta_cut", config, std::bind(&L1GTScales::to_hw_eta, scales_, std::placeholders::_1))),
      maxEta_cut_(getOptionalParam<int, double>(
          "maxEta_cut", config, std::bind(&L1GTScales::to_hw_eta, scales_, std::placeholders::_1))),
      minPhi_cut_(getOptionalParam<int, double>(
          "minPhi_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      maxPhi_cut_(getOptionalParam<int, double>(
          "maxPhi_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      minDz_cut_(getOptionalParam<int, double>(
          "minDz_cut", config, std::bind(&L1GTScales::to_hw_dZ, scales_, std::placeholders::_1))),
      maxDz_cut_(getOptionalParam<int, double>(
          "maxDz_cut", config, std::bind(&L1GTScales::to_hw_dZ, scales_, std::placeholders::_1))),
      qual_cut_(getOptionalParam<unsigned int>("qual_cut", config)),
      iso_cut_(getOptionalParam<unsigned int>("iso_cut", config)) {
  consumes<P2GTCandidateCollection>(colTag_);

  produces<P2GTCandidateVectorRef>(colTag_.instance());
}

void L1GTSingleObjectCond::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("colTag");
  desc.addOptional<double>("pt_cut");
  desc.addOptional<double>("minEta_cut");
  desc.addOptional<double>("maxEta_cut");
  desc.addOptional<double>("minPhi_cut");
  desc.addOptional<double>("maxPhi_cut");
  desc.addOptional<double>("minDz_cut");
  desc.addOptional<double>("maxDz_cut");
  desc.addOptional<unsigned int>("qual_cut");
  desc.addOptional<unsigned int>("iso_cut");

  edm::ParameterSetDescription scalesDesc;
  L1GTScales::fillDescriptions(scalesDesc);
  desc.add<edm::ParameterSetDescription>("scales", scalesDesc);

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
  res &= minEta_cut_ ? (obj.hwEta() > minEta_cut_) : true;
  res &= maxEta_cut_ ? (obj.hwEta() < maxEta_cut_) : true;
  res &= minPhi_cut_ ? (obj.hwPhi() > minPhi_cut_) : true;
  res &= maxPhi_cut_ ? (obj.hwPhi() < maxPhi_cut_) : true;
  res &= minDz_cut_ ? (obj.hwDZ() > minDz_cut_) : true;
  res &= maxDz_cut_ ? (obj.hwDZ() < maxDz_cut_) : true;
  res &= qual_cut_ ? (obj.hwQual() > qual_cut_) : true;
  res &= iso_cut_ ? (obj.hwIso() > iso_cut_) : true;

  return res;
}

DEFINE_FWK_MODULE(L1GTSingleObjectCond);
