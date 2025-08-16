#include "enlace_crc32.hpp"
#include <string>
#include <cstdint>

static uint32_t crc32_msb_bits(const std::string& bits_msb){
    const uint32_t POLY = 0x04C11DB7u;
    uint32_t reg = 0xFFFFFFFFu;
    for(char c : bits_msb){
        uint32_t bit = (c=='1') ? 1u : 0u;
        uint32_t feedback = ((reg >> 31) & 1u) ^ bit;
        reg = (reg << 1) & 0xFFFFFFFFu;
        if(feedback) reg ^= POLY;
    }
    return reg ^ 0xFFFFFFFFu;
}

static std::string to_bits32_msb(uint32_t x){
    std::string s; s.reserve(32);
    for(int i=31;i>=0;i--) s.push_back( ((x>>i)&1u) ? '1':'0' );
    return s;
}

namespace enlace_crc32 {
    std::string append_crc32(const std::string& payload_bits) {
        uint32_t crc = crc32_msb_bits(payload_bits);
        std::string crc_bits = to_bits32_msb(crc);
        return payload_bits + crc_bits;
    }

    std::string crc32_bits_msb(const std::string& payload_bits) {
        uint32_t crc = crc32_msb_bits(payload_bits);  
        return to_bits32_msb(crc);                   
    }
}
