#!/usr/bin/env python3
import argparse, json, os, random, socket, csv, time

# Presentación
def ascii_to_bits(text: str) -> str:
    return "".join(f"{ord(c):08b}" for c in text)

# Enlace: Hamming (emisor)
def _is_pow2(x: int) -> bool:
    return x and (x & -x) == x

def hamming_encode(bits_msb: str) -> str:
    m = bits_msb
    md = len(m)
    r = 0
    while (1 << r) < md + r + 1:
        r += 1
    n = md + r
    cw = [0]*(n+1)
    j = md - 1
    for i in range(1, n+1):
        if not _is_pow2(i):
            cw[i] = 1 if (j >= 0 and m[j] == "1") else 0
            j -= 1
    p = 1
    while p <= n:
        parity = 0
        for i in range(1, n+1):
            if i & p:
                parity ^= cw[i]
        cw[p] = parity
        p <<= 1
    # regreso MSB->LSB
    return "".join("1" if cw[i] else "0" for i in range(n, 0, -1))

# Enlace: CRC-32 (emisor)
POLY = 0x04C11DB7

def crc32_msb_bits(bits: str) -> int:
    reg = 0xFFFFFFFF
    for c in bits:
        bit = 1 if c == "1" else 0
        feedback = ((reg >> 31) & 1) ^ bit
        reg = ((reg << 1) & 0xFFFFFFFF)
        if feedback:
            reg ^= POLY
    return reg ^ 0xFFFFFFFF

def to_bits32_msb(x: int) -> str:
    return "".join("1" if (x >> i) & 1 else "0" for i in range(31, -1, -1))

def crc_append(bits: str) -> str:
    return bits + to_bits32_msb(crc32_msb_bits(bits))

# Ruido
def flip_bits(bits: str, p: float, rng: random.Random) -> str:
    out = []
    for b in bits:
        if rng.random() < p:
            out.append('0' if b == '1' else '1')
        else:
            out.append(b)
    return "".join(out)

# Net (cliente)
def send_line(host: str, port: int, line: str) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.sendall((line + "\n").encode("utf-8"))
        buf = b""
        while not buf.endswith(b"\n"):
            chunk = s.recv(4096)
            if not chunk:
                break
            buf += chunk
        return buf.decode("utf-8").rstrip("\n")
    finally:
        s.close()

# Main batch
def main():
    ap = argparse.ArgumentParser(description="Cliente batch para Lab2 Parte 2")
    ap.add_argument("--alg", choices=["HAM","CRC"], required=True, help="Algoritmo en Enlace")
    ap.add_argument("--p", type=float, default=0.0, help="Probabilidad de flip por bit")
    ap.add_argument("--n", type=int, default=1000, help="Número de mensajes a enviar")
    ap.add_argument("--len", type=int, default=8, help="Longitud del mensaje en BYTES (ASCII)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=5050)
    ap.add_argument("--seed", type=int, default=123)
    ap.add_argument("--csv", default="results.csv", help="Archivo CSV de salida")
    args = ap.parse_args()

    rng = random.Random(args.seed)

    # CSV headers
    exists = os.path.exists(args.csv)
    f = open(args.csv, "a", newline="")
    wr = csv.writer(f)
    if not exists:
        wr.writerow(["ts","alg","p","msg_bytes","frame_bits_len","status","syndrome","ok_text_match"])

    ok_count = corr_count = disc_count = 0

    for i in range(args.n):
        # Generar mensaje ASCII aleatorio (a..z y espacio)
        msg = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz ") for _ in range(args.len))
        payload_bits = ascii_to_bits(msg)

        if args.alg == "HAM":
            frame = hamming_encode(payload_bits)
        else:
            frame = crc_append(payload_bits)

        noisy = flip_bits(frame, args.p, rng)

        line = json.dumps({"alg": args.alg, "frame_bits": noisy})
        resp_raw = send_line(args.host, args.port, line)

        try:
            resp = json.loads(resp_raw)
        except json.JSONDecodeError:
            resp = {"status":"ERROR","info":{"detail":"bad json"}, "decoded_text":""}

        status = resp.get("status","ERROR")
        decoded = resp.get("decoded_text","")
        syn = resp.get("info",{}).get("syndrome",0)

        # Validación de éxito
        ok_text_match = (decoded == msg) if status in ("OK","CORRECTED") else False

        # Contadores
        if status == "OK":
            ok_count += 1
        elif status == "CORRECTED":
            corr_count += 1
        else:
            disc_count += 1

        wr.writerow([int(time.time()), args.alg, args.p, len(msg), len(frame), status, syn, int(ok_text_match)])

        # Opcional: barra mínima
        if (i+1) % max(1, args.n//10) == 0:
            print(f"[{args.alg}] p={args.p}  {i+1}/{args.n}  OK={ok_count} CORR={corr_count} DISC={disc_count}", flush=True)

    f.close()
    print(f"[FIN] CSV -> {args.csv}  Totales: OK={ok_count} CORR={corr_count} DISC={disc_count}")

if __name__ == "__main__":
    main()
