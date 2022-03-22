 #ifndef P2GTCandidate_h
 #define P2GTCandidate_h
 
 #include "DataFormats/Candidate/interface/LeafCandidate.h"
 #include "DataFormats/L1Trigger/interface/BXVector.h"
 namespace l1t {
 
   class P2GTCandidate;
   typedef BXVector<P2GTCandidate> P2GTCandidateBxCollection;
   typedef edm::Ref<P2GTCandidateBxCollection> P2GTCandidateRef;
   typedef edm::RefVector<P2GTCandidateBxCollection> P2GTCandidateRefVector;
   typedef std::vector<P2GTCandidateRef> P2GTCandidateVectorRef;
 
   class P2GTCandidate : public reco::LeafCandidate {
   public:
     P2GTCandidate();
 

 
     ~P2GTCandidate() override;
 
     // methods to set integer values
     void setHwPt(int pt) { hwPt_ = pt; }
     void setHwEta(int eta) { hwEta_ = eta; }
     void setHwPhi(int phi) { hwPhi_ = phi; }
     void setHwQual(int qual) { hwQual_ = qual; }
     void setHwIso(int iso) { hwIso_ = iso; }
     void setHwDZ(int DZ) { hwDz_ = DZ;}
     void setHwDD(int DD) { hwDd_ = DD;}
     void setHwCharge(int Charge) { hwCharge_ = Charge;}
     void setHwMass(int Mass) { hwMass_ = Mass;}
     void setHwIndex(int Index) { hwIndex_ = Index;}
     void setHwSeedPt(int SeedPt) { hwSeedPt_ = SeedPt;}


     // methods to retrieve integer values
     int hwPt() const { return hwPt_.value(); }
     int hwEta() const { return hwEta_.value(); }
     int hwPhi() const { return hwPhi_.value(); }
     int hwQual() const { return hwQual_.value(); }
     int hwIso() const { return hwIso_.value(); }
     int hwDZ() const { return hwDz_.value();}
     int hwDD() const { return hwDd_.value();}
     int hwCharge() const { return hwCharge_.value();}
     int hwMass() const { return hwMass_.value();}
     int hwIndex() const { return hwIndex_.value();}
     int hwSeedPt() const { return hwSeedPt_.value();} 


    // This is probably needed later:
    //  virtual bool operator==(const l1t::P2GTCandidate& rhs) const;
    //  virtual inline bool operator!=(const l1t::P2GTCandidate& rhs) const { return !(operator==(rhs)); };
 
   private:
    std::optional<int> hwPt_;
    std::optional<int> hwEta_;
    std::optional<int> hwPhi_;
    std::optional<int> hwQual_;
    std::optional<int> hwIso_;
    std::optional<int> hwDz_;
    std::optional<int> hwDd_;
    std::optional<int> hwCharge_; 
    std::optional<int> hwMass_;
    std::optional<int> hwIndex_;
    std::optional<int> hwSeedPt_;
   };
 
 };  // namespace l1t
 
 #endif

 	
