// Main Emisor 
#include "application.hpp"
#include "presentation.hpp"
#include "enlace_hamming.hpp"
#include "enlace_crc32.hpp"
#include "noise.hpp"
#include "net_client.hpp"
#include <iostream>
#include <algorithm>

// helper: dif de bits (posiciones distintas, indexadas MSB=1)
static std::vector<int> diff_positions_msb(const std::string& a, const std::string& b){
    std::vector<int> pos;
    size_t n = std::min(a.size(), b.size());
    for(size_t i=0;i<n;i++){
        if(a[i]!=b[i]) pos.push_back(int(i)+1); // MSB=1
    }
    return pos;
}

// obtener solo los 32 bits de CRC si implementaste crc32_bits_msb
static std::string try_crc32_bits(const std::string& payload){
    try { return enlace_crc32::crc32_bits_msb(payload); }
    catch(...) { return ""; }
}

int main(int argc, char** argv) {
    auto cli = application::parse_cli(argc, argv);
    AppInput in;
    if (cli.first) in = cli.second;
    else           in = application::solicitar_mensaje();

    std::transform(in.alg.begin(), in.alg.end(), in.alg.begin(), ::toupper);
    if (in.alg != "HAM" && in.alg != "CRC32") {
        std::cerr << "[APLICACIÓN] Algoritmo no válido. Use HAM o CRC32.\n";
        return 1;
    }

    // APLICACIÓN
    std::cout << "[APLICACIÓN][EMISOR] Mensaje: \"" << in.texto
              << "\", Algoritmo=" << in.alg
              << ", p_ruido=" << in.p_ruido << "\n";

    // PRESENTACIÓN: texto -> bits
    auto payload = presentation::ascii_to_bits(in.texto);
    std::cout << "[PRESENTACIÓN][EMISOR] ASCII->bits: " << payload << "\n";

    // ENLACE (construcción de trama)
    std::string frame;
    if (in.alg == "HAM") {
        int m = (int)payload.size();
        int r = enlace_hamming::parity_bits_needed(m);
        frame = enlace_hamming::build_codeword(payload);
        std::cout << "[ENLACE][EMISOR][HAM] m=" << m << " bits, r=" << r
                  << " paridades, codeword: " << frame << "\n";
    } else {
        auto crc_bits = try_crc32_bits(payload);
        frame = enlace_crc32::append_crc32(payload);
        if (!crc_bits.empty())
            std::cout << "[ENLACE][EMISOR][CRC32] CRC(32): " << crc_bits << "\n";
        std::cout << "[ENLACE][EMISOR][CRC32] Trama=payload||CRC: " << frame << "\n";
    }

    // RUIDO
    auto noisy = noise::flip_bits(frame, in.p_ruido);
    auto flips = diff_positions_msb(frame, noisy);
    std::cout << "[RUIDO][EMISOR] p=" << in.p_ruido
              << ", posiciones volteadas (MSB=1): ";
    if (flips.empty()) std::cout << "NINGUNA";
    else { for(size_t i=0;i<flips.size();++i){ if(i) std::cout<<","; std::cout<<flips[i]; } }
    std::cout << "\n[RUIDO][EMISOR] Trama con ruido: " << noisy << "\n";

    // TRANSMISIÓN
    std::string json = std::string("{\"alg\":\"") + in.alg +
                       "\",\"frame_bits\":\"" + noisy + "\"}";
    std::cout << "[TRANSMISIÓN][EMISOR] Enviando JSON: " << json << "\n";
    auto resp = net_client::send_line("127.0.0.1", 5050, json);

    // Respuesta (ya contiene lo que imprime el receptor)
    application::mostrar_respuesta(resp);
    return 0;
}
