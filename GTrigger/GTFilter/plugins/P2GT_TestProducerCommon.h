// -*- C++ -*-
//
// Package:    GTrigger/GTFilter
// Class:      P2GT_TestProducerCommon
//
/**\class P2GT_TestProducerCommon P2GT_TestProducerCommon.cc GTrigger/GTFilter/plugins/P2GT_TestProducerCommon.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Elias Leutgeb
//         Created:  Sun, 16 Jan 2022 13:44:58 GMT
//
//
#ifndef P2GT_TestProducerCommon_h
#define P2GT_TestProducerCommon_h


// system include files
#include <memory>
#include <vector>
#include <cmath>
#include <iterator>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "P2GTCandidate.h"

//
// class declaration
//
template <class T>
class P2GT_TestProducerCommon : public edm::stream::EDProducer<>
{
public:
  explicit P2GT_TestProducerCommon(const edm::ParameterSet &);
  ~P2GT_TestProducerCommon();

  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
 // void beginStream(edm::StreamID) override;
  void produce(edm::Event &, const edm::EventSetup &) override;
 // void endStream() override;

  //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
  //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

  // ----------member data ---------------------------
  edm::InputTag const srcTag_;
  edm::EDGetTokenT<std::vector<T>> const srcToken_;

  typedef l1t::P2GTCandidate Candidate;
  typedef std::vector<Candidate> P2GT_CandidateCollection;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
template <class T>
P2GT_TestProducerCommon<T>::P2GT_TestProducerCommon(const edm::ParameterSet &iConfig) : srcTag_(iConfig.getParameter<edm::InputTag>("src")),
                                                                                        srcToken_(consumes<std::vector<T>>(srcTag_))
{
  produces<P2GT_CandidateCollection>("candColl").setBranchAlias("P2GT_CandidateCollectionTest");
}
template <class T>
P2GT_TestProducerCommon<T>::~P2GT_TestProducerCommon()
{
  // do anything here that needs to be done at destruction time
  // (e.g. close files, deallocate resources etc.)
  //
  // please remove this method altogether if it would be left empty
}

//
// member functions
//

// ------------ method called to produce the data  ------------
template <class T>
void P2GT_TestProducerCommon<T>::produce(edm::Event &iEvent, const edm::EventSetup &iSetup)
{
  using namespace edm;

  auto const& l1cand = iEvent.getHandle(srcToken_);
  Candidate res;
   P2GT_CandidateCollection resvec;
  for (auto icand = l1cand->begin(); icand != l1cand->end(); ++icand)
  {
    res.setHwPt(icand->hwPt());
    res.setHwEta(icand->hwEta());
    res.setHwPhi(icand->hwPhi());
    resvec.push_back(res);
  }
   
  
  iEvent.put(std::move(std::make_unique<P2GT_CandidateCollection>(resvec)), "P2GTColl");

  /* This is an event example
  //Read 'ExampleData' from the Event
  ExampleData const& in = iEvent.get(inToken_);

  //Use the ExampleData to create an ExampleData2 which 
  // is put into the Event
  iEvent.put(std::make_unique<ExampleData2>(in));
*/

  /* this is an EventSetup example
  //Read SetupData from the SetupRecord in the EventSetup
  SetupData& setup = iSetup.getData(setupToken_);
*/
}
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------

template <class T>
void P2GT_TestProducerCommon<T>::fillDescriptions(edm::ConfigurationDescriptions &descriptions)
{
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
/*
template <class T>
void P2GT_TestProducerCommon<T>::beginStream(edm::StreamID) {
  // please remove this method if not needed
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
template <class T>
void P2GT_TestProducerCommon<T>::endStream() {
  // please remove this method if not needed
}
*/


//define this as a plug-in
#endif
