// Ruido (Emisor)
#pragma once
#include <string>
namespace noise {
    std::string flip_bits(const std::string& bits, double p); // Bernoulli(p)
}
