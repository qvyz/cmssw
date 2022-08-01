#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"

#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/Ref.h"

#include "FWCore/Framework/interface/MakerMacros.h"

#include "L1GTScales.h"

#include <cinttypes>
#include <memory>
#include <vector>
#include <functional>
#include <optional>
#include <set>

#include <ap_int.h>

using namespace l1t;

class L1GTTripleObjectCond : public edm::stream::EDFilter<> {
public:
  explicit L1GTTripleObjectCond(const edm::ParameterSet&);
  ~L1GTTripleObjectCond() override = default;

  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  bool filter(edm::Event&, edm::EventSetup const&) override;
  bool checkObjects(const P2GTCandidate&, const P2GTCandidate&, const P2GTCandidate&) const;

  const edm::InputTag col1Tag_;
  const edm::InputTag col2Tag_;
  const edm::InputTag col3Tag_;

  const L1GTScales scales_;

  const std::optional<ap_uint<16>> pt1_cut_;
  const std::optional<ap_uint<16>> pt2_cut_;
  const std::optional<ap_uint<16>> pt3_cut_;
  const std::optional<ap_int<14>> minEta1_cut_;
  const std::optional<ap_int<14>> maxEta1_cut_;
  const std::optional<ap_int<14>> minEta2_cut_;
  const std::optional<ap_int<14>> maxEta2_cut_;
  const std::optional<ap_int<14>> minEta3_cut_;
  const std::optional<ap_int<14>> maxEta3_cut_;
  const std::optional<ap_int<13>> minPhi1_cut_;
  const std::optional<ap_int<13>> maxPhi1_cut_;
  const std::optional<ap_int<13>> minPhi2_cut_;
  const std::optional<ap_int<13>> maxPhi2_cut_;
  const std::optional<ap_int<13>> minPhi3_cut_;
  const std::optional<ap_int<13>> maxPhi3_cut_;
  const std::optional<ap_int<10>> minDz1_cut_;
  const std::optional<ap_int<10>> maxDz1_cut_;
  const std::optional<ap_int<10>> minDz2_cut_;
  const std::optional<ap_int<10>> maxDz2_cut_;
  const std::optional<ap_int<10>> minDz3_cut_;
  const std::optional<ap_int<10>> maxDz3_cut_;
  const std::optional<ap_uint<8>> qual1_cut_;
  const std::optional<ap_uint<8>> qual2_cut_;
  const std::optional<ap_uint<8>> qual3_cut_;
  const std::optional<ap_uint<2>> iso1_cut_;
  const std::optional<ap_uint<2>> iso2_cut_;
  const std::optional<ap_uint<2>> iso3_cut_;

  const bool os_cut_;
  const bool ss_cut_;
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

L1GTTripleObjectCond::L1GTTripleObjectCond(const edm::ParameterSet& config)
    : col1Tag_(config.getParameter<edm::InputTag>("col1Tag")),
      col2Tag_(config.getParameter<edm::InputTag>("col2Tag")),
      col3Tag_(config.getParameter<edm::InputTag>("col3Tag")),
      scales_(config.getParameter<edm::ParameterSet>("scales")),
      pt1_cut_(getOptionalParam<int, double>(
          "pt1_cut", config, std::bind(&L1GTScales::to_hw_pT, scales_, std::placeholders::_1))),
      pt2_cut_(getOptionalParam<int, double>(
          "pt2_cut", config, std::bind(&L1GTScales::to_hw_pT, scales_, std::placeholders::_1))),
      pt3_cut_(getOptionalParam<int, double>(
          "pt3_cut", config, std::bind(&L1GTScales::to_hw_pT, scales_, std::placeholders::_1))),
      minEta1_cut_(getOptionalParam<int, double>(
          "minEta1_cut", config, std::bind(&L1GTScales::to_hw_eta, scales_, std::placeholders::_1))),
      maxEta1_cut_(getOptionalParam<int, double>(
          "maxEta1_cut", config, std::bind(&L1GTScales::to_hw_eta, scales_, std::placeholders::_1))),
      minEta2_cut_(getOptionalParam<int, double>(
          "minEta2_cut", config, std::bind(&L1GTScales::to_hw_eta, scales_, std::placeholders::_1))),
      maxEta2_cut_(getOptionalParam<int, double>(
          "maxEta2_cut", config, std::bind(&L1GTScales::to_hw_eta, scales_, std::placeholders::_1))),
      minEta3_cut_(getOptionalParam<int, double>(
          "minEta3_cut", config, std::bind(&L1GTScales::to_hw_eta, scales_, std::placeholders::_1))),
      maxEta3_cut_(getOptionalParam<int, double>(
          "maxEta3_cut", config, std::bind(&L1GTScales::to_hw_eta, scales_, std::placeholders::_1))),
      minPhi1_cut_(getOptionalParam<int, double>(
          "minPhi1_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      maxPhi1_cut_(getOptionalParam<int, double>(
          "maxPhi1_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      minPhi2_cut_(getOptionalParam<int, double>(
          "minPhi2_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      maxPhi2_cut_(getOptionalParam<int, double>(
          "maxPhi2_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      minPhi3_cut_(getOptionalParam<int, double>(
          "minPhi3_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      maxPhi3_cut_(getOptionalParam<int, double>(
          "maxPhi3_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      minDz1_cut_(getOptionalParam<int, double>(
          "minDz1_cut", config, std::bind(&L1GTScales::to_hw_dZ, scales_, std::placeholders::_1))),
      maxDz1_cut_(getOptionalParam<int, double>(
          "maxDz1_cut", config, std::bind(&L1GTScales::to_hw_dZ, scales_, std::placeholders::_1))),
      minDz2_cut_(getOptionalParam<int, double>(
          "minDz2_cut", config, std::bind(&L1GTScales::to_hw_dZ, scales_, std::placeholders::_1))),
      maxDz2_cut_(getOptionalParam<int, double>(
          "maxDz2_cut", config, std::bind(&L1GTScales::to_hw_dZ, scales_, std::placeholders::_1))),
      minDz3_cut_(getOptionalParam<int, double>(
          "minDz3_cut", config, std::bind(&L1GTScales::to_hw_dZ, scales_, std::placeholders::_1))),
      maxDz3_cut_(getOptionalParam<int, double>(
          "maxDz3_cut", config, std::bind(&L1GTScales::to_hw_dZ, scales_, std::placeholders::_1))),
      qual1_cut_(getOptionalParam<unsigned int>("qual1_cut", config)),
      qual2_cut_(getOptionalParam<unsigned int>("qual2_cut", config)),
      qual3_cut_(getOptionalParam<unsigned int>("qual3_cut", config)),
      iso1_cut_(getOptionalParam<unsigned int>("iso1_cut", config)),
      iso2_cut_(getOptionalParam<unsigned int>("iso2_cut", config)),
      iso3_cut_(getOptionalParam<unsigned int>("iso3_cut", config)),
      os_cut_(config.exists("os_cut") ? config.getParameter<bool>("os_cut") : false),
      ss_cut_(config.exists("ss_cut") ? config.getParameter<bool>("ss_cut") : false) {
  consumes<P2GTCandidateCollection>(col1Tag_);
  produces<P2GTCandidateVectorRef>(col1Tag_.instance());

  if (!(col1Tag_ == col2Tag_)) {
    consumes<P2GTCandidateCollection>(col2Tag_);
    produces<P2GTCandidateVectorRef>(col2Tag_.instance());
  }

  if (!(col1Tag_ == col3Tag_) && !(col2Tag_ == col3Tag_)) {
    consumes<P2GTCandidateCollection>(col3Tag_);
    produces<P2GTCandidateVectorRef>(col3Tag_.instance());
  }
}

void L1GTTripleObjectCond::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("col1Tag");
  desc.add<edm::InputTag>("col2Tag");
  desc.add<edm::InputTag>("col3Tag");
  desc.addOptional<double>("pt1_cut");
  desc.addOptional<double>("pt2_cut");
  desc.addOptional<double>("pt3_cut");
  desc.addOptional<double>("minEta1_cut");
  desc.addOptional<double>("maxEta1_cut");
  desc.addOptional<double>("minEta2_cut");
  desc.addOptional<double>("maxEta2_cut");
  desc.addOptional<double>("minEta3_cut");
  desc.addOptional<double>("maxEta3_cut");
  desc.addOptional<double>("minPhi1_cut");
  desc.addOptional<double>("maxPhi1_cut");
  desc.addOptional<double>("minPhi2_cut");
  desc.addOptional<double>("maxPhi2_cut");
  desc.addOptional<double>("minPhi3_cut");
  desc.addOptional<double>("maxPhi3_cut");
  desc.addOptional<double>("minDz1_cut");
  desc.addOptional<double>("maxDz1_cut");
  desc.addOptional<double>("minDz2_cut");
  desc.addOptional<double>("maxDz2_cut");
  desc.addOptional<double>("minDz3_cut");
  desc.addOptional<double>("maxDz3_cut");
  desc.addOptional<unsigned int>("qual1_cut");
  desc.addOptional<unsigned int>("qual2_cut");
  desc.addOptional<unsigned int>("qual3_cut");
  desc.addOptional<unsigned int>("iso1_cut");
  desc.addOptional<unsigned int>("iso2_cut");
  desc.addOptional<unsigned int>("iso3_cut");
  desc.addOptional<bool>("os_cut", false);
  desc.addOptional<bool>("ss_cut", false);

  edm::ParameterSetDescription scalesDesc;
  L1GTScales::fillDescriptions(scalesDesc);
  desc.add<edm::ParameterSetDescription>("scales", scalesDesc);

  descriptions.addWithDefaultLabel(desc);
}

bool L1GTTripleObjectCond::filter(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<P2GTCandidateCollection> col1;
  edm::Handle<P2GTCandidateCollection> col2;
  edm::Handle<P2GTCandidateCollection> col3;
  event.getByLabel(col1Tag_, col1);
  event.getByLabel(col2Tag_, col2);
  event.getByLabel(col3Tag_, col3);

  bool condition_result = false;

  std::set<std::size_t> triggeredIdcs1;
  std::set<std::size_t> triggeredIdcs2;
  std::set<std::size_t> triggeredIdcs3;

  for (std::size_t idx1 = 0; idx1 < col1->size(); ++idx1) {
    for (std::size_t idx2 = 0; idx2 < col2->size(); ++idx2) {
      for (std::size_t idx3 = 0; idx3 < col3->size(); ++idx3) {
        // If we're looking at the same collection then we shouldn't use the same object in one comparison.
        if (col1.product() == col2.product() && idx1 == idx2) {
          continue;
        }

        if (col1.product() == col3.product() && idx1 == idx3) {
          continue;
        }

        if (col2.product() == col3.product() && idx2 == idx3) {
          continue;
        }

        bool pass{checkObjects(col1->at(idx1), col2->at(idx2), col3->at(idx3))};
        condition_result |= pass;

        if (pass) {
          triggeredIdcs1.emplace(idx1);

          if (col1.product() != col2.product()) {
            triggeredIdcs2.emplace(idx2);
          } else {
            triggeredIdcs1.emplace(idx2);
          }

          if (col1.product() != col3.product() && col2.product() != col3.product()) {
            triggeredIdcs3.emplace(idx3);
          } else if (col1.product() == col3.product()) {
            triggeredIdcs1.emplace(idx3);
          } else {
            triggeredIdcs2.emplace(idx3);
          }
        }
      }
    }
  }

  if (condition_result) {
    std::unique_ptr<P2GTCandidateVectorRef> triggerCol1 = std::make_unique<P2GTCandidateVectorRef>();

    for (std::size_t idx : triggeredIdcs1) {
      triggerCol1->push_back(P2GTCandidateRef(col1, idx));
    }
    event.put(std::move(triggerCol1), col1Tag_.instance());

    if (col1.product() != col2.product()) {
      std::unique_ptr<P2GTCandidateVectorRef> triggerCol2 = std::make_unique<P2GTCandidateVectorRef>();

      for (std::size_t idx : triggeredIdcs2) {
        triggerCol2->push_back(P2GTCandidateRef(col2, idx));
      }
      event.put(std::move(triggerCol2), col2Tag_.instance());
    }

    if (col1.product() != col3.product() && col2.product() != col3.product()) {
      std::unique_ptr<P2GTCandidateVectorRef> triggerCol3 = std::make_unique<P2GTCandidateVectorRef>();

      for (std::size_t idx : triggeredIdcs3) {
        triggerCol3->push_back(P2GTCandidateRef(col3, idx));
      }
      event.put(std::move(triggerCol3), col3Tag_.instance());
    }
  }

  return condition_result;
}

bool L1GTTripleObjectCond::checkObjects(const P2GTCandidate& obj1,
                                        const P2GTCandidate& obj2,
                                        const P2GTCandidate& obj3) const {
  bool res{true};
  res &= pt1_cut_ ? (obj1.hwPT() > pt1_cut_) : true;
  res &= pt2_cut_ ? (obj2.hwPT() > pt2_cut_) : true;
  res &= pt3_cut_ ? (obj3.hwPT() > pt3_cut_) : true;
  res &= minEta1_cut_ ? (obj1.hwEta() > minEta1_cut_) : true;
  res &= maxEta1_cut_ ? (obj1.hwEta() < maxEta1_cut_) : true;
  res &= minEta2_cut_ ? (obj2.hwEta() > minEta2_cut_) : true;
  res &= maxEta2_cut_ ? (obj2.hwEta() < maxEta2_cut_) : true;
  res &= minEta3_cut_ ? (obj3.hwEta() > minEta3_cut_) : true;
  res &= maxEta3_cut_ ? (obj3.hwEta() < maxEta3_cut_) : true;
  res &= minPhi1_cut_ ? (obj1.hwPhi() > minPhi1_cut_) : true;
  res &= maxPhi1_cut_ ? (obj1.hwPhi() < maxPhi1_cut_) : true;
  res &= minPhi2_cut_ ? (obj2.hwPhi() > minPhi2_cut_) : true;
  res &= maxPhi2_cut_ ? (obj2.hwPhi() < maxPhi2_cut_) : true;
  res &= minPhi3_cut_ ? (obj3.hwPhi() > minPhi3_cut_) : true;
  res &= maxPhi3_cut_ ? (obj3.hwPhi() < maxPhi3_cut_) : true;
  res &= minDz1_cut_ ? (obj1.hwDZ() > minDz1_cut_) : true;
  res &= maxDz1_cut_ ? (obj1.hwDZ() < maxDz1_cut_) : true;
  res &= minDz2_cut_ ? (obj2.hwDZ() > minDz2_cut_) : true;
  res &= maxDz2_cut_ ? (obj2.hwDZ() < maxDz2_cut_) : true;
  res &= minDz3_cut_ ? (obj3.hwDZ() > minDz3_cut_) : true;
  res &= maxDz3_cut_ ? (obj3.hwDZ() < maxDz3_cut_) : true;
  res &= qual1_cut_ ? (obj1.hwQual() > qual1_cut_) : true;
  res &= qual2_cut_ ? (obj2.hwQual() > qual2_cut_) : true;
  res &= qual3_cut_ ? (obj3.hwQual() > qual3_cut_) : true;
  res &= iso1_cut_ ? (obj1.hwIso() > iso1_cut_) : true;
  res &= iso2_cut_ ? (obj2.hwIso() > iso2_cut_) : true;
  res &= iso3_cut_ ? (obj3.hwIso() > iso3_cut_) : true;

  return res;
}

DEFINE_FWK_MODULE(L1GTTripleObjectCond);
