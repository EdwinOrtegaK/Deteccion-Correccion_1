// Aplicación (Emisor)
#pragma once
#include <string>
#include <utility>

struct AppInput {
    std::string texto;    // ej. "Hola"
    std::string alg;      // "HAM" o "CRC32"
    double p_ruido;       // 0.0 .. 0.2
};

namespace application {
    AppInput solicitar_mensaje();
    void mostrar_respuesta(const std::string& line_json);

    std::pair<bool, AppInput> parse_cli(int argc, char** argv);
}
