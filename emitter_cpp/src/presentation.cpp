//Presentación (Emisor)
#include "presentation.hpp"
#include <bitset>

namespace presentation {
    std::string ascii_to_bits(const std::string& s) {
        std::string out;
        out.reserve(s.size()*8);
        for (unsigned char c : s) {
            std::bitset<8> b(c);           // MSB-first
            out += b.to_string();
        }
        return out;
    }
}
