#ifndef DataFormats_L1Trigger_P2GTAlgoBlock_h
#define DataFormats_L1Trigger_P2GTAlgoBlock_h

#include "P2GTCandidate.h"

#include <vector>
#include <string>
#include <utility>

namespace l1t {

  class P2GTAlgoBlock;
  typedef std::vector<P2GTAlgoBlock> P2GTAlgoBlockCollection;

  class P2GTAlgoBlock {
  public:
    P2GTAlgoBlock() : algoName_(""), initial_(false), afterMask_(false), afterPrescale_(false), trigObjects_() {}
    P2GTAlgoBlock(std::string name, bool initial, bool afterMask, bool afterPrescale, P2GTCandidateVectorRef trigObjects)
        : algoName_(std::move(name)),
          initial_(initial),
          afterMask_(afterMask),
          afterPrescale_(afterPrescale),
          trigObjects_(std::move(trigObjects)) {}

    const std::string& algoName() const { return algoName_; }
    bool initial() const { return initial_; }
    bool afterMask() const { return afterMask_; }
    bool afterPrescale() const { return afterPrescale_; }
    const P2GTCandidateVectorRef& trigObjects() const { return trigObjects_; }

  private:
    const std::string algoName_;
    const bool initial_;
    const bool afterMask_;
    const bool afterPrescale_;
    const P2GTCandidateVectorRef trigObjects_;
  };

}  // namespace l1t

#endif  // DataFormats_L1Trigger_P2GTAlgoBlock_h
