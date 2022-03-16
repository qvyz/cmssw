#ifndef P2GTDoubleObjFilter_h

#define P2GTDoubleObjFilter_h


//Base Class of the Filter, Taken from HLT
#include "HLTrigger/HLTcore/interface/HLTFilter.h"


//Muons from Correlator
#include "DataFormats/L1TCorrelator/interface/TkMuon.h"
#include "DataFormats/L1TCorrelator/interface/TkMuonFwd.h"

//Electrons from Correlator
#include "DataFormats/L1TCorrelator/interface/TkElectron.h"
#include "DataFormats/L1TCorrelator/interface/TkElectronFwd.h"

class P2GTDoubleObjFilter : public HLTFilter    {
public:
	explicit P2GTDoubleObjFilter(const edm::ParameterSet&);

        ~P2GTDoubleObjFilter() override;
        static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
        bool hltFilter(edm::Event&,
                 const edm::EventSetup&,
                 trigger::TriggerFilterObjectWithRefs& filterproduct) const override;
private:
        edm::InputTag l1TkMuonTag_;  //input tag for L1 Tk Muon product
        edm::InputTag l1TkEleTag_;  //input tag for L1 Tk Ele product
	typedef std::vector<l1t::TkMuon> TkMuonCollection;
	typedef std::vector<l1t::TkElectron> TkEleCollection;
        edm::EDGetTokenT<TkMuonCollection> tkMuonToken_;  // token identifying product containing L1 TkMuons
        edm::EDGetTokenT<TkEleCollection> tkEleToken_;  // token identifying product containing L1 TkEles
        double min_Pt_Muon_;                        // min pt cut
        double min_Pt_Ele_;                        // min pt cut
        int min_N_;                            // min number of candidates above pT cut
        double min_Eta_Muon_;                       // min eta cut
        double min_Eta_Ele_;                       // min eta cut
        double max_Eta_Muon_;                       // max eta cut
        double max_Eta_Ele_;                       // max eta cut

        double TkMuonOfflineEt(double Et, double Eta) const;
  	double TkEleOfflineEt(double Et, double Eta) const;
};
#endif  //P2GTDoubleObjFilter

