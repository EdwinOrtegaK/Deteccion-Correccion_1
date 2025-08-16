// Implementación Aplicación (Emisor)
#include "application.hpp"
#include <algorithm>
#include <iostream>

namespace application {
        std::pair<bool, AppInput> parse_cli(int argc, char** argv) {
        AppInput x;
        x.p_ruido = 0.0;
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if ((arg == "-m" || arg == "--msg") && i + 1 < argc) {
                x.texto = argv[++i];
            } else if ((arg == "-a" || arg == "--alg") && i + 1 < argc) {
                x.alg = argv[++i];
            } else if ((arg == "-p" || arg == "--p") && i + 1 < argc) {
                x.p_ruido = std::stod(argv[++i]);
            }
        }
        std::transform(x.alg.begin(), x.alg.end(), x.alg.begin(), ::toupper);
        if (!x.texto.empty() && (x.alg == "HAM" || x.alg == "CRC32")) {
            return {true, x};
        }
        return {false, {}};
    }
    AppInput solicitar_mensaje() {
        AppInput x;
        std::cout << "Mensaje (texto): ";
        std::getline(std::cin, x.texto);
        std::cout << "Algoritmo [HAM|CRC32]: ";
        std::getline(std::cin, x.alg);
        std::cout << "Probabilidad de ruido p (ej 0.01): ";
        std::cin >> x.p_ruido; std::cin.ignore();
        return x;
    }
    void mostrar_respuesta(const std::string& line_json) {
        std::cout << "Respuesta receptor: " << line_json << "\n";
    }
}
