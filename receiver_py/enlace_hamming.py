# Capa Enlace - Hamming (Receptor) 
from typing import Tuple, Optional

def _is_binary(s: str) -> bool:
    return len(s) > 0 and set(s) <= {"0", "1"}

def _is_pow2(x: int) -> bool:
    return x and (x & -x) == x

def _bits_lsb_first(bits_msb: str) -> list[int]:
    """Convierte MSB->LSB (string) a lista LSB-first (enteros 0/1)."""
    return [1 if c == "1" else 0 for c in bits_msb[::-1]]

def _payload_from_cw_lsb(cw_1idx: list[int]) -> str:
    """Extrae payload (datos) de un codeword 1-indexado LSB-first; retorna MSB->LSB."""
    n = len(cw_1idx) - 1
    data = []
    for i in range(1, n + 1):
        if not _is_pow2(i):
            data.append(cw_1idx[i])
    return "".join("1" if b else "0" for b in data[::-1])


def _layout_parity_data(n: int) -> str:
    """
    Devuelve una cadena "p d d p d ..." de longitud n (MSB->LSB),
    indicando qué posiciones son paridad (p) y cuáles datos (d).
    """
    out = []
    for msb_pos in range(n, 0, -1):  # MSB -> LSB
        lsb_pos = msb_pos            
        out.append('p' if _is_pow2(lsb_pos) else 'd')
    return " ".join(out)

def _pretty_bits_msb(bits_msb: str) -> str:
    """
    Inserta espacios cada 4 bits para legibilidad visual (MSB->LSB).
    """
    chunks = []
    s = bits_msb
    while s:
        take = len(s) % 4 or 4
        chunks.append(s[:take])
        s = s[take:]
    return " ".join(chunks)

def _mark_corrected_msb(n: int, syndrome_pos_lsb: int) -> str:
    """
    Dibuja una flecha (^) bajo el bit corregido, indexando la cadena MSB->LSB.
    syndrome_pos_lsb es 1-indexado en LSB-first; debemos convertir a índice MSB.
    """
    if syndrome_pos_lsb < 1 or syndrome_pos_lsb > n:
        return ""
    # índice MSB (1-index MSB) = n - (lsb_index - 1)
    msb_index_1 = n - (syndrome_pos_lsb - 1)
    # constuir una línea con espacios y '^' bajo la posición MSB correspondiente
    out = []
    for i in range(1, n + 1):
        out.append("^" if i == msb_index_1 else " ")
    return "".join(out)


def verificar_y_corregir(frame_bits: str) -> Tuple[str, str, Optional[int]]:
    """
    Verifica/corrige Hamming SEC (paridad par).
    Entradas/salidas en MSB->LSB.
    Retorna: (status, payload_bits, syndrome)
      - status: "OK" | "CORRECTED" | "DISCARD"
      - payload_bits: datos MSB->LSB si OK/CORRECTED; "" si DISCARD
      - syndrome: posición 1-indexada (LSB-first) corregida si CORRECTED; 0 si OK; None si DISCARD
    """
    if not _is_binary(frame_bits):
        print("[ENLACE][RECEPTOR][HAM] Trama inválida (no binaria).")
        return "DISCARD", "", None

    n = len(frame_bits)
    print(f"[ENLACE][RECEPTOR][HAM] codeword recibido (MSB->LSB): { _pretty_bits_msb(frame_bits) }")
    print(f"[ENLACE][RECEPTOR][HAM] layout (MSB->LSB):            { _layout_parity_data(n) }")

    # Construir vector 1-indexado LSB-first
    cw = [0] * (n + 1)
    v = _bits_lsb_first(frame_bits)
    for i in range(1, n + 1):
        cw[i] = v[i - 1]

    # Calcular síndrome (paridad par)
    syndrome = 0
    p = 1
    while p <= n:
        parity = 0
        for i in range(1, n + 1):
            if i & p:
                parity ^= cw[i]
        if parity:
            syndrome |= p
        p <<= 1

    if syndrome == 0:
        payload = _payload_from_cw_lsb(cw)
        print("[ENLACE][RECEPTOR][HAM] Síndrome = 0 → OK (sin errores).")
        print(f"[ENLACE][RECEPTOR][HAM] Payload (MSB->LSB):          { _pretty_bits_msb(payload) }")
        return "OK", payload, 0

    if 1 <= syndrome <= n:
        # Mostrar una guía visual del bit corregido bajo la cadena MSB
        caret_line = _mark_corrected_msb(n, syndrome)
        if caret_line:
            print(f"[ENLACE][RECEPTOR][HAM] Bit a corregir (MSB->LSB):  { _pretty_bits_msb(frame_bits) }")
            print(f"[ENLACE][RECEPTOR][HAM]                             { caret_line }")
        print(f"[ENLACE][RECEPTOR][HAM] Síndrome = {syndrome} (LSB=1) → corregir esa posición.")
        cw[syndrome] ^= 1  # flip

        payload = _payload_from_cw_lsb(cw)
        print(f"[ENLACE][RECEPTOR][HAM] Payload corregido (MSB->LSB): { _pretty_bits_msb(payload) }")
        return "CORRECTED", payload, syndrome

    print("[ENLACE][RECEPTOR][HAM] Síndrome fuera de rango → DESCARTAR.")
    return "DISCARD", "", None
