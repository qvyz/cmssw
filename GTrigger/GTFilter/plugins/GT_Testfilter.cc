// -*- C++ -*-
//
// Package:    HLTrigger/GT_Testfilter
// Class:      GT_Testfilter
//
/**\class GT_Testfilter GT_Testfilter.cc HLTrigger/GT_Testfilter/plugins/GT_Testfilter.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Elias Leutgeb
//         Created:  Mon, 06 Sep 2021 14:17:46 GMT
//
//
//



#include "GT_Testfilter.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"

#include "DataFormats/Common/interface/Handle.h"

#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"
#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/EventSetupRecord.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

//
// constructors and destructor
//


P2GTDoubleObjFilter::P2GTDoubleObjFilter(const edm::ParameterSet& iConfig)
    : HLTFilter(iConfig),
      l1TkMuonTag_(iConfig.getParameter<edm::InputTag>("inputTag1")),
      l1TkEleTag_(iConfig.getParameter<edm::InputTag>("inputTag2")),
      tkMuonToken_(consumes<TkMuonCollection>(l1TkMuonTag_)),
      tkEleToken_(consumes<TkEleCollection>(l1TkEleTag_)){
  min_Pt_Muon_ = iConfig.getParameter<double>("MinPtMuon");
  min_Pt_Ele_ = iConfig.getParameter<double>("MinPtEle");
  min_N_ = iConfig.getParameter<int>("MinN");
  min_Eta_Muon_ = iConfig.getParameter<double>("MinEtaMuon");
  min_Eta_Ele_ = iConfig.getParameter<double>("MinEtaEle");
  max_Eta_Muon_ = iConfig.getParameter<double>("MaxEtaMuon");
  max_Eta_Ele_ = iConfig.getParameter<double>("MaxEtaEle");
}


//Destructor


P2GTDoubleObjFilter::~P2GTDoubleObjFilter() = default;




//member functions


void P2GTDoubleObjFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  makeHLTFilterDescription(desc);
  desc.add<double>("MinPtMuon", -1.0);
  desc.add<double>("MinPtEle", -1.0);
  desc.add<double>("MinEtaMuon", -5.0);
  desc.add<double>("MinEtaEle", -5.0);
  desc.add<double>("MaxEtaMuon", 5.0);
  desc.add<double>("MaxEtaEle", 5.0);
  desc.add<int>("MinN", 1);
  desc.add<edm::InputTag>("inputTag1", edm::InputTag("L1TkMuons"));
  desc.add<edm::InputTag>("inputTag2", edm::InputTag("L1TkElectrons"));
}

















bool P2GTDoubleObjFilter::hltFilter(edm::Event& iEvent,
                                const edm::EventSetup& iSetup,
                                trigger::TriggerFilterObjectWithRefs& filterproduct) const {
	using namespace std;
  	using namespace edm;
  	using namespace reco;
  	using namespace trigger;
    	filterproduct.addCollectionTag(l1TkMuonTag_);
    	filterproduct.addCollectionTag(l1TkEleTag_);
 	Handle<l1t::TkMuonCollection> tkMuons;
	Handle<l1t::TkElectronCollection> tkEle;
  	iEvent.getByToken(tkMuonToken_, tkMuons);
  	iEvent.getByToken(tkEleToken_, tkEle);

 	std::vector<l1t::TkMuonRef> passingMuons;
	std::vector<l1t::TkElectronRef> passingEles;
  	auto atrkmuons(tkMuons->begin());
  	auto otrkmuons(tkMuons->end());
  	TkMuonCollection::const_iterator itkMuon;
  	for (itkMuon = atrkmuons; itkMuon != otrkmuons; itkMuon++) {
  		if ((itkMuon->pt() >= min_Pt_Muon_) && (itkMuon->eta() <= max_Eta_Muon_) && (itkMuon->eta() >= min_Eta_Muon_)) {
      			passingMuons.push_back(l1t::TkMuonRef(tkMuons, distance(atrkmuons, itkMuon)));
   		}
	}
  	for (const auto& muon : passingMuons) {
    		filterproduct.addObject(trigger::TriggerObjectType::TriggerL1TkMu, muon);
  	}

	auto atrkeles(tkEle->begin());
        auto otrkeles(tkEle->end());
        TkEleCollection::const_iterator itkEle;
        for (itkEle = atrkeles; itkEle != otrkeles; itkEle++) {
                if ((itkEle->pt() >= min_Pt_Ele_) && (itkEle->eta() <= max_Eta_Ele_) && (itkEle->eta() >= min_Eta_Ele_)) {
                        passingEles.push_back(l1t::TkElectronRef(tkEle, distance(atrkeles, itkEle)));
                }
        }
        for (const auto& ele : passingEles) {
                filterproduct.addObject(trigger::TriggerObjectType::TriggerL1TkEle, ele);
        }


	
  	const bool accept((static_cast<int>(passingMuons.size())>=min_N_)&&(static_cast<int>(passingMuons.size()) >= min_N_));
  	return accept;
}

