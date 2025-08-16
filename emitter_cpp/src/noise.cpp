#include "noise.hpp"
#include <random>

namespace noise {
    std::string flip_bits(const std::string& bits, double p) {
        static std::random_device rd; static std::mt19937 gen(rd());
        std::bernoulli_distribution flip(p);
        std::string out = bits;
        for (auto& ch : out) if (ch=='0' || ch=='1') if (flip(gen)) ch = (ch=='0')?'1':'0';
        return out;
    }
}
