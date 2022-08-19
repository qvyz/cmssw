#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"

#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/Ref.h"

#include "L1Trigger/Phase2L1GT/interface/L1GTInvariantMassError.h"

#include "FWCore/Framework/interface/MakerMacros.h"

#include "L1Trigger/Phase2L1GT/interface/L1GTScales.h"

#include <cinttypes>
#include <memory>
#include <vector>
#include <functional>
#include <optional>
#include <set>

#include <ap_int.h>

using namespace l1t;

class L1TSingleInOutLUT {
public:
  L1TSingleInOutLUT(const std::vector<int32_t>& data, uint32_t unused_lsbs, double output_scale, double max_error)
      : data_(data),
        unused_lsbs_(unused_lsbs),
        output_scale_(output_scale),
        // I guess ceil is required due to small differences in C++ and python's cos/cosh implementation.
        hwMax_error_(std::ceil(max_error * output_scale)) {}

  int32_t operator[](int32_t i) const { return data_[(i >> unused_lsbs_) % data_.size()]; }
  double hwMax_error() const { return hwMax_error_; }
  double output_scale() const { return output_scale_; }

private:
  const std::vector<int32_t> data_;
  const uint32_t unused_lsbs_;
  const double output_scale_;
  const double hwMax_error_;  // Sanity check
};

class L1GTDoubleObjectCond : public edm::stream::EDFilter<> {
public:
  explicit L1GTDoubleObjectCond(const edm::ParameterSet&);
  ~L1GTDoubleObjectCond() override = default;

  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  bool filter(edm::Event&, edm::EventSetup const&) override;
  bool checkObjects(const P2GTCandidate&, const P2GTCandidate&, InvariantMassErrorCollection&) const;

  const edm::InputTag col1Tag_;
  const edm::InputTag col2Tag_;

  const L1GTScales scales_;

  static constexpr uint32_t DETA_LUT_SPLIT = 1 << 13;  // hw 2pi

  const L1TSingleInOutLUT coshEtaLUT_;   // [0, 2pi)
  const L1TSingleInOutLUT coshEtaLUT2_;  // [2pi, 4pi)
  const L1TSingleInOutLUT cosPhiLUT_;

  const std::optional<int> pt1_cut_;
  const std::optional<int> pt2_cut_;
  const std::optional<int> minEta1_cut_;
  const std::optional<int> maxEta1_cut_;
  const std::optional<int> minEta2_cut_;
  const std::optional<int> maxEta2_cut_;
  const std::optional<int> minPhi1_cut_;
  const std::optional<int> maxPhi1_cut_;
  const std::optional<int> minPhi2_cut_;
  const std::optional<int> maxPhi2_cut_;
  const std::optional<int> minDz1_cut_;
  const std::optional<int> maxDz1_cut_;
  const std::optional<int> minDz2_cut_;
  const std::optional<int> maxDz2_cut_;
  const std::optional<int> qual1_cut_;
  const std::optional<int> qual2_cut_;
  const std::optional<int> iso1_cut_;
  const std::optional<int> iso2_cut_;
  const std::optional<int> dEtaMin_cut_;
  const std::optional<int> dEtaMax_cut_;
  const std::optional<int> dPhiMin_cut_;
  const std::optional<int> dPhiMax_cut_;

  const std::optional<int> dRSquaredMin_cut_;
  const std::optional<int> dRSquaredMax_cut_;

  const std::optional<double> invMassDiv2Min_cut_;
  const std::optional<double> invMassDiv2Max_cut_;
  const std::optional<double> transMassDiv2Min_cut_;
  const std::optional<double> transMassDiv2Max_cut_;

  const bool os_cut_;
  const bool ss_cut_;

  const bool enable_sanity_checks_;
  const bool inv_mass_checks_;
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

L1GTDoubleObjectCond::L1GTDoubleObjectCond(const edm::ParameterSet& config)
    : col1Tag_(config.getParameter<edm::InputTag>("col1Tag")),
      col2Tag_(config.getParameter<edm::InputTag>("col2Tag")),
      scales_(config.getParameter<edm::ParameterSet>("scales")),
      coshEtaLUT_(config.getParameterSet("cosh_eta_lut").getParameter<std::vector<int>>("lut"),
                  config.getParameterSet("cosh_eta_lut").getParameter<uint32_t>("unused_lsbs"),
                  config.getParameterSet("cosh_eta_lut").getParameter<double>("output_scale_factor"),
                  config.getParameterSet("cosh_eta_lut").getParameter<double>("max_error")),
      coshEtaLUT2_(config.getParameterSet("cosh_eta_lut2").getParameter<std::vector<int>>("lut"),
                   config.getParameterSet("cosh_eta_lut2").getParameter<uint32_t>("unused_lsbs"),
                   config.getParameterSet("cosh_eta_lut2").getParameter<double>("output_scale_factor"),
                   config.getParameterSet("cosh_eta_lut2").getParameter<double>("max_error")),
      cosPhiLUT_(config.getParameterSet("cos_phi_lut").getParameter<std::vector<int>>("lut"),
                 config.getParameterSet("cos_phi_lut").getParameter<uint32_t>("unused_lsbs"),
                 config.getParameterSet("cos_phi_lut").getParameter<double>("output_scale_factor"),
                 config.getParameterSet("cos_phi_lut").getParameter<double>("max_error")),
      pt1_cut_(getOptionalParam<int, double>(
          "pt1_cut", config, std::bind(&L1GTScales::to_hw_pT, scales_, std::placeholders::_1))),
      pt2_cut_(getOptionalParam<int, double>(
          "pt2_cut", config, std::bind(&L1GTScales::to_hw_pT, scales_, std::placeholders::_1))),
      minEta1_cut_(getOptionalParam<int, double>(
          "minEta1_cut", config, std::bind(&L1GTScales::to_hw_eta, scales_, std::placeholders::_1))),
      maxEta1_cut_(getOptionalParam<int, double>(
          "maxEta1_cut", config, std::bind(&L1GTScales::to_hw_eta, scales_, std::placeholders::_1))),
      minEta2_cut_(getOptionalParam<int, double>(
          "minEta2_cut", config, std::bind(&L1GTScales::to_hw_eta, scales_, std::placeholders::_1))),
      maxEta2_cut_(getOptionalParam<int, double>(
          "maxEta2_cut", config, std::bind(&L1GTScales::to_hw_eta, scales_, std::placeholders::_1))),
      minPhi1_cut_(getOptionalParam<int, double>(
          "minPhi1_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      maxPhi1_cut_(getOptionalParam<int, double>(
          "maxPhi1_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      minPhi2_cut_(getOptionalParam<int, double>(
          "minPhi2_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      maxPhi2_cut_(getOptionalParam<int, double>(
          "maxPhi2_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      minDz1_cut_(getOptionalParam<int, double>(
          "minDz1_cut", config, std::bind(&L1GTScales::to_hw_dZ, scales_, std::placeholders::_1))),
      maxDz1_cut_(getOptionalParam<int, double>(
          "maxDz1_cut", config, std::bind(&L1GTScales::to_hw_dZ, scales_, std::placeholders::_1))),
      minDz2_cut_(getOptionalParam<int, double>(
          "minDz2_cut", config, std::bind(&L1GTScales::to_hw_dZ, scales_, std::placeholders::_1))),
      maxDz2_cut_(getOptionalParam<int, double>(
          "maxDz2_cut", config, std::bind(&L1GTScales::to_hw_dZ, scales_, std::placeholders::_1))),
      qual1_cut_(getOptionalParam<unsigned int>("qual1_cut", config)),
      qual2_cut_(getOptionalParam<unsigned int>("qual2_cut", config)),
      iso1_cut_(getOptionalParam<unsigned int>("iso1_cut", config)),
      iso2_cut_(getOptionalParam<unsigned int>("iso2_cut", config)),
      dEtaMin_cut_(getOptionalParam<int, double>(
          "dEtaMin_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      dEtaMax_cut_(getOptionalParam<int, double>(
          "dEtaMax_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      dPhiMin_cut_(getOptionalParam<int, double>(
          "dPhiMin_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      dPhiMax_cut_(getOptionalParam<int, double>(
          "dPhiMax_cut", config, std::bind(&L1GTScales::to_hw_phi, scales_, std::placeholders::_1))),
      dRSquaredMin_cut_(getOptionalParam<int, double>(
          "dRMin_cut", config, std::bind(&L1GTScales::to_hw_dRSquared, scales_, std::placeholders::_1))),
      dRSquaredMax_cut_(getOptionalParam<int, double>(
          "dRMax_cut", config, std::bind(&L1GTScales::to_hw_dRSquared, scales_, std::placeholders::_1))),
      invMassDiv2Min_cut_(getOptionalParam<int, double>(
          "invMassMin_cut", config, std::bind(&L1GTScales::to_hw_InvMassSqrDiv2, scales_, std::placeholders::_1))),
      invMassDiv2Max_cut_(getOptionalParam<int, double>(
          "invMassMax_cut", config, std::bind(&L1GTScales::to_hw_InvMassSqrDiv2, scales_, std::placeholders::_1))),
      transMassDiv2Min_cut_(getOptionalParam<int, double>(
          "transMassMin_cut", config, std::bind(&L1GTScales::to_hw_TransMassSqrDiv2, scales_, std::placeholders::_1))),
      transMassDiv2Max_cut_(getOptionalParam<int, double>(
          "transMassMax_cut", config, std::bind(&L1GTScales::to_hw_TransMassSqrDiv2, scales_, std::placeholders::_1))),
      os_cut_(config.exists("os_cut") ? config.getParameter<bool>("os_cut") : false),
      ss_cut_(config.exists("ss_cut") ? config.getParameter<bool>("ss_cut") : false),
      enable_sanity_checks_(config.getUntrackedParameter<bool>("sanity_checks")),
      inv_mass_checks_(config.getUntrackedParameter<bool>("inv_mass_checks")) {
  consumes<P2GTCandidateCollection>(col1Tag_);
  produces<P2GTCandidateVectorRef>(col1Tag_.instance());

  if (!(col1Tag_ == col2Tag_)) {
    consumes<P2GTCandidateCollection>(col2Tag_);
    produces<P2GTCandidateVectorRef>(col2Tag_.instance());
  }

  if (inv_mass_checks_) {
    produces<InvariantMassErrorCollection>();
  }
}

void L1GTDoubleObjectCond::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("col1Tag");
  desc.add<edm::InputTag>("col2Tag");
  desc.addOptional<double>("pt1_cut");
  desc.addOptional<double>("pt2_cut");
  desc.addOptional<double>("minEta1_cut");
  desc.addOptional<double>("maxEta1_cut");
  desc.addOptional<double>("minEta2_cut");
  desc.addOptional<double>("maxEta2_cut");
  desc.addOptional<double>("minPhi1_cut");
  desc.addOptional<double>("maxPhi1_cut");
  desc.addOptional<double>("minPhi2_cut");
  desc.addOptional<double>("maxPhi2_cut");
  desc.addOptional<double>("minDz1_cut");
  desc.addOptional<double>("maxDz1_cut");
  desc.addOptional<double>("minDz2_cut");
  desc.addOptional<double>("maxDz2_cut");
  desc.addOptional<unsigned int>("qual1_cut");
  desc.addOptional<unsigned int>("qual2_cut");
  desc.addOptional<unsigned int>("iso1_cut");
  desc.addOptional<unsigned int>("iso2_cut");
  desc.addOptional<double>("dEtaMin_cut");
  desc.addOptional<double>("dEtaMax_cut");
  desc.addOptional<double>("dPhiMin_cut");
  desc.addOptional<double>("dPhiMax_cut");
  desc.addOptional<double>("dRMin_cut");
  desc.addOptional<double>("dRMax_cut");
  desc.addOptional<double>("invMassMin_cut");
  desc.addOptional<double>("invMassMax_cut");
  desc.addOptional<double>("transMassMin_cut");
  desc.addOptional<double>("transMassMax_cut");
  desc.addOptional<bool>("os_cut", false);
  desc.addOptional<bool>("ss_cut", false);

  edm::ParameterSetDescription scalesDesc;
  L1GTScales::fillDescriptions(scalesDesc);
  desc.add<edm::ParameterSetDescription>("scales", scalesDesc);

  edm::ParameterSetDescription coshLUTDesc;
  coshLUTDesc.add<std::vector<int32_t>>("lut");
  coshLUTDesc.add<double>("output_scale_factor");
  coshLUTDesc.add<uint32_t>("unused_lsbs");
  coshLUTDesc.add<double>("max_error");
  desc.add<edm::ParameterSetDescription>("cosh_eta_lut", coshLUTDesc);

  edm::ParameterSetDescription coshLUT2Desc;
  coshLUT2Desc.add<std::vector<int32_t>>("lut");
  coshLUT2Desc.add<double>("output_scale_factor");
  coshLUT2Desc.add<uint32_t>("unused_lsbs");
  coshLUT2Desc.add<double>("max_error");
  desc.add<edm::ParameterSetDescription>("cosh_eta_lut2", coshLUT2Desc);

  edm::ParameterSetDescription cosLUTDesc;
  cosLUTDesc.add<std::vector<int32_t>>("lut");
  cosLUTDesc.add<double>("output_scale_factor");
  cosLUTDesc.add<uint32_t>("unused_lsbs");
  cosLUTDesc.add<double>("max_error");
  desc.add<edm::ParameterSetDescription>("cos_phi_lut", cosLUTDesc);

  desc.addUntracked<bool>("sanity_checks");
  desc.addUntracked<bool>("inv_mass_checks");

  descriptions.addWithDefaultLabel(desc);
}

bool L1GTDoubleObjectCond::filter(edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<P2GTCandidateCollection> col1;
  edm::Handle<P2GTCandidateCollection> col2;
  event.getByLabel(col1Tag_, col1);
  event.getByLabel(col2Tag_, col2);

  bool condition_result = false;

  std::set<std::size_t> triggeredIdcs1;
  std::set<std::size_t> triggeredIdcs2;

  InvariantMassErrorCollection massErrors;

  if (inv_mass_checks_) {
    massErrors.reserve(col1.product() == col2.product() ? col1->size() * (col2->size() - 1)
                                                        : col1->size() * col2->size());
  }

  for (std::size_t idx1 = 0; idx1 < col1->size(); ++idx1) {
    for (std::size_t idx2 = 0; idx2 < col2->size(); ++idx2) {
      // If we're looking at the same collection then we shouldn't use the same object in one comparison.
      if (col1.product() == col2.product()) {
        if (idx1 == idx2) {
          continue;
        }
      }

      bool pass{checkObjects(col1->at(idx1), col2->at(idx2), massErrors)};
      condition_result |= pass;

      if (pass) {
        triggeredIdcs1.emplace(idx1);
        if (col1.product() != col2.product()) {
          triggeredIdcs2.emplace(idx2);
        } else {
          triggeredIdcs1.emplace(idx2);
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

    if (inv_mass_checks_) {
      event.put(std::move(std::make_unique<InvariantMassErrorCollection>(std::move(massErrors))), "");
    }
  }

  return condition_result;
}

bool L1GTDoubleObjectCond::checkObjects(const P2GTCandidate& obj1,
                                        const P2GTCandidate& obj2,
                                        InvariantMassErrorCollection& massErrors) const {
  bool res{true};
  res &= pt1_cut_ ? (obj1.hwPT() > pt1_cut_) : true;
  res &= pt2_cut_ ? (obj2.hwPT() > pt2_cut_) : true;
  res &= minEta1_cut_ ? (obj1.hwEta() > minEta1_cut_) : true;
  res &= maxEta1_cut_ ? (obj1.hwEta() < maxEta1_cut_) : true;
  res &= minEta2_cut_ ? (obj2.hwEta() > minEta2_cut_) : true;
  res &= maxEta2_cut_ ? (obj2.hwEta() < maxEta2_cut_) : true;
  res &= minPhi1_cut_ ? (obj1.hwPhi() > minPhi1_cut_) : true;
  res &= maxPhi1_cut_ ? (obj1.hwPhi() < maxPhi1_cut_) : true;
  res &= minPhi2_cut_ ? (obj2.hwPhi() > minPhi2_cut_) : true;
  res &= maxPhi2_cut_ ? (obj2.hwPhi() < maxPhi2_cut_) : true;
  res &= minDz1_cut_ ? (obj1.hwDZ() > minDz1_cut_) : true;
  res &= maxDz1_cut_ ? (obj1.hwDZ() < maxDz1_cut_) : true;
  res &= minDz2_cut_ ? (obj2.hwDZ() > minDz2_cut_) : true;
  res &= maxDz2_cut_ ? (obj2.hwDZ() < maxDz2_cut_) : true;
  res &= qual1_cut_ ? (obj1.hwQual() > qual1_cut_) : true;
  res &= qual2_cut_ ? (obj2.hwQual() > qual2_cut_) : true;
  res &= iso1_cut_ ? (obj1.hwIso() > iso1_cut_) : true;
  res &= iso2_cut_ ? (obj2.hwIso() > iso2_cut_) : true;

  int64_t dEta = (obj1.hwEta() > obj2.hwEta()) ? obj1.hwEta().to_int64() - obj2.hwEta().to_int64()
                                               : obj2.hwEta().to_int64() - obj1.hwEta().to_int64();
  res &= dEtaMin_cut_ ? dEta > dEtaMin_cut_ : true;
  res &= dEtaMax_cut_ ? dEta < dEtaMax_cut_ : true;

  int64_t dPhi = (obj1.hwPhi() > obj2.hwPhi()) ? obj1.hwPhi().to_int() - obj2.hwPhi().to_int()
                                               : obj2.hwPhi().to_int() - obj1.hwPhi().to_int();
  res &= dPhiMin_cut_ ? dPhi > dPhiMin_cut_ : true;
  res &= dPhiMax_cut_ ? dPhi < dPhiMax_cut_ : true;

  int64_t dRSquared = dEta * dEta + dPhi * dPhi;
  res &= dRSquaredMin_cut_ ? dRSquared > dRSquaredMin_cut_ : true;
  res &= dRSquaredMax_cut_ ? dRSquared < dRSquaredMax_cut_ : true;

  res &= os_cut_ ? obj1.hwCharge() != obj2.hwCharge() : true;
  res &= ss_cut_ ? obj1.hwCharge() == obj2.hwCharge() : true;

  int32_t lutCoshDEta = dEta < DETA_LUT_SPLIT ? coshEtaLUT_[dEta] : coshEtaLUT2_[dEta - DETA_LUT_SPLIT];
  int32_t lutCosDPhi = cosPhiLUT_[dPhi];

  if (enable_sanity_checks_) {
    // Check whether the LUT error is smaller or equal than the expected maximum LUT error
    double coshEtaLUTMax = dEta < DETA_LUT_SPLIT ? coshEtaLUT_.hwMax_error() : coshEtaLUT2_.hwMax_error();
    double etaLUTScale = dEta < DETA_LUT_SPLIT ? coshEtaLUT_.output_scale() : coshEtaLUT2_.output_scale();

    if (std::abs(lutCoshDEta - etaLUTScale * std::cosh(dEta * scales_.eta_lsb())) > coshEtaLUTMax) {
      edm::LogError("COSH LUT") << "Difference larger than max LUT error: " << coshEtaLUTMax << ", lut: " << lutCoshDEta
                                << ", calc: " << etaLUTScale * std::cosh(dEta * scales_.eta_lsb()) << ", dEta: " << dEta
                                << ", scale: " << etaLUTScale;
    }

    if (std::abs(lutCosDPhi - cosPhiLUT_.output_scale() * std::cos(dPhi * scales_.phi_lsb())) >
        cosPhiLUT_.hwMax_error()) {
      edm::LogError("COS LUT") << "Difference larger than max LUT error: " << cosPhiLUT_.hwMax_error()
                               << ", lut: " << lutCosDPhi
                               << ", calc: " << cosPhiLUT_.output_scale() * std::cos(dPhi * scales_.phi_lsb());
    }
  }

  int64_t invMassDiv2;
  if (dEta < DETA_LUT_SPLIT) {
    // dEta [0, 2pi)
    invMassDiv2 = obj1.hwPT().to_int64() * obj2.hwPT().to_int64() * (lutCoshDEta - lutCosDPhi);
    res &=
        invMassDiv2Min_cut_ ? invMassDiv2 > std::round(invMassDiv2Min_cut_.value() * coshEtaLUT_.output_scale()) : true;
    res &=
        invMassDiv2Max_cut_ ? invMassDiv2 < std::round(invMassDiv2Max_cut_.value() * coshEtaLUT_.output_scale()) : true;
  } else {
    // dEta [2pi, 4pi), ignore cos
    invMassDiv2 = obj1.hwPT().to_int64() * obj2.hwPT().to_int64() * lutCoshDEta;
    res &= invMassDiv2Min_cut_ ? invMassDiv2 > std::round(invMassDiv2Min_cut_.value() * coshEtaLUT2_.output_scale())
                               : true;
    res &= invMassDiv2Max_cut_ ? invMassDiv2 < std::round(invMassDiv2Max_cut_.value() * coshEtaLUT2_.output_scale())
                               : true;
  }

  if (inv_mass_checks_) {
    double precInvMass =
        scales_.pT_lsb() * std::sqrt(2 * obj1.hwPT().to_double() * obj2.hwPT().to_double() *
                                     (std::cosh(dEta * scales_.eta_lsb()) - std::cos(dPhi * scales_.phi_lsb())));

    double lutInvMass = scales_.pT_lsb() *
                        std::sqrt(2 * static_cast<double>(invMassDiv2) /
                                  (dEta < DETA_LUT_SPLIT ? coshEtaLUT_.output_scale() : coshEtaLUT2_.output_scale()));

    double error = std::abs(precInvMass - lutInvMass);
    massErrors.emplace_back(InvariantMassError{error, error / precInvMass, precInvMass});
  }

  int64_t transMassDiv2 =
      obj1.hwPT().to_int64() * obj2.hwPT().to_int64() * (static_cast<int64_t>(coshEtaLUT_.output_scale()) - lutCosDPhi);
  res &= transMassDiv2Min_cut_ ? transMassDiv2 > std::round(transMassDiv2Min_cut_.value() * coshEtaLUT_.output_scale())
                               : true;
  res &= transMassDiv2Max_cut_ ? transMassDiv2 < std::round(transMassDiv2Max_cut_.value() * coshEtaLUT_.output_scale())
                               : true;

  return res;
}

DEFINE_FWK_MODULE(L1GTDoubleObjectCond);
