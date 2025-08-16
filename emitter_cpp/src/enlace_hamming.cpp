// Capa Enlace - Hamming (Emisor)
#include "enlace_hamming.hpp"
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>

namespace {
    inline bool isPow2(int x){ return x && (x & -x) == x; }

    // Calcula r tal que 2^r >= m + r + 1
    int calc_r(int m){
        int r = 0;
        while((1<<r) < m + r + 1) r++;
        return r;
    }

    // Helper para layout de bits (p=paridad, d=dato)
    std::string layout_parity_data(int n) {
        std::string s;
        s.reserve(2*n);
        for (int msbPos = n; msbPos >= 1; --msbPos) {
            int lsbPos = msbPos;
            s += isPow2(lsbPos) ? 'p' : 'd';
            if (msbPos != 1) s += ' ';
        }
        return s;
    }
}

namespace enlace_hamming {

    int parity_bits_needed(int m_bits){ return calc_r(m_bits); }

    std::string build_codeword(const std::string& payload_bits) {
        const int m = (int)payload_bits.size();
        const int r = calc_r(m);
        const int n = m + r; // longitud total del codeword

        std::vector<int> cw(n+1, 0); // 1-indexado

        // Colocar bits de datos
        int j = m - 1; 
        for(int i=1; i<=n; ++i){
            if(!isPow2(i)){
                cw[i] = (j >= 0 ? (payload_bits[j] == '1') : 0);
                --j;
            }
        }

        // Calcular bits de paridad
        for(int p=1; p<=n; p<<=1){
            int parity = 0;
            for(int i=1; i<=n; ++i){
                if(i & p) parity ^= cw[i];
            }
            cw[p] = parity;
        }

        // Construir string MSB->LSB
        std::string codeword;
        codeword.reserve(n);
        for(int i=n; i>=1; --i) codeword.push_back(char('0' + cw[i]));

        // Imprimir layout
        std::cout << "[ENLACE][EMISOR][HAM] layout (MSB->LSB): "
                  << layout_parity_data(n) << "\n";

        return codeword;
    }
}
