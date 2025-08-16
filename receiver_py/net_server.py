# Transmisión - Servidor TCP (Receptor)
import socket, json

def serve(host="0.0.0.0", port=5050, handler=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port)); s.listen(1)
        print(f"[TRANSMISIÓN][RECEPTOR] escuchando en {host}:{port}")
        while True:
            conn, addr = s.accept()
            print(f"[TRANSMISIÓN][RECEPTOR] conexión de {addr}")
            with conn:
                data = b""
                while True:
                    chunk = conn.recv(4096)
                    if not chunk: break
                    data += chunk
                    while b"\n" in data:
                        line, _, data = data.partition(b"\n")
                        txt = line.decode("utf-8", errors="replace").strip()
                        if not txt: continue
                        # ver JSON recibido
                        print(f"[TRANSMISIÓN][RECEPTOR] JSON recibido: {txt}")
                        try:
                            msg = json.loads(txt)
                        except json.JSONDecodeError as e:
                            print(f"[TRANSMISIÓN][RECEPTOR] JSON inválido: {e}")
                            continue
                        try:
                            resp = handler(msg) if handler else {}
                        except Exception as e:
                            print(f"[RECEPTOR] Error en handler: {e}")
                            resp = {"status":"ERROR","info":{"detail":str(e)}}
                        if resp:
                            out = json.dumps(resp)+"\n"
                            conn.sendall(out.encode("utf-8"))
                            print(f"[TRANSMISIÓN][RECEPTOR] Respuesta: {out.strip()}")
