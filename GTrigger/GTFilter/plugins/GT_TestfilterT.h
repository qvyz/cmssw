#ifndef P2GTDoubleObjFilterT_h

#define P2GTDoubleObjFilterT_h


//Base Class of the Filter, Taken from HLT
#include "HLTrigger/HLTcore/interface/HLTFilter.h"
#include "HLTrigger/HLTcore/interface/defaultModuleLabel.h"


//Muons from Correlator
#include "DataFormats/L1TCorrelator/interface/TkMuon.h"
#include "DataFormats/L1TCorrelator/interface/TkMuonFwd.h"

//Electrons from Correlator
#include "DataFormats/L1TCorrelator/interface/TkElectron.h"
#include "DataFormats/L1TCorrelator/interface/TkElectronFwd.h"
template <class T1, class T2>
class P2GTDoubleObjFilterT : public HLTFilter    {
public:
	explicit P2GTDoubleObjFilterT(const edm::ParameterSet&);

        ~P2GTDoubleObjFilterT() override;
        static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
        bool hltFilter(edm::Event&,
                 const edm::EventSetup&,
                 trigger::TriggerFilterObjectWithRefs& filterproduct) const override;
private:
        edm::InputTag l1tfirstTag_;  //input tag for L1 Tk Muon product
        edm::InputTag l1tsecondTag_;  //input tag for L1 Tk Ele product
        edm::EDGetTokenT<std::vector<T1>> l1tfirstToken_;  // token identifying product containing L1 TkMuons
        edm::EDGetTokenT<std::vector<T2>> l1tsecondToken_;  // token identifying product containing L1 TkEles
        double min_Pt_first_;                        // min pt cut 1
        double min_Pt_second_;                        // min pt cut 2
        int min_N_;                            // min number of candidates
        double min_Eta_first_;                       // min eta cut 1
        double min_Eta_second_;                       // min eta cut 2
        double max_Eta_first_;                       // max eta cut 1
        double max_Eta_second_;                       // max eta cut 2

};

template <class T1, class T2>
P2GTDoubleObjFilterT<T1,T2>::P2GTDoubleObjFilterT(const edm::ParameterSet& iConfig)
    : HLTFilter(iConfig),
      l1tfirstTag_(iConfig.getParameter<edm::InputTag>("inputTag1")),
      l1tsecondTag_(iConfig.getParameter<edm::InputTag>("inputTag2")),
      l1tfirstToken_(consumes<std::vector<T1>>(l1tfirstTag_)),
      l1tsecondToken_(consumes<std::vector<T2>>(l1tsecondTag_)),
  min_Pt_first_(iConfig.getParameter<int>("MinPtfirst")),
  min_Pt_second_(iConfig.getParameter<int>("MinPtsecond")),
  min_N_(iConfig.getParameter<int>("MinN")),
  min_Eta_first_(iConfig.getParameter<int>("MinEtafirst")),
  min_Eta_second_(iConfig.getParameter<int>("MinEtasecond")),
  max_Eta_first_(iConfig.getParameter<int>("MaxEtafirst")),
  max_Eta_second_(iConfig.getParameter<int>("MaxEtasecond")){
}


template <class T1, class T2>
P2GTDoubleObjFilterT<T1,T2>::~P2GTDoubleObjFilterT() = default;


template <class T1, class T2>
void P2GTDoubleObjFilterT<T1,T2>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  makeHLTFilterDescription(desc);
  desc.add<int>("MinPtfirst", -1.0);
  desc.add<int>("MinPtsecond", -1.0);
  desc.add<int>("MinEtafirst", -5.0);
  desc.add<int>("MinEtasecond", -5.0);
  desc.add<int>("MaxEtafirst", 5.0);
  desc.add<int>("MaxEtasecond", 5.0);
  desc.add<int>("MinN", 1);
  desc.add<edm::InputTag>("inputTag1", edm::InputTag("L1TkMuons"));
  desc.add<edm::InputTag>("inputTag2", edm::InputTag("L1TkElectrons"));
  descriptions.add(defaultModuleLabel<P2GTDoubleObjFilterT<T1,T2>>(), desc);

}






//for pointer stuff:
//https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideEDMRef
//The trigger::TriggerObjectType is just a number i dont know how its used, should ask someone
//https://cmsdoxygen.web.cern.ch/cmsdoxygen/CMSSW_12_0_0/doc/html/da/d54/namespacetrigger.html#a739430c65b695cfa3359bed709a2e6eb
template <class T1, class T2>
bool P2GTDoubleObjFilterT<T1,T2>::hltFilter(edm::Event& iEvent,
                                	const edm::EventSetup& iSetup,
                                	trigger::TriggerFilterObjectWithRefs& filterproduct) const {
        filterproduct.addCollectionTag(l1tfirstTag_);
        filterproduct.addCollectionTag(l1tsecondTag_);
        auto const& firstcoll_ = iEvent.getHandle(l1tfirstToken_);
        auto const& secondcoll_ = iEvent.getHandle(l1tsecondToken_);

        std::vector<edm::Ref<std::vector<T1>>> passingfirst;
        std::vector<edm::Ref<std::vector<T2>>> passingsecond;
        for (auto ifirst = firstcoll_->begin(); ifirst != firstcoll_->end(); ++ifirst) {
                if (ifirst->pt()>= min_Pt_first_ && ifirst->eta() <= max_Eta_first_ && ifirst->eta() >= min_Eta_first_) {
			edm::Ref<std::vector<T1>> ref(firstcoll_, distance(firstcoll_->begin(), ifirst));
                        passingfirst.push_back(ref);
                }
        }

        for (auto isecond = secondcoll_->begin(); isecond != secondcoll_->end(); ++isecond) {
                if (isecond->pt()>= min_Pt_second_ && isecond->eta() <= max_Eta_second_ && isecond->eta() >= min_Eta_second_) {
		       edm::Ref<std::vector<T2>> ref2(secondcoll_, distance(secondcoll_->begin(), isecond));
 
                       passingsecond.push_back(ref2);
                }
        }
	if((not passingfirst.empty())&&(not passingsecond.empty())){
        	for (const auto& second : passingsecond) {
                	filterproduct.addObject(trigger::TriggerObjectType::TriggerL1TkEle, second);
        	}

        	for (const auto& first : passingfirst) {
                	filterproduct.addObject(trigger::TriggerObjectType::TriggerL1TkMu, first);

        	}
        }

        const bool accept((static_cast<int>(passingfirst.size())>=min_N_)&&(static_cast<int>(passingsecond.size()) >= min_N_));
        return accept;
}
















#endif  //P2GTDoubleObjFilterT
