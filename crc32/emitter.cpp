#include <bits/stdc++.h>
using namespace std;

static bool isBinary(const string& s){
    return !s.empty() && all_of(s.begin(), s.end(), [](char c){ return c=='0'||c=='1'; });
}

static uint32_t crc32_msb_bits(const string& bits_msb){
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

static string to_bits32_msb(uint32_t x){
    string s; s.reserve(32);
    for(int i=31;i>=0;i--) s.push_back( ((x>>i)&1u) ? '1':'0' );
    return s;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << "CRC-32 (emisor C++). Ingrese payload binario (MSB->LSB): " << flush;
    string m; 
    if(!(cin >> m)) return 0;
    if(!isBinary(m)){ cerr << "Error: solo 0's y 1's\n"; return 1; }

    uint32_t crc = crc32_msb_bits(m);
    string crc_bits = to_bits32_msb(crc);

    cout << "CRC32: " << crc_bits << "\n";
    cout << "Trama||CRC32: " << (m + crc_bits) << "\n";
    return 0;
}
