// Capa Enlace - Hamming (Emisor)
#pragma once
#include <string>

namespace enlace_hamming {
    std::string build_codeword(const std::string& payload_bits);

    // helper para pruebas o introspección
    int parity_bits_needed(int m_bits);
}
