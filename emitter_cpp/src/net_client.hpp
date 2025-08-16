#pragma once
#include <string>

namespace net_client {
    // Envía una línea (terminada en '\n') y devuelve UNA línea de respuesta
    std::string send_line(const std::string& host, int port, const std::string& line_json);
}
