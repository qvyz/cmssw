#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/L1Trigger/interface/L1EtMissParticle.h"
#include "DataFormats/L1Trigger/interface/L1JetParticle.h"
#include "DataFormats/L1Trigger/interface/L1MuonParticle.h"
#include "DataFormats/RecoCandidate/interface/RecoEcalCandidate.h"
#include "DataFormats/RecoCandidate/interface/RecoEcalCandidateFwd.h"
#include "DataFormats/EgammaCandidates/interface/Electron.h"
#include "DataFormats/EgammaCandidates/interface/ElectronFwd.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidate.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidateFwd.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "DataFormats/Candidate/interface/CompositeCandidateFwd.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETFwd.h"
#include "DataFormats/METReco/interface/CaloMET.h"
#include "DataFormats/METReco/interface/CaloMETFwd.h"
#include "DataFormats/METReco/interface/MET.h"
#include "DataFormats/METReco/interface/METFwd.h"
#include "DataFormats/TauReco/interface/HLTTau.h"
#include "DataFormats/TauReco/interface/HLTTauFwd.h"
#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/TauReco/interface/PFTauFwd.h"

#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"

#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"
#include "P2GTCandidate.h"
using namespace reco;
using namespace trigger;

#include "GT_TestfilterT.h"
#include "GT_Testfilter.h"
#include "P2GT_TestProducerCommon.h"
typedef P2GTDoubleObjFilterT<l1t::TkMuon,l1t::TkElectron> P2GTDoubleObjFilterMuEle;
typedef P2GT_TestProducerCommon<l1t::TkMuon> P2GT_TkmuonProd;




DEFINE_FWK_MODULE(P2GTDoubleObjFilterMuEle);
DEFINE_FWK_MODULE(P2GTDoubleObjFilter);
DEFINE_FWK_MODULE(P2GT_TkmuonProd);






