import sys

POLY = 0x04C11DB7

def is_binary(s): 
    return len(s) > 0 and set(s) <= {"0","1"}

def crc32_msb_bits(bits):
    reg = 0xFFFFFFFF
    for c in bits:
        bit = 1 if c == "1" else 0
        feedback = ((reg >> 31) & 1) ^ bit
        reg = ((reg << 1) & 0xFFFFFFFF)
        if feedback:
            reg ^= POLY
    return reg ^ 0xFFFFFFFF

def to_bits32_msb(x):
    return "".join("1" if (x >> i) & 1 else "0" for i in range(31,-1,-1))

def main():
    print("CRC-32 (receptor Python). Ingrese trama||CRC32 (MSB->LSB): ", end="", flush=True)
    s = sys.stdin.readline().strip()
    if not is_binary(s) or len(s) < 33:
        print("Error: se requiere binario y longitud >= 33 (payload + 32 bits de CRC).")
        return

    payload, recv_crc_bits = s[:-32], s[-32:]
    calc_crc_bits = to_bits32_msb(crc32_msb_bits(payload))

    if recv_crc_bits == calc_crc_bits:
        print("No se detectaron errores. \nPayload:", payload)
    else:
        print("Se detectaron errores. \nTrama descartada.")

if __name__ == "__main__":
    main()
