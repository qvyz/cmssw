#ifndef L1GTSingleInOutLUT_h
#define L1GTSingleInOutLUT_h

#include "DataFormats/L1Trigger/interface/P2GTCandidate.h"

#include <array>
#include <cmath>
#include <cstddef>
#include <sstream>
#include <string>

namespace l1t {

  template <std::size_t W_IN, std::size_t W_OUT>
  class L1GTSingleInOutLUT {
  public:
    template <typename FUNC>
    constexpr L1GTSingleInOutLUT(int input_resolution_reduction,
                                 double input_scale_factor,
                                 int output_scale_factor_num,
                                 int output_scale_factor_den,
                                 FUNC operation)
        : input_resolution_reduction_(input_resolution_reduction),
          contents_(generate(input_resolution_reduction,
                             input_scale_factor,
                             output_scale_factor_num,
                             output_scale_factor_den,
                             operation)) {}

    constexpr int operator[](int in) const { return contents_[in / input_resolution_reduction_]; }

    std::string get_contents_as_lut_file() const {
      std::ostringstream os;
      for (std::size_t idx = 0; idx < contents_.size(); ++idx) {
        // TODO: Make sure value fits into out_width!
        os << "@" << std::hex << idx << " " << contents_[idx] << "\n";
      }
      return os.str();
    }

  private:
    template <typename FUNC>
    static constexpr std::array<int, (1 << W_IN)> generate(int input_resolution_reduction,
                                                           double input_scale_factor,
                                                           int output_scale_factor_num,
                                                           int output_scale_factor_den,
                                                           FUNC operation) {
      std::array<int, (1 << W_IN)> contents{};

      int out_mask = (1 << W_OUT) - 1;

      for (int i = 0; i < (1 << W_IN); ++i) {
        int lut_output_raw{
            static_cast<int>(output_scale_factor_num * operation(input_resolution_reduction * input_scale_factor * i) /
                             output_scale_factor_den)};
        if (lut_output_raw < 0) {
          lut_output_raw += (1 << W_OUT);
        }
        contents[i] = lut_output_raw & out_mask;
      }

      return contents;
    }

    const int input_resolution_reduction_;
    const std::array<int, (1 << W_IN)> contents_;
  };

  /** cmath functions are only constexpr in gcc, this is unfortunately not standard but might be in the future,
   *  possibly C++23: https://github.com/cplusplus/papers/issues/104
   * */
  constexpr L1GTSingleInOutLUT<P2GTCandidate::hwPhi_t::width - 1, 5> cosPhiLUT(4, 0.00125, 10, 1, [](double x) {
    return std::cos(x);
  });

  constexpr L1GTSingleInOutLUT<P2GTCandidate::hwEta_t::width - 2, 17> coshEtaLUT(4, 0.00020, 10, 1, [](double x) {
    return std::cosh(x);
  });
}  // namespace l1t

#endif  // L1GTSingleInOutLUT_h
