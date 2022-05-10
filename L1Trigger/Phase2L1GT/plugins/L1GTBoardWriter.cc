/**
 * BoardDataWriter for validation with hardware. Currently only writting the algo bits is implemented.
 **/

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "L1Trigger/DemonstratorTools/interface/BoardDataWriter.h"
#include "L1Trigger/DemonstratorTools/interface/utilities.h"

#include "FWCore/Utilities/interface/EDGetToken.h"
#include "DataFormats/Common/interface/PathStatus.h"

#include "ap_int.h"

#include <vector>
#include <map>
#include <cmath>
#include <algorithm>

class L1GTBoardWriter : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit L1GTBoardWriter(const edm::ParameterSet&);

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  struct AlgoBit {
    unsigned int bit_;
    edm::EDGetTokenT<edm::PathStatus> token_;

    bool isSet(const edm::Event& event) const { return event.get(token_).accept(); }
  };

private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void endJob() override;

  size_t framesPerBX_;

  l1t::demo::BoardDataWriter boardDataWriter_;
  std::map<size_t, std::vector<AlgoBit>> algoBitMap_;
};

static l1t::demo::BoardDataWriter::ChannelMap_t generateChannelMap(const edm::ParameterSet& config,
                                                                   size_t framesPerBX) {
  l1t::demo::BoardDataWriter::ChannelMap_t channelMap;
  for (auto& param : config.getParameterSetVector("channelConfig")) {
    l1t::demo::LinkId id{"Algos", param.getParameter<unsigned int>("channel")};

    const edm::VParameterSet& algoBits = param.getParameterSetVector("algoBits");

    unsigned int maxBit = 0;

    for (const auto& algoBit : algoBits) {
      unsigned int bit = algoBit.getParameter<unsigned int>("bit");
      maxBit = std::max(bit, maxBit);
    }

    l1t::demo::ChannelSpec spec{
        1, static_cast<size_t>(framesPerBX - std::ceil(static_cast<float>(maxBit + 1) / 64)), 0};

    channelMap.insert({id, {spec, {id.channel}}});
  }

  return channelMap;
}

L1GTBoardWriter::L1GTBoardWriter(const edm::ParameterSet& config)
    : framesPerBX_(config.exists("framesPerBX") ? config.getParameter<unsigned int>("framesPerBX") : 9),
      boardDataWriter_(l1t::demo::parseFileFormat(config.getParameter<std::string>("format")),
                       config.getParameter<std::string>("outputFilename"),
                       framesPerBX_,
                       1,
                       config.exists("maxLines") ? config.getParameter<unsigned int>("maxLines") : 1024,
                       generateChannelMap(config, framesPerBX_)) {
  edm::ConsumesCollector iC(consumesCollector());
  for (const edm::ParameterSet& param : config.getParameterSetVector("channelConfig")) {
    std::vector<AlgoBit> algoBits;
    for (const edm::ParameterSet& algoConfig : param.getParameterSetVector("algoBits")) {
      edm::EDGetTokenT<edm::PathStatus> token =
          iC.consumes<edm::PathStatus>(edm::InputTag(algoConfig.getParameter<std::string>("path")));

      algoBits.emplace_back(AlgoBit{algoConfig.getParameter<unsigned int>("bit"), token});
    }

    std::sort(
        algoBits.begin(), algoBits.end(), [](const AlgoBit& lhs, const AlgoBit& rhs) { return lhs.bit_ < rhs.bit_; });

    algoBitMap_.insert({param.getParameter<unsigned int>("channel"), algoBits});
  }
}

void L1GTBoardWriter::analyze(const edm::Event& event, const edm::EventSetup& iSetup) {
  l1t::demo::EventData eventData;
  for (const auto& [channel, algoBits] : algoBitMap_) {
    std::vector<ap_uint<64>> bits(std::ceil(static_cast<float>(algoBits.back().bit_ + 1) / 64));

    for (const AlgoBit& algoBit : algoBits) {
      bits[algoBit.bit_ / 64].set(algoBit.bit_ % 64, algoBit.isSet(event));
    }

    eventData.add({"Algos", channel}, bits);
  }

  boardDataWriter_.addEvent(eventData);
}

void L1GTBoardWriter::endJob() { boardDataWriter_.flush(); }

void L1GTBoardWriter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription algoDesc;
  algoDesc.add<unsigned int>("bit");
  algoDesc.add<std::string>("path");

  edm::ParameterSetDescription algosDesc;
  algosDesc.add<unsigned int>("channel");
  algosDesc.addVPSet("algoBits", algoDesc);

  edm::ParameterSetDescription desc;
  desc.add<std::string>("outputFilename");
  desc.addVPSet("channelConfig", algosDesc);
  desc.addOptional<unsigned int>("framesPerBX", 9);
  desc.addOptional<unsigned int>("maxLines", 1024);
  desc.add<std::string>("format", "EMP");

  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(L1GTBoardWriter);
