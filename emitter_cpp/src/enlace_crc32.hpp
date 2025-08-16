// Capa Enlace - CRC32 (Emisor)
#pragma once
#include <string>

namespace enlace_crc32 {
    std::string append_crc32(const std::string& payload_bits);

    std::string crc32_bits_msb(const std::string& payload_bits);

}
