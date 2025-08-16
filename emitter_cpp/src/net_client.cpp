#include "net_client.hpp"
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdexcept>
#include <string>

namespace net_client {
    std::string send_line(const std::string& host, int port, const std::string& line_json) {
        int sock = ::socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) throw std::runtime_error("socket()");
        sockaddr_in addr{}; 
        addr.sin_family = AF_INET; 
        addr.sin_port = htons(port);
        if (::inet_pton(AF_INET, host.c_str(), &addr.sin_addr) != 1) {
            ::close(sock);
            throw std::runtime_error("inet_pton()");
        }
        if (::connect(sock, (sockaddr*)&addr, sizeof(addr)) < 0) {
            ::close(sock);
            throw std::runtime_error("connect()");
        }

        // Enviar línea con '\n'
        std::string line = line_json; 
        line.push_back('\n');
        ssize_t sent = ::send(sock, line.c_str(), (int)line.size(), 0);
        if (sent < 0) { ::close(sock); throw std::runtime_error("send()"); }

        // Leer UNA línea de respuesta (hasta '\n')
        std::string resp;
        char c;
        while (true) {
            ssize_t n = ::recv(sock, &c, 1, 0);
            if (n <= 0) break;      // conexión cerrada / error: devolvemos lo leído
            if (c == '\n') break;   // fin de línea
            resp.push_back(c);
        }
        ::close(sock);
        return resp;
    }
}
