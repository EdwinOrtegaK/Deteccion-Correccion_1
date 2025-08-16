# Capa Enlace - CRC32 (Receptor) 
from typing import Tuple
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
    return "".join("1" if (x >> i) & 1 else "0" for i in range(31,-1,-1))

def verificar(frame_bits: str) -> Tuple[str, str]:
    if len(frame_bits) < 33:
        print("[ENLACE][RECEPTOR][CRC32] Trama inválida (<33 bits).")
        return "DISCARD", ""
    payload, recv_crc_bits = frame_bits[:-32], frame_bits[-32:]
    calc_crc_bits = to_bits32_msb(crc32_msb_bits(payload))
    print(f"[ENLACE][RECEPTOR][CRC32] payload_bits: {payload}")
    print(f"[ENLACE][RECEPTOR][CRC32] CRC recibido:   {recv_crc_bits}")
    print(f"[ENLACE][RECEPTOR][CRC32] CRC calculado: {calc_crc_bits}")
    if recv_crc_bits == calc_crc_bits:
        print("[ENLACE][RECEPTOR][CRC32] Verificación: OK (sin errores).")
        return "OK", payload
    else:
        print("[ENLACE][RECEPTOR][CRC32] Verificación: ERROR -> DESCARTAR.")
        return "DISCARD", ""
