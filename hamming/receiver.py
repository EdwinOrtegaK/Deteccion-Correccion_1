import sys

def is_binary(s): return len(s)>0 and set(s) <= {"0","1"}
def is_pow2(x): return x and (x & -x) == x

def bits_lsb_first(s_msb_first):
    # invierte para que index 1 sea LSB
    return [1 if c=="1" else 0 for c in s_msb_first[::-1]]

def msb_first_from_lsb_first(v):
    return "".join("1" if b else "0" for b in v[::-1])

def extract_payload_lsb_first(cw):
    n = len(cw)-1  # 1-indexado
    data = []
    for i in range(1, n+1):
        if not is_pow2(i):
            data.append(cw[i])
    return "".join("1" if b else "0" for b in data[::-1])

def main():
    print("Hamming (receptor Python). Ingrese codeword (MSB->LSB): ", end="", flush=True)
    s = sys.stdin.readline().strip()
    if not is_binary(s):
        print("Error: solo '0' y '1'."); return

    n = len(s)
    cw = [0] * (n+1)
    # cargar bits al vector 1-indexado
    v = bits_lsb_first(s)
    for i in range(1, n+1):
        cw[i] = v[i-1]

    # calcular síndrome
    syndrome = 0
    p = 1
    while p <= n:
        parity = 0
        for i in range(1, n+1):
            if i & p: parity ^= cw[i]
        if parity: syndrome |= p
        p <<= 1

    if syndrome == 0:
        payload = extract_payload_lsb_first(cw)
        print("No se detectaron errores. \nPayload:", payload)
        return

    if 1 <= syndrome <= n:
        # corregir
        cw[syndrome] ^= 1
        payload = extract_payload_lsb_first(cw)
        print(f"Se detectaron y corrigieron errores. \nBit corregido en posicion {syndrome}. \nPayload:", payload)
        return

    print("Se detectaron errores, pero no se pudo corregir de forma confiable.")

if __name__ == "__main__":
    main()
